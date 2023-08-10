import datetime
from src.configuration.config import sql


class Notification(sql.Model):
    __tablename__ = 'notifications'
    notification_id: int = sql.Column(sql.Integer, primary_key=True)
    user_id: int = sql.Column(sql.Integer, nullable=True)
    global_notification: bool = sql.Column(sql.Boolean, nullable=False)
    title: str = sql.Column(sql.String(40), nullable=False)
    content: str = sql.Column(sql.String(140), nullable=False)

    def __init__(self, content, title, userId, globalNotification=False):
        self.content = content
        self.title = title
        self.user_id = userId
        self.global_notification = globalNotification

    def toJSON(self, **kvargs):
        obj = {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'global_notification': self.global_notification,
            'title': self.title,
            'content': self.content,
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj