# server/src/models.py

from datetime import datetime
from config import db

class Session(db.Model):
    __tablename__ = 'sessions'

    session_id = db.Column(db.String, primary_key=True)
    nickname   = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_or_create(cls, sid, nickname=None):
        """
        세션 ID가 이미 존재하면 해당 객체를 반환하고,
        없으면 새로 생성하여 반환합니다.
        """
    #   obj = cls.query.get(sid)
        obj = db.session.get(cls, sid)
        if not obj:
            obj = cls(session_id=sid, nickname=nickname)
            db.session.add(obj)
            db.session.commit()
        return obj

class FillLog(db.Model):
    __tablename__ = 'fill_logs'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String, db.ForeignKey('sessions.session_id'), nullable=False)
    board_size = db.Column(db.Integer, nullable=False)
    seq        = db.Column(db.Integer, nullable=False)
    row        = db.Column(db.Integer, nullable=False)
    col        = db.Column(db.Integer, nullable=False)
    timestamp  = db.Column(db.DateTime, nullable=False)
