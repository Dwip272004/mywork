from app import db
from datetime import datetime

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    file_path = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Homework {self.name}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactMessage {self.name}>'
"""
flask db migrate -m "Add ContactMessage model"
flask db upgrade

"""