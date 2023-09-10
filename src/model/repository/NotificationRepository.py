from sqlalchemy import desc

from src.configuration.config import sql
from src.model.entity.Contribution import Contribution
from src.model.entity.Notification import Notification


class NotificationRepository:

    @classmethod
    def create(cls, content, title, userId, globalNotification, removable):
        notification = Notification(content, title, userId, globalNotification, removable)
        sql.session.add(notification)
        sql.session.commit()
        return notification

    @classmethod
    def remove(cls, notificationId):
        notification = sql.session.query(Notification).filter(Notification.notification_id == notificationId).first()
        sql.session.delete(notification)
        sql.session.commit()
        return notification

    @classmethod
    def get(cls, userId):
        notifications = sql.session.query(Notification)\
            .filter(Notification.user_id == userId).order_by(desc(Notification.notification_id)).all()
        return notifications

    @classmethod
    def getGlobal(cls):
        notifications = sql.session.query(Notification)\
            .filter(Notification.global_notification == True).all()
        return notifications