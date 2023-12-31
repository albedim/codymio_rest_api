import random
from datetime import timedelta
from typing import Any

import requests
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.UserRepository import UserRepository
from src.service.ContributionService import ContributionService
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class RepoGithubService:

    GET_REPOS_API_CALL = "https://api.github.com/search/repositories?q=open source {query}" + " language:{language}" + "&page={page}"

    @classmethod
    def get(cls, token, userId, language, query, page):
        auto = language == "all" and query == "all"
        page = random.randint(0, 34) if auto else page

        try:
            res = requests.get(
                cls.GET_REPOS_API_CALL
                .replace("{query}", "" if auto else query)
                .replace("{language}", "" if auto else " language:" + language)
                .replace("{page}", str(page)),
                headers={ "Authorization":  "Bearer " + token })
            res = res.json()['items']
            array = []
            for repo in res:
                if repo['open_issues'] > 0:
                    array.append({
                        'github_repo_id': repo['id'],
                        'forks': repo['forks'],
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'tags': repo['topics'],
                        'contributable': ContributionService.contributable(repo['id'], userId),
                        'open_issues': repo['open_issues'],
                        'description': repo['description'],
                        'language': repo['language']
                    })

            return Utils.createSuccessResponse(True, array)
        except KeyError:
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 415), 415

    @classmethod
    def getIssues(cls, token, page, userId, repoId, repoFullName):
        try:
            res = requests.get("https://api.github.com/repos/" + repoFullName + "/issues?page=" + page,
                               headers={"Authorization": "Bearer " + token})
            res = res.json()

            array = []
            for issue in res:
                if len(issue['assignees']) == 0:
                    array.append({
                        'issue_id': issue['id'],
                        'number': issue['number'],
                        'title': issue['title'],
                        'has_contributed': ContributionService.hasContributed(issue['id'], repoId, userId),
                        'creator_username': issue['user']['login'],
                        'body': issue['body'],
                        'has_pull_requests': cls.hasPullRequests(issue),
                        'created_on': issue['created_at']
                    })

            return Utils.createSuccessResponse(True, sorted(array, key=cls.orderByHasPullRequests))
        except TypeError:
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 400), 400

    @classmethod
    def orderByHasPullRequests(cls, array):
        if array['has_pull_requests']:
            return 1
        return 0

    @classmethod
    def hasPullRequests(cls, issue):
        return "pull_request" in issue
