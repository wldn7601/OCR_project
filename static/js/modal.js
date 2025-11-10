// modal.js
import { clearInputs } from './utils.js';

// 모달 열기
export function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'block';
    clearInputs(modal);
  }
}

// 모달 닫기
export function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'none';
    clearInputs(modal);
  }
}

// 모달 바깥 클릭 시 닫기
export function registerModalOutsideClick() {
  window.addEventListener('click', (e) => {
    document.querySelectorAll('.modal').forEach((modal) => {
      if (e.target === modal) {
        modal.style.display = 'none';
        clearInputs(modal);
      }
    });
  });
}
