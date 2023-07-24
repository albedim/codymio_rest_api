from flask_jwt_extended import JWTManager

from src.configuration.config import app, sql
from src.controller import UserController, RepoGithubController, ServerController

# controllers init
app.register_blueprint(RepoGithubController.repoGithub)
app.register_blueprint(UserController.user)
app.register_blueprint(ServerController.server)

# modules init
JWTManager(app)


def create_app():
    with app.app_context():
        sql.create_all()
    return app


if __name__ == '__main__':
    create_app().run()