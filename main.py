from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models.models import db, User


app = Flask(__name__, template_folder="templates", static_folder="static")
load_dotenv()
CORS(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ocr_project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from routes.health_routes import health_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(health_bp)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(user_id="admin").first():
        admin = User(user_id="admin", email="admin@example.com")
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()
        print("[INFO] 기본 관리자 계정(admin/admin) 생성 완료")


if __name__ == "__main__":
    # gunicorn --bind 0.0.0.0:8000 main:app --daemo
    # :포트번호 .py파일의 이름:flask 객체이름 --deamon
    
    # ps aux | grep gunicorn
    # 실행 중인 gunicorn 보기
    app.run(host="0.0.0.0", port=5000, debug=True)
