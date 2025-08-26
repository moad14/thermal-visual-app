document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("visual", document.getElementById("visual").files[0]);
  formData.append("thermal", document.getElementById("thermal").files[0]);

  try {
    const res = await fetch("http://127.0.0.1:8000/process", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    document.getElementById("jsonResult").textContent = JSON.stringify(data, null, 2);

    if (data.image_base64) {
      document.getElementById("outputImage").src = "data:image/jpeg;base64," + data.image_base64;
    }
  } catch (err) {
    console.error(err);
    alert("Error occurred, check console");
  }
});
