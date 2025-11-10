document.addEventListener("DOMContentLoaded", () => {
  // ✅ 파일 이름 표시
  const fileInput = document.getElementById("file");
  const fileName = document.getElementById("file-name");

  if (fileInput && fileName) {
    fileInput.addEventListener("change", () => {
      fileName.textContent = fileInput.files.length > 0
        ? fileInput.files[0].name
        : "아직 선택된 파일이 없습니다.";
    });
  }

  // ✅ 삭제 기능
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const filename = btn.dataset.filename;
      if (!confirm(`${filename} 파일을 삭제하시겠습니까?`)) return;

      try {
        const res = await fetch(`${window.location.pathname}/delete/${filename}`, {
          method: "POST",
        });
        const data = await res.json();
        alert(data.message);

        if (data.success) {
          // ✅ 1️⃣ 테이블 행 삭제
          const row = document.getElementById(`row-${filename}`);
          if (row) row.remove();

          // ✅ 2️⃣ 총 지출 금액 갱신
          updateTotalSpent();
        }
      } catch (err) {
        alert("삭제 중 오류가 발생했습니다.");
        console.error(err);
      }
    });
  });

  // ✅ 총 지출 금액 재계산 함수
  function updateTotalSpent() {
    const totalElement = document.querySelector(".total-spent span");
    if (!totalElement) return;

    // 테이블 내 남은 총액을 모두 합산
    let newTotal = 0;
    document.querySelectorAll(".image-table tbody tr td:nth-child(3)").forEach(td => {
      const text = td.textContent.replace(/[^\d]/g, ""); // 숫자만 추출
      if (text) newTotal += parseInt(text);
    });

    totalElement.textContent = `${newTotal.toLocaleString()} 원`;
  }
});
