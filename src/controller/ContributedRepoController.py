from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.RepoGithubService import RepoGithubService
from src.service.ContributedRepoService import ContributedRepoService
from src.utils.Utils import Utils


contributedRepo: Blueprint = Blueprint('ContributedRepoController', __name__, url_prefix=Utils.getURL('contributed-repo'))


@contributedRepo.route("/create", methods=['POST'])
@cross_origin()
def create():
    return ContributedRepoService.create(request.json)


@contributedRepo.route("/user/<userId>", methods=['GET'])
@cross_origin()
def get(userId):
    return ContributedRepoService.get(Utils.getTokenManually(request), userId)