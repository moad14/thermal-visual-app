import cv2
import numpy as np
from ultralytics import YOLO
from flirimageextractor import FlirImageExtractor
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# تحميل الموديل مرة واحدة
model_path = "runs/train/my_yolov8_model/weights/best.pt"
model = YOLO(model_path)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ممكن تخصصها على http://localhost:5500 فقط
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# السماح بالاتصال من أي مكان (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def classify_component(name, tmax):
    if name == "antenna":
        if tmax < 10: return (255,255,255), "Normal"
        elif tmax <= 30: return (0,255,255), "Slightly hot"
        else: return (0,0,255), "Critical"
    elif name == "lighnig-rad":
        if tmax < 10: return (255,255,255), "Normal"
        elif tmax <= 20: return (0,255,255), "Slightly hot"
        else: return (0,0,255), "Critical"
    elif name in ["microware-dish","power-box"]:
        if tmax < 15: return (255,255,255), "Normal"
        elif tmax <= 35: return (0,255,255), "Slightly hot"
        else: return (0,0,255), "Critical"
    elif name == "radio-unit":
        if tmax < 10: return (255,255,255), "Normal"
        elif tmax <= 33: return (0,255,255), "Slightly hot"
        else: return (0,0,255), "Critical"
    return (0,255,0), "Normal"

def process_images(thermal_file, visual_file):
    thermal_path = "temp_thermal.jpg"
    visual_path = "temp_visual.jpg"
    with open(thermal_path, "wb") as f:
        f.write(thermal_file.file.read())
    with open(visual_path, "wb") as f:
        f.write(visual_file.file.read())

    # إحداثيات القص
    scale_used_when_selecting = 0.2
    x_start_rz, y_start_rz, w_rz, h_rz = 131, 91, 556, 420

    # === اقرأ الصور ===
    rgb = cv2.imread(visual_path)
    if rgb is None:
        raise FileNotFoundError("❌ لم يتم العثور على الصورة العادية")

    # قص الجزء المطلوب من الصورة العادية
    x0 = int(round(x_start_rz / scale_used_when_selecting))
    y0 = int(round(y_start_rz / scale_used_when_selecting))
    w0 = int(round(w_rz / scale_used_when_selecting))
    h0 = int(round(h_rz / scale_used_when_selecting))
    cropped_rgb = rgb[y0:y0+h0, x0:x0+w0]

    # === معالجة الصورة الحرارية ===
    flir = FlirImageExtractor()
    flir.process_image(thermal_path)
    thermal_np = flir.get_thermal_np()
    H_th, W_th = thermal_np.shape

    thermal_norm = cv2.normalize(thermal_np, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    thermal_color = cv2.applyColorMap(thermal_norm, cv2.COLORMAP_INFERNO)

    # === مواءمة: غير حجم القص ليطابق الحرارية ===
    aligned_rgb = cv2.resize(cropped_rgb, (W_th, H_th))

    # === تشغيل YOLO على القص العادي فقط ===
    res = model.predict(aligned_rgb, conf=0.35, verbose=False)[0]

    detected_objects = []
    for xyxy, cls in zip(res.boxes.xyxy.cpu().numpy(), res.boxes.cls.cpu().numpy()):
        x1, y1, x2, y2 = map(int, xyxy)
        roi = thermal_np[y1:y2, x1:x2]
        if roi.size == 0: 
            continue
        tmax = float(np.max(roi))
        label = model.names[int(cls)]

        # تصنيف الحالة
        color, state = classify_component(label, tmax)

        detected_objects.append({
            "label": label,
            "temperature": round(tmax, 1),
            "state": state
        })

        # رسم على الحرارية
        cv2.rectangle(thermal_color, (x1, y1), (x2, y2), color, 2)
        cv2.putText(thermal_color, f"{label}: {tmax:.1f}C",
                    (x1, max(15, y1-8)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.55, color, 2)

    # حفظ النتيجة وتحويلها base64
    _, buffer = cv2.imencode(".jpg", thermal_color)
    encoded_img = base64.b64encode(buffer).decode("utf-8")

    return encoded_img, detected_objects


@app.post("/analyze/")
async def analyze(thermal: UploadFile = File(...), visual: UploadFile = File(...)):
    try:
        result_img, detected_objects = process_images(thermal, visual)
        return {
            "status": "success",
            "message": "تم التحليل بنجاح ✅",
            "result_image": result_img,
            "detected_objects": detected_objects
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
