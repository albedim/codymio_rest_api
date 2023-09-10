from datetime import timedelta
from typing import Any

import requests
from flask_jwt_extended import create_access_token
from src.model.entity.User import User
from src.model.repository.UserRepository import UserRepository
from src.service.NotificationService import NotificationService
from src.utils.Constants import Constants
from src.utils.Utils import Utils


class UserService:

    @classmethod
    def signin(cls, request: dict) -> tuple[Any, int] | Any:

        if not Utils.isValid(request, "SIGNIN_USER"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                415
            ), 415

        user: User = UserRepository.signin(
            request['email'],
            Utils.hash(request['password'])
        )

        if user is not None:
            return Utils.createSuccessResponse(True, {
                "token": create_access_token(
                    identity=user.toJson(),
                    expires_delta=timedelta(days=7))
            })
        else:
            return Utils.createWrongResponse(False, Constants.USER_NOT_FOUND, 404), 404

    @classmethod
    def existsByEmail(cls, email) -> bool:
        return UserRepository.getUserByEmail(email) is not None

    @classmethod
    def getUserById(cls, userId):
        user: User = UserRepository.getUserById(userId)
        if user is None:
            return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404
        else:
            return user.toJSON()

    @classmethod
    def githubAccess(cls, request: dict):

        if not Utils.isValid(request, "GITHUB_ACCESS"):
            return Utils.createWrongResponse(
                False,
                Constants.INVALID_REQUEST,
                415
            ), 415

        r = cls.getEntityFromCode(request)

        if r is None:
            return Utils.createWrongResponse(False, Constants.NOT_FOUND, 404), 404

        user = r['entity']
        githubToken = r['github_token']

        requestUser = UserRepository.getUserByUsername(user['login'])
        if requestUser is not None:
            NotificationService.create(
                Constants.WELCOME_NOTIFICATION['content'],
                Constants.WELCOME_NOTIFICATION['title'].replace("{username}", requestUser.username),
                requestUser.user_id,
                removable=False
            )
            return Utils.createSuccessResponse(True, {
                'token': create_access_token(identity=requestUser.toJSON(),
                                             expires_delta=timedelta(days=7)),
                'github_token': githubToken
            })

        createdUser = UserRepository.signup(user['avatar_url'], user['id'], user['login'])
        NotificationService.create(
            Constants.WELCOME_NOTIFICATION['content'],
            Constants.WELCOME_NOTIFICATION['title'].replace("{username}", createdUser.username),
            createdUser.user_id,
            removable=False
        )
        return Utils.createSuccessResponse(True, {
            'token': create_access_token(identity=createdUser.toJSON(),
                                         expires_delta=timedelta(days=7)),
            'github_token': githubToken
        })

    @classmethod
    def getEntityFromCode(cls, request):
        res = requests.post("https://github.com/login/oauth/access_token", json={
            'code': request['code'],
            'client_id': "38839c37d7a53b00e9dc",
            'client_secret': "c6f4cfd12e86c182542967732e03dccdd89aafdf"
        })
        if res.text.split("=")[1].split("&")[0] == 'bad_verification_code':
            return None
        user = requests.get("https://api.github.com/user", headers={"Authorization": "Bearer "+res.text.split("=")[1].split("&")[0]})
        return {
            'entity': user.json(),
            'github_token': res.text.split("=")[1].split("&")[0]
        }

    @classmethod
    def changePassword(cls, request) -> tuple[Any, int] | dict:

        if not Utils.isValid(request, "CHANGE_PASSWORD"):
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 415), 415

        UserRepository.changePassword(request['user_id'], Utils.hash(request['new_password']))
        return Utils.createSuccessResponse(True, Constants.CREATED)

    @classmethod
    def change(cls, userId, request) -> tuple[Any, int] | dict:

        if not Utils.isValid(request, "CHANGE"):
            return Utils.createWrongResponse(False, Constants.INVALID_REQUEST, 415), 415

        UserRepository.change(userId, request)
        return Utils.createSuccessResponse(True, {
                "token": create_access_token(
                    identity=UserRepository.getUserById(userId).toJson(),
                    expires_delta=timedelta(days=7))
            })

    @classmethod
    def sync(cls, requestUser):
        user = UserRepository.getUserById(requestUser['user_id']).toJSON()
        if user == requestUser:
            return Utils.createSuccessResponse(True, Constants.UP_TO_DATE)
        else:
            return Utils.createSuccessResponse(False, {
                "token": create_access_token(identity=user.toJSON(),
                                             expires_delta=timedelta(days=7)),
                "github_token": create_access_token(identity=user.toJSON(),
                                             expires_delta=timedelta(days=7))
            })
