from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from src.service.UserService import UserService
from src.utils.Utils import Utils


user: Blueprint = Blueprint('UserController', __name__, url_prefix=Utils.getURL('user'))


@user.route("/signin", methods=['POST'])
@cross_origin()
def signin():
    return UserService.signin(request.json)


@user.route("/github-access", methods=['POST'])
@cross_origin()
def signup():
    return UserService.githubAccess(request.json)


@user.route("/sync", methods=['GET'])
@cross_origin()
@jwt_required()
def sync():
    return UserService.sync(get_jwt_identity())


