// static/js/image_detail.js
document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("ocrCanvas");
  const ctx = canvas.getContext("2d");
  const img = new Image();

  // Flask 템플릿에서 data-* 속성으로 전달받은 경로 사용
  const imageSrc = canvas.dataset.imageSrc;
  img.src = imageSrc;

  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);

    Tesseract.recognize(img, "kor+eng", { logger: m => console.log(m) })
      .then(({ data }) => {
        data.words.forEach(word => {
          const { x0, y0, x1, y1 } = word.bbox;
          const conf = word.confidence;
          const color =
            conf > 85 ? "green" : conf > 50 ? "orange" : "red";

          ctx.strokeStyle = color;
          ctx.lineWidth = 2;
          ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);

          ctx.font = "16px Arial";
          ctx.fillStyle = color;
          ctx.fillText(
            word.text,
            x0,
            y0 > 20 ? y0 - 5 : y1 + 20
          );
        });
      })
      .catch(err => console.error("OCR 시각화 실패:", err));
  };
});
