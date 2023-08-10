from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.NotificationService import NotificationService
from src.service.RepoGithubService import RepoGithubService
from src.service.UserService import UserService
from src.utils.Utils import Utils


notification: Blueprint = Blueprint('NotificationController', __name__, url_prefix=Utils.getURL('notifications'))


@notification.route("/user/<userId>", methods=['GET'])
@cross_origin()
def get(userId):
    return NotificationService.get(userId)


@notification.route("/<notificationId>", methods=['DELETE'])
@cross_origin()
def remove(notificationId):
    return NotificationService.remove(notificationId)
