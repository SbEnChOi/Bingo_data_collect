# server/src/app.py

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from config import db
from models import Session, FillLog
from datetime import datetime

# .env 로드
load_dotenv()

# SQLite 파일 경로에서 디렉터리 자동 생성
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('sqlite:///'):
    # 데이터를 저장할 파일 경로에서 'sqlite:///' 접두사를 제거
    db_path = DATABASE_URL.replace('sqlite:///', '')
    # 디렉터리 경로만 추출
    folder = os.path.dirname(db_path)
    # 디렉터리가 없으면 생성
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# Flask 앱 초기화 (static 및 templates 폴더 지정)
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
CORS(app)

# DB 설정
app.config['SQLALCHEMY_DATABASE_URI']        = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 테이블 생성
with app.app_context():
    db.create_all()

# UI 라우트: index.html 렌더링
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# API 라우트: 클릭 로그 저장
@app.route('/api/fill', methods=['POST'])
def log_fill():
    data = request.get_json()

    # 세션 조회 또는 생성
    Session.get_or_create(data['session_id'], data.get('nickname'))

    # timestamp 문자열을 Python datetime 객체로 변환
    ts_str = data.get('timestamp', '')
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1]
    timestamp = datetime.fromisoformat(ts_str)

    # 로그 저장
    log = FillLog(
        session_id=data['session_id'],
        board_size=data['board_size'],
        seq=data['seq'],
        row=data['row'],
        col=data['col'],
        timestamp=timestamp
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'status': 'ok'}), 201

# 정적 파일 서빙 (필요시)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=True
    )
