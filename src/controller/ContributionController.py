from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.RepoGithubService import RepoGithubService
from src.service.ContributionService import ContributionService
from src.utils.Utils import Utils


contribution: Blueprint = Blueprint('ContributionController', __name__, url_prefix=Utils.getURL('contributions'))


@contribution.route("/create", methods=['POST'])
@cross_origin()
def create():
    return ContributionService.create(request.json)


@contribution.route("/<contributedRepoId>", methods=['DELETE'])
@cross_origin()
def remove(contributedRepoId):
    return ContributionService.remove(contributedRepoId)


@contribution.route("/seen", methods=['POST'])
@cross_origin()
def seen():
    return ContributionService.setSeen(request.json)


@contribution.route("/user/<userId>", methods=['GET'])
@cross_origin()
def get(userId):
    return ContributionService.get(Utils.getTokenManually(request), userId)