import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# ✅ .env 로드
load_dotenv()
OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY")

def ocr_space_api(image_path: Path, api_key: str = None, language: str = "kor") -> str:
    """
    OCR.space API를 이용해 이미지를 텍스트로 변환합니다.
    - image_path: 입력 이미지 경로 (Path)
    - api_key: OCR.space API 키 (기본값은 .env에서 읽음)
    - language: OCR 언어 코드 ('kor', 'eng' 등)
    """
    url_api = "https://api.ocr.space/parse/image"
    api_key = api_key or OCR_SPACE_API_KEY

    if not api_key:
        raise ValueError("OCR_SPACE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    if not image_path.exists():
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")

    try:
        with open(image_path, "rb") as f:
            response = requests.post(
                url_api,
                files={"filename": f},
                data={
                    "apikey": api_key,
                    "language": language,
                    "isOverlayRequired": False,
                    "isTable": True,              # 표 형태 인식 강화
                    "scale": True,
                    "detectOrientation": True,     # 회전 보정
                    "OCREngine": 2,                # 최신 엔진
                },
                timeout=60,
            )

        if response.status_code != 200:
            print(f"[ERROR] OCR.space 응답 코드: {response.status_code}")
            return ""

        try:
            result = response.json()
        except json.JSONDecodeError:
            print("[ERROR] OCR.space 응답을 JSON으로 파싱할 수 없습니다.")
            return ""

        parsed = result.get("ParsedResults")
        if not parsed:
            print("[WARN] OCR.space 결과가 비어 있습니다:", result)
            return ""

        text_detected = parsed[0].get("ParsedText", "").strip()
        return text_detected

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] OCR.space 요청 실패: {e}")
        return ""


def ocr_space_api_json(image_path: Path, api_key: str = None, language: str = "kor") -> dict:
    """
    OCR.space API 결과를 JSON 형태로 정리해 반환.
    {
        "lines": ["이마트 탄현점 ...", "대표: 최병렬", ...],
        "raw_text": "이마트 탄현점 128-85-48537 대표: 최병렬..."
    }
    """
    text = ocr_space_api(image_path, api_key, language)

    if not text:
        return {"lines": [], "raw_text": ""}

    # ✅ 줄 단위로 분리 후 공백 제거
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    
    return {
        "lines": lines,
        "raw_text": text
    }
