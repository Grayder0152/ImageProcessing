from datetime import datetime

from main import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    task = db.relationship('Task', backref='client', lazy=True, cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"{self.id}"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    upload_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_proc_at = db.Column(db.DateTime, default=datetime.utcnow)
    stop_proc_at = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='cascade'), nullable=False)

    def __repr__(self):
        return f"{self.file_name}"


db.create_all()
