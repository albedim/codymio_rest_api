from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.RepoGithubService import RepoGithubService
from src.service.UserService import UserService
from src.utils.Utils import Utils


repoGithub: Blueprint = Blueprint('RepoGithubController', __name__, url_prefix=Utils.getURL('repositories'))


@repoGithub.route("/<repoId>/issues", methods=['GET'])
@cross_origin()
def getIssues(repoId):
    return RepoGithubService.getIssues(Utils.getTokenManually(request), request.args.get("page"), request.args.get("user_id"), repoId, request.args.get("repo_full_name"),)


@repoGithub.route("/fetch", methods=['GET'])
@cross_origin()
@jwt_required()
def getRepoGithub():
    return RepoGithubService.get(get_jwt_identity()['user_id'], request.args.get("language"), request.args.get("query"), request.args.get("page"))
