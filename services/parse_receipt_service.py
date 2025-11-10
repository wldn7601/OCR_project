import re
import json

def normalize_text(text: str) -> str:
    """OCR 오탈자 정규화"""
    text = text.replace("O", "0").replace("o", "0")
    text = text.replace("l", "1").replace("I", "1")
    # 모든 종류의 점 문자 제거
    text = re.sub(r"[․·•．｡.]", "", text)
    text = text.replace(" ", "")
    return text



def extract_amounts(ocr_text: str) -> dict:
    """
    OCR로 추출된 영수증 텍스트를 분석해 금액 정보를 JSON 형태로 반환.
    - 총 결제 금액 (total)
    - 결제 수단별 금액 (credit_card, cash)
    - 세부 항목별 금액 (details)
    """

    if not ocr_text or not ocr_text.strip():
        return {"details": {}, "final_total": None, "raw_text": ""}

    # ⚙️ 전체 텍스트 단위 정규화 추가
    normalized_text = normalize_text(ocr_text)

    # 정규식 패턴
    AMOUNT_PATTERN = r"([₩]?\s?\d{1,3}(?:[, ]?\d{3})+|\d{4,})"
    ITEM_LINE_PATTERN = r"([가-힣A-Za-z\s\(\)\d\.\-]+)\s+(\d+)\s+" + AMOUNT_PATTERN
    # TOTAL_KEYWORDS = ["합계", "총액", "총금액", "결제금액", "계", "받을금액", "신용카드", "현금", "카드금액", "합계금액", "받은금액"]

    # 🔽 원본과 정규화본 모두 저장
    lines = [line.strip() for line in normalized_text.splitlines() if line.strip()]

    results = {
        "details": {},
        "final_total": None,
        "raw_text": normalized_text   # ← 정규화된 텍스트 저장
    }

    # 1️⃣ 세부 항목 추출
    for line in lines:
        m = re.search(ITEM_LINE_PATTERN, line)
        if m:
            item_name = m.group(1).strip()
            qty = int(m.group(2))
            amount = m.group(3).replace(",", "")
            results["details"][item_name] = {"qty": qty, "price": int(amount)}

    # 2️⃣ 결제 관련 키워드 탐색 (유연한 정규식 적용 버전)
    total_candidates = []

    # OCR 오탈자까지 포함한 키워드 정규식
    TOTAL_REGEX = re.compile(
        r"(합계|합곗|총액|총금[액앵약역]?|결제금[액앵약역]?|받[을은]?금[액앵약역]?|계|신용카드|현금|카드금액)"
    )

    for line in lines:
        normalized = normalize_text(line)
        if re.search(TOTAL_REGEX, normalized):  # ← 리스트 대신 정규식 매칭
            m = re.search(AMOUNT_PATTERN, normalized)
            if m:
                total_candidates.append(
                    int(
                        m.group(0)
                        .replace(",", "")
                        .replace("₩", "")
                    )
                )



    # 3️⃣ 신용카드 / 현금 금액 구분 (정규화 적용)
    pay_info = {"신용카드": None, "현금": None}
    for line in lines:
        normalized = normalize_text(line)
        if "신용" in normalized and re.search(AMOUNT_PATTERN, normalized):
            pay_info["신용카드"] = int(re.search(AMOUNT_PATTERN, normalized).group(0).replace(",", ""))
        if "현금" in normalized and re.search(AMOUNT_PATTERN, normalized):
            pay_info["현금"] = int(re.search(AMOUNT_PATTERN, normalized).group(0).replace(",", ""))


    # 4️⃣ 최종 합계 결정
    if total_candidates:
        results["final_total"] = max(total_candidates)
    elif pay_info["신용카드"] or pay_info["현금"]:
        total = 0
        if pay_info["신용카드"]:
            total += pay_info["신용카드"]
        if pay_info["현금"]:
            total += pay_info["현금"]
        results["final_total"] = total

    results.update(pay_info)
    return results


# ✅ 테스트용 (직접 실행 시)
if __name__ == "__main__":
    sample_text = """
    이마트 탄현점 128-85-48537
    김치찌개 2 12,000
    공기밥 1 1,000
    합계 13,000
    신용카드 13.000
    """

    parsed = extract_amounts(sample_text)
    print(json.dumps(parsed, ensure_ascii=False, indent=2))


    sample = "받은금역:42․700 / 42．700 / 42.700 / 42·700"
    # sample = "받은금역:42․700"
    print(normalize_text(sample))
    print(extract_amounts(sample))