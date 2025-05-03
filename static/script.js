// 이미지 생성
async function generateImage() {
  const prompt = document.getElementById("prompt").value;

  const response = await fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  const data = await response.json();
  const resultDiv = document.getElementById("generate-result");

  if (data.image_url) {
    resultDiv.innerHTML = `<img src="${data.image_url}" alt="생성된 이미지" style="max-width: 512px;" />`;
  } else {
    resultDiv.innerHTML = `<p>❗ 오류: ${data.error}</p>`;
  }
}

// 업로드 이미지 미리보기
document.getElementById("imageInput").addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const preview = document.getElementById("original-preview");
    preview.src = URL.createObjectURL(file);
  }
});

// 이미지 업로드 & 지브리풍 변환
document.getElementById("upload-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const formData = new FormData();
  const fileInput = document.getElementById("imageInput");
  formData.append("image", fileInput.files[0]);

  const response = await fetch("/upload", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  const resultDiv = document.getElementById("upload-result");

  if (data.result_url) {
    resultDiv.innerHTML = `<img src="${data.result_url}" alt="지브리풍 결과 이미지" />`;
  } else {
    resultDiv.innerHTML = `<p>❗ 오류가 발생했어요</p>`;
  }
});

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("show");
}

// 예시 프롬프트
function useExample(text) {
  document.getElementById("prompt").value = text;
}
