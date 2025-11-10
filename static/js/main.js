// main.js
import { openModal, closeModal, registerModalOutsideClick } from './modal.js';

// HTML에서 onclick으로 호출할 수 있게 전역 등록
window.openModal = openModal;
window.closeModal = closeModal;

// 페이지 로드 시 모달 외부 클릭 이벤트 등록
document.addEventListener('DOMContentLoaded', () => {
  registerModalOutsideClick();
});
