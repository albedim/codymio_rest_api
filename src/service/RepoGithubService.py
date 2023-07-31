import random
from datetime import timedelta
from typing import Any

import requests
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.UserRepository import UserRepository
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class RepoGithubService:

    @classmethod
    def get(cls, language, query, page):
        auto = language == "all" and query == "all"
        page = random.randint(0, 34) if auto else page
        print(page)
        try:
            res = requests.get("https://api.github.com/search/repositories?q=open source " +
                               ("" if auto else query) +
                               ("" if auto else "language:" + language) + "&page=" + str(page))
            res = res.json()['items']
            array = []
            for repo in res:
                if repo['has_issues']:
                    array.append({
                        'github_repo_id': repo['id'],
                        'forks': repo['forks'],
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'tags': repo['topics'],
                        'open_issues': repo['open_issues'],
                        'description': repo['description'],
                        'language': repo['language']
                    })

            return Utils.createSuccessResponse(True, array)
        except KeyError:
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 415), 415

    @classmethod
    def getIssues(cls, token, page, username, repo):
        res = requests.get("https://api.github.com/repos/" + username + "/" + repo + "/issues?page=" + page,
                           headers={"Authorization": "Bearer " + token})
        res = res.json()

        array = []

        for issue in res:
            array.append({
                'issue_id': issue['id'],
                'number': issue['number'],
                'title': issue['title'],
                'creator_username': issue['user']['login'],
                'body': issue['body'],
                'created_on': issue['created_at']
            })

        return Utils.createSuccessResponse(True, array)
