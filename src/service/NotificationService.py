import requests

from src.model.entity.Contribution import Contribution
from src.model.repository.NotificationRepository import NotificationRepository
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils
from src.model.repository.ContributionRepository import ContributionRepository


class NotificationService:

    @classmethod
    def create(cls, content, title, userId=0, globalNotification=False, removable=True):
        NotificationRepository.create(
            content,
            title,
            userId,
            globalNotification,
            removable
        )

    @classmethod
    def remove(cls, notificationId):
        notification = NotificationRepository.remove(notificationId)
        return cls.get(notification.user_id)

    @classmethod
    def get(cls, userId):

        notifications = NotificationRepository.get(userId)
        res = []

        for notification in notifications:
            res.append(notification.toJSON())

        return Utils.createSuccessResponse(True, res)


