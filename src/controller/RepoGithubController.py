from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from src.service.RepoGithubService import RepoGithubService
from src.service.UserService import UserService
from src.utils.Utils import Utils


repoGithub: Blueprint = Blueprint('RepoGithubController', __name__, url_prefix=Utils.getURL('repo-github'))


@repoGithub.route("/<username>/<repo>/issues", methods=['GET'])
@cross_origin()
def getIssues(username, repo):
    return RepoGithubService.getIssues(Utils.getTokenManually(request), request.args.get('page'), username, repo)


@repoGithub.route("/fetch", methods=['GET'])
@cross_origin()
def getRepoGithub():
    return RepoGithubService.get(request.args.get("language"), request.args.get("query"), request.args.get("page"))
