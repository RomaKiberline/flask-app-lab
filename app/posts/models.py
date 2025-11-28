from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SAEnum
from app import db


class CategoryEnum(str, Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    category = db.Column(SAEnum(CategoryEnum), default=CategoryEnum.other, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    author = db.Column(db.String(20), default='Anonymous', nullable=False)

    def __repr__(self) -> str:
        return f"<Post id={self.id} title='{self.title}'>"
