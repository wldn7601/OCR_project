from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, abort, jsonify, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import json
import shutil
from services.preprocess_service import preprocess_image
from services.ocrspace_service import ocr_space_api_json
from services.parse_receipt_service import extract_amounts, normalize_text


user_bp = Blueprint("user", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
RESULTS_DIR = BASE_DIR / "results"


def allowed_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@user_bp.route("/<user_id>", methods=["GET", "POST"])
def user_page(user_id):
    # 관리자(admin)는 모든 유저 페이지 접근 허용
    if session["user_id"] != user_id and session["user_id"] != "admin":
        flash("접근 권한이 없습니다.")
        return redirect(url_for("auth.index"))

    # ✅ 디렉토리 구성 (분리형)
    base_dir = IMAGES_DIR / user_id
    original_dir = base_dir / "original"
    pre_dir = base_dir / "preprocessed"
    result_root = RESULTS_DIR / user_id

    for d in [original_dir, pre_dir, result_root]:
        d.mkdir(parents=True, exist_ok=True)

    # ===============================
    # 업로드 POST 처리
    # ===============================
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("파일을 선택해주세요.")
            return redirect(url_for("user.user_page", user_id=user_id))

        filename = secure_filename(file.filename)

        # ✅ 1. 원본 이미지 저장
        original_path = original_dir / filename
        file.save(original_path)

        # ✅ 2. 전처리 후 저장
        preprocessed_path = pre_dir / filename
        pre_result = preprocess_image(original_path)
        pre_result.rename(preprocessed_path)

        # ✅ 3. OCR.space 적용
        ocr_result = ocr_space_api_json(preprocessed_path)
        ocr_text = normalize_text(ocr_result.get("raw_text", ""))
        ocr_result["raw_text"] = ocr_text

        # ✅ JSON 전체 구조 정규화
        def normalize_json(obj):
            if isinstance(obj, dict):
                return {k: normalize_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [normalize_json(v) for v in obj]
            elif isinstance(obj, str):
                return normalize_text(obj)
            else:
                return obj

        ocr_result = normalize_json(ocr_result)

        # ✅ 4. 결과 폴더 생성
        image_stem = Path(filename).stem
        result_folder = result_root / image_stem
        result_folder.mkdir(parents=True, exist_ok=True)

        # ✅ 5. OCR 결과 저장
        with open(result_folder / "ocr_text.txt", "w", encoding="utf-8") as f:
            f.write(ocr_text.strip())

        with open(result_folder / "all.json", "w", encoding="utf-8") as f:
            json.dump(ocr_result, f, ensure_ascii=False, indent=2)

        # ✅ 6. 금액 파싱
        parsed_data = extract_amounts(ocr_text)
        with open(result_folder / "result.json", "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)

        flash(f"{filename} OCR 완료 — 결과 저장 및 시각화 생성 완료.")
        return redirect(url_for("user.user_page", user_id=user_id))

    # ===============================
    # GET — 유저 이미지 목록
    # ===============================
    image_info_list = []
    total_spent = 0

    for img_path in sorted(original_dir.glob("*")):
        if img_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            image_stem = img_path.stem
            result_json = result_root / image_stem / "result.json"
            total_amount = None
            if result_json.exists():
                try:
                    with open(result_json, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        total_amount = data.get("final_total")
                        if isinstance(total_amount, (int, float)):
                            total_spent += total_amount
                except Exception:
                    pass
            image_info_list.append({
                "name": img_path.name,
                "total": total_amount
            })

    return render_template(
        "user_home.html",
        user_id=user_id,
        image_info_list=image_info_list,
        total_spent=total_spent
    )




@user_bp.route("/<user_id>/<filename>")
def image_detail(user_id, filename):
    image_path = IMAGES_DIR / user_id / filename
    result_folder = RESULTS_DIR / user_id / Path(filename).stem
    all_json_path = result_folder / "all.json"
    result_json_path = result_folder / "result.json"

    all_json_str = None
    result_json_str = None
    final_total = None

    # all.json
    if all_json_path.exists():
        with open(all_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_json_str = json.dumps(data, ensure_ascii=False, indent=2)

    # result.json
    if result_json_path.exists():
        with open(result_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            result_json_str = json.dumps(data, ensure_ascii=False, indent=2)
            final_total = data.get("final_total")

    return render_template(
        "image_detail.html",
        user_id=user_id,
        filename=filename,
        all_json_str=all_json_str,
        result_json_str=result_json_str,
        final_total=final_total
    )

@user_bp.route("/<user_id>/delete/<filename>", methods=["POST"])
def delete_image(user_id, filename):
    """특정 이미지 및 관련 데이터 삭제"""
    if "user_id" not in session or session["user_id"] != user_id:
        return jsonify({"success": False, "message": "로그인이 필요합니다."}), 403

    base_dir = IMAGES_DIR / user_id
    original_path = base_dir / "original" / filename
    preprocessed_path = base_dir / "preprocessed" / filename
    result_folder = RESULTS_DIR / user_id / Path(filename).stem

    deleted = []
    for path in [original_path, preprocessed_path]:
        if path.exists():
            path.unlink()
            deleted.append(str(path))

    if result_folder.exists():
        shutil.rmtree(result_folder)
        deleted.append(str(result_folder))

    print(f"[INFO] Deleted files/folders for {filename}: {deleted}")
    return jsonify({"success": True, "message": f"{filename} 삭제 완료."})

@user_bp.route("/<user_id>/<category>/<filename>")
def serve_user_image(user_id, category, filename):
    if category not in ("original", "preprocessed"):
        abort(404)
    path = IMAGES_DIR / user_id / category / filename
    if not path.exists():
        abort(404)
    return send_file(path)
