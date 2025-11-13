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

    # 가상 환경에서 pip install gevent
    # gunicorn에서 멀티 쓰레드 : 기본적으로 sync worker
    # gevent : async로 변경
    # connections : worker가 최대 동시 접속
    # gunicorn --worker-class gevent --worker 3 --worker-connections 1000 --bind 0.0.0.0:8000 main:app

    
    # systemd 서비스 등록
    # Gunicorn을 시스템 서비스로 실행하려면 다음 파일을 생성합니다.
    # $ sudo nano /etc/systemd/system/[원하는 이름].service

    # [[원하는 이름].service]
    # [Unit]
    # Description=Gunicorn Flask Application
    # After=network.target

    # [Service]
    # User=ubuntu
    # Group=ubuntu
    # WorkingDirectory=/home/ubuntu/OCR_Project/myapp
    # Environment="PATH=/home/ubuntu/OCR_Project/venv312/bin"
    # ExecStart=/home/ubuntu/OCR_Project/venv312/bin/gunicorn --worker-class gevent --workers 9 --bind 0.0.0.0:8000 --worker-connections 1000 main:app

    # [Install]
    # WantedBy=multi-user.target


    # ps aux | grep gunicorn
    # 실행 중인 gunicorn 보기

    app.run(host="0.0.0.0", port=5000, debug=True)
