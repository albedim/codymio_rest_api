import datetime
from src.configuration.config import sql


class Notification(sql.Model):
    __tablename__ = 'notifications'
    notification_id: int = sql.Column(sql.Integer, primary_key=True)
    created_on: datetime.date = sql.Column(sql.Date, nullable=False)
    user_id: int = sql.Column(sql.Integer, nullable=True)
    global_notification: bool = sql.Column(sql.Boolean, nullable=False)
    title: str = sql.Column(sql.String(40), nullable=False)
    removable: bool = sql.Column(sql.Boolean, nullable=False)
    content: str = sql.Column(sql.String(140), nullable=False)

    def __init__(self, content, title, userId, globalNotification, removable):
        self.content = content
        self.created_on = datetime.date.today()
        self.title = title
        self.removable = removable
        self.user_id = userId
        self.global_notification = globalNotification

    def toJSON(self, **kvargs):
        obj = {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'global_notification': self.global_notification,
            'title': self.title,
            'created_on': str(self.created_on),
            'content': self.content,
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj