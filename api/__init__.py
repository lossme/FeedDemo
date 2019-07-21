from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
api = Api()


def create_app(config_file):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)

    from .views import HelloApi, UserApi, TokenApi, UsersApi, FollowApi, RepoApi, RepoForkApi, RepoStarApi, FeedApi

    api.add_resource(HelloApi, '/hello')     # GET hello FOR TEST
    api.add_resource(UsersApi, '/users')     # GET 查看所有的用户 FOR TEST

    api.add_resource(UserApi, '/user')       # GET 查询用户信息 POST 创建用户
    api.add_resource(TokenApi, '/token')     # POST 生成 token
    api.add_resource(FollowApi, '/follow')   # GET 查询用户的关注 POST follow 用户
    api.add_resource(RepoApi, '/repo')       # GET 查询用户的repo POST 创建 repo
    api.add_resource(RepoForkApi, '/fork')   # POST fork repo
    api.add_resource(RepoStarApi, '/star')   # POST star repo
    api.add_resource(FeedApi, '/feed')       # GET 查询用户的信息流

    from .exceptions import ApiBaseException

    @api.errorhandler(ApiBaseException)
    def error_handle(e):
        return {"message": e.message}, e.code

    api.init_app(app)

    return app
