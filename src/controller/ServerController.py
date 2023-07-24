from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.ServerService import ServerService
from src.service.UserService import UserService
from src.utils.Utils import Utils


server: Blueprint = Blueprint('ServerController', __name__, url_prefix=Utils.getURL('server'))


@server.route("/languages", methods=['GET'])
@cross_origin()
def getLanguages():
    return ServerService.getLanguages()
