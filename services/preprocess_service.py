import cv2
import numpy as np
from pathlib import Path


def deskew(image: np.ndarray) -> np.ndarray:
    """기울기 보정 (세로형 영수증 대응)"""
    gray = cv2.bitwise_not(image)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = 90 + angle
    elif angle > 45:
        angle = angle - 90

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(255, 255, 255))
    return rotated


def preprocess_image(image_path: Path) -> Path:
    """영수증 전용 전처리: 조명 보정 + 대비 향상 + 이진화 + 기울기 보정 + 샤프닝"""
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"이미지를 읽을 수 없습니다: {image_path}")

    # 1️⃣ Grayscale 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2️⃣ Gaussian Blur (노이즈 완화)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # 3️⃣ Illumination Correction (조명 보정)
    background = cv2.medianBlur(blurred, 25)
    corrected = cv2.divide(blurred, background, scale=255)

    # 4️⃣ Contrast Enhancement (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(corrected)

    # 5️⃣ Adaptive Threshold (밝기 균일화)
    binary = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21, 10
    )

    # 7️⃣ Skew Correction (기울기 보정)
    deskewed = deskew(binary)

    # 6️⃣ Morphological Closing (작은 구멍 제거)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    morph = cv2.morphologyEx(deskewed, cv2.MORPH_CLOSE, kernel)


    # 8️⃣ Sharpening (글자 윤곽 강화)
    sharpen_kernel = np.array([[0, -0.5, 0],
                           [-0.5, 3, -0.5],
                           [0, -0.5, 0]])
    sharpened = cv2.filter2D(deskewed, -1, sharpen_kernel)

    # 9️⃣ 저장
    preprocessed_path = image_path.parent / f"preprocessed_{image_path.name}"
    output_path = Path(preprocessed_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 확장자가 없는 경우 기본 jpg로 설정
    if output_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        output_path = output_path.with_suffix(".jpg")

    success = cv2.imwrite(str(output_path), sharpened)
    if not success:
        raise RuntimeError(f"⚠️ 이미지 저장 실패: {output_path}")
    # cv2.imwrite(str(preprocessed_path), sharpened)

    return preprocessed_path
