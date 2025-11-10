from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import db, User


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    user_id = request.form.get("user_id")
    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(user_id=user_id).first():
        return render_template("index.html", error="이미 존재하는 ID입니다.")

    new_user = User(user_id=user_id, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return render_template("index.html", success="회원가입이 완료되었습니다. 로그인해주세요.")

@auth_bp.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")

    if not user_id or not password:
        return render_template("index.html", error="ID와 비밀번호를 모두 입력해주세요.")

    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        return render_template("index.html", error="존재하지 않는 사용자입니다. 회원가입을 진행해주세요.")
    if not user.check_password(password):
        return render_template("index.html", error="비밀번호가 올바르지 않습니다.")

    session["user_id"] = user_id

    if user_id == "admin":
        return redirect(url_for("admin.admin_page"))
    return redirect(url_for("user.user_page", user_id=user_id))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.index"))
