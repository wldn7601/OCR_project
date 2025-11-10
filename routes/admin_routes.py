from flask import Blueprint, render_template, redirect, url_for, session
from models.models import db, User
from pathlib import Path
import shutil

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ✅ 이미지 및 결과 폴더의 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "images"
RESULTS_DIR = BASE_DIR / "results"


@admin_bp.route("/")
def admin_page():
    if "user_id" not in session or session["user_id"] != "admin":
        return redirect(url_for("auth.index"))

    users = User.query.filter(User.user_id != "admin").all()
    return render_template("admin_home.html", users=users)


@admin_bp.route("/delete_user/<string:user_id>", methods=["POST"])
def delete_user(user_id):
    """유저 삭제 + 해당 유저의 이미지 / 결과 폴더 삭제"""
    if "user_id" not in session or session["user_id"] != "admin":
        return redirect(url_for("auth.index"))

    user = User.query.filter_by(user_id=user_id).first()
    message = ""

    if user:
        # ✅ 1️⃣ DB에서 유저 삭제
        db.session.delete(user)
        db.session.commit()

        # ✅ 2️⃣ 유저의 폴더 삭제
        user_image_dir = IMAGES_DIR / user_id
        user_result_dir = RESULTS_DIR / user_id

        for folder in [user_image_dir, user_result_dir]:
            if folder.exists():
                try:
                    shutil.rmtree(folder)
                    print(f"[INFO] Deleted folder: {folder}")
                except Exception as e:
                    print(f"[ERROR] Failed to delete {folder}: {e}")

        message = f"{user_id} 계정과 관련된 모든 데이터가 삭제되었습니다."
    else:
        message = "존재하지 않는 사용자입니다."

    users = User.query.filter(User.user_id != "admin").all()
    return render_template("admin_home.html", users=users, success=message)
