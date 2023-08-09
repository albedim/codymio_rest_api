from sqlalchemy import text

from src.configuration.config import sql
from src.model.entity.User import User


class UserRepository:

    @classmethod
    def signin(cls, email, password) -> User:
        user: User = sql.session.query(User).filter(User.email == email).filter(User.password == password).first()
        return user

    @classmethod
    def signup(cls, avatar, user_github_id, username) -> User:
        user: User = User(avatar, user_github_id, username)
        sql.session.add(user)
        sql.session.commit()
        return user

    @classmethod
    def getUserById(cls, userId) -> User:
        user: User = sql.session.query(User).filter(User.user_id == userId).first()
        return user

    @classmethod
    def getUserByEmail(cls, email) -> User:
        user: User = sql.session.query(User).filter(User.email == email).first()
        return user

    @classmethod
    def getAllUsers(cls) -> list:
        users: list = sql.session.query(User).all()
        return users

    @classmethod
    def createForgottenPasswordToken(cls, user, token) -> None:
        user.password_forget_token = token
        sql.session.commit()

    @classmethod
    def getUserByPasswordForgottenToken(cls, token) -> User:
        user: User = sql.session.query(User).filter(User.password_forget_token == token).first()
        return user

    @classmethod
    def changePassword(cls, userId, password) -> User:
        user: User = cls.getUserById(userId)
        user.password = password
        sql.session.commit()

    @classmethod
    def change(cls, userId, request) -> User:
        user: User = cls.getUserById(userId)
        user.complete_name = request['complete_name']
        user.email = request['email']
        user.password = request['password']
        sql.session.commit()

    @classmethod
    def getUserByUsername(cls, username):
        user = sql.session.query(User).filter(User.username == username).first()
        return user

