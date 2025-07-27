import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# 환경변수에서 DATABASE_URL 읽기
DATABASE_URL = os.getenv('DATABASE_URL')

# SQLAlchemy 인스턴스
db = SQLAlchemy()
