// modal.js에서 임포트
// utils.js
export function clearInputs(modal) {
  if (!modal) return;
  const inputs = modal.querySelectorAll('input, textarea');
  inputs.forEach(i => (i.value = ''));
}
