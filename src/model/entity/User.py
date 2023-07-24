import datetime
from src.configuration.config import sql


class User(sql.Model):
    __tablename__ = 'users'
    user_id: int = sql.Column(sql.Integer, primary_key=True)
    user_github_id: int = sql.Column(sql.Integer, nullable=False)
    username: str = sql.Column(sql.String(40), nullable=False)
    name: datetime.date = sql.Column(sql.String(40), nullable=False)
    bio = sql.Column(sql.String(240), nullable=False)
    avatar = sql.Column(sql.String(74), nullable=False)

    def __init__(self, avatar, bio, user_github_id, username, name):
        self.avatar = avatar
        self.bio = bio
        self.user_github_id = user_github_id
        self.username = username
        self.name = name

    def toJSON(self, **kvargs):
        obj = {
            'user_id': self.user_id,
            'user_github_id': self.user_github_id,
            'username': self.username,
            'name': self.name,
            'bio': self.bio,
            'avatar': self.avatar
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj