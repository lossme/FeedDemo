import functools

from flask import request, g, current_app
from flask_restplus import Resource
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from . import db
from .models import User, UserFollow, UserRepo, RepoStar, RepoFork, NewsEvent
from .exceptions import UserNotFound, UserAlreadyExists, ParamError, AuthFailed, RepoNotFound, RepoAlreadyExists
from .event_data import CreateRepoEventData, StarredRepoEventData, StarredUserEventData, ForkRepoEventData


class HelloApi(Resource):

    def get(self):
        return "hello world"


def login_reuqired(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            raise ParamError("token为空")
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            raise AuthFailed("认证失败: token已过期")
        except BadSignature:
            raise AuthFailed("认证失败: 无效token")
        user = User.query.get(data['user_id'])
        g.user = user
        return func(*args, **kwargs)
    return wrapper


class UserApi(Resource):

    def get(self):
        # show userinfo
        username = request.args.get("username")
        if not username:
            raise UserNotFound()
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            raise UserNotFound()
        return user.to_dict()

    def post(self):
        # craete user
        username = request.json.get('username')
        password = request.json.get('password')
        if not username or not password:
            raise ParamError("参数错误. 用户名或密码为空")

        user = db.session.query(User).filter_by(username=username).first()
        if user:
            raise UserAlreadyExists()

        password_hash = User.hash_password(password)
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()


class TokenApi(Resource):

    def post(self):
        # generate_auth_token
        username = request.json.get('username')
        password = request.json.get('password')
        user = db.session.query(User).filter_by(username=username).first()
        if not user or not user.verify_password(password):
            raise AuthFailed()
        expiration = 3600 * 24 * 30
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = s.dumps({'user_id': user.id}).decode()
        return {"token": token}


class UsersApi(Resource):

    def get(self):
        # 列出用户
        page_size = request.args.get("page_size", 10, int)
        page_index = request.args.get("page_index", 1, int)
        rows = db.session.query(User).slice((page_index - 1) * page_size, page_index * page_size)
        return [row.to_dict() for row in rows]


class FollowApi(Resource):

    @login_reuqired
    def get(self):
        # 查看我关注了谁
        user_id = g.user.id
        rows = db.session.query(UserFollow, User)\
            .filter(UserFollow.user_id == user_id)\
            .filter(UserFollow.follow_user_id == User.id).all()

        return {
            "user_id": user_id,
            "follows": [
                {
                    "user_id": user_folow.follow_user_id,
                    "username": user.username
                }
                for user_folow, user in rows]
        }

    @login_reuqired
    def post(self):
        # follow user
        follow_username = request.json.get("username")
        follow_user = db.session.query(User).filter_by(username=follow_username).first()
        if not follow_user:
            raise UserNotFound()

        user_id = g.user.id
        follow_user_id = follow_user.id
        if user_id == follow_user_id:
            raise ParamError("不能关注自己")

        r = db.session.query(UserFollow).filter_by(user_id=user_id, follow_user_id=follow_user_id).first()
        if r:
            return {
                "message": "该用户已关注"
            }

        row = UserFollow(user_id=user_id, follow_user_id=follow_user.id)
        db.session.add(row)
        db.session.commit()

        # 往活动消息表插入一条记录
        StarredUserEventData(user_id=user_id, target_user_id=follow_user.id).save()

        return {
            "message": "关注成功"
        }


class RepoApi(Resource):

    @login_reuqired
    def get(self):
        # 查看 user_id 下所有repo
        user_id = request.args.get("user_id", type=int) or g.user.id

        repos = db.session.query(UserRepo).filter_by(user_id=user_id).all()
        return [repo.to_dict() for repo in repos]

    @login_reuqired
    def post(self):
        # create repo
        user_id = g.user.id
        repo_name = request.json.get("repo_name")
        repo_desc = request.json.get("repo_desc")
        repo_tags = request.json.get("repo_tags")
        repo_type = UserRepo.REPO_TYPE_CREATE

        repo = db.session.query(UserRepo).filter_by(user_id=user_id, repo_name=repo_name).first()
        if repo:
            raise RepoAlreadyExists()

        repo = UserRepo(user_id=user_id, repo_name=repo_name, repo_desc=repo_desc,
                        repo_tags=repo_tags, repo_type=repo_type)
        db.session.add(repo)
        db.session.commit()

        # 往活动消息表插入一条记录
        CreateRepoEventData(user_id=user_id, target_repo_id=repo.id).save()

        return {
            "message": "仓库创建成功"
        }


class RepoForkApi(Resource):

    @login_reuqired
    def post(self):
        # fork repo
        user_id = g.user.id
        repo_id = request.json.get("repo_id")
        repo = db.session.query(UserRepo).filter_by(id=repo_id).first()
        if not repo:
            raise RepoNotFound()

        repo_fork = db.session.query(RepoFork).filter_by(user_id=user_id, repo_id=repo.id).first()
        if repo_fork:
            return {
                "message": "已fork"
            }

        repo_fork = RepoFork(user_id=user_id, repo_id=repo.id)
        db.session.add(repo_fork)
        db.session.commit()

        # 往活动消息表插入一条记录
        ForkRepoEventData(user_id=user_id, target_repo_id=repo_fork.id).save()

        return {
            "message": "fork成功"
        }


class RepoStarApi(Resource):

    @login_reuqired
    def post(self):
        # star repo
        user_id = g.user.id
        repo_id = request.json.get("repo_id")

        repo = db.session.query(UserRepo).filter_by(id=repo_id).first()
        if not repo:
            raise RepoNotFound()

        repo_star = db.session.query(RepoStar).filter_by(user_id=user_id, repo_id=repo.id).first()
        if repo_star:
            return {
                "message": "已star"
            }

        repo_star = RepoStar(user_id=user_id, repo_id=repo.id)
        db.session.add(repo_star)
        db.session.commit()

        # 往活动消息表插入一条记录
        StarredRepoEventData(user_id=user_id, target_repo_id=repo_star.id).save()

        return {
            "message": "star成功"
        }


class FeedApi(Resource):

    @login_reuqired
    def get(self):
        # 查询feed
        user_id = g.user.id

        # 找出我关注的所有用户
        follow_list = db.session.query(UserFollow).filter_by(user_id=user_id).all()
        follow_user_id_list = [follow.follow_user_id for follow in follow_list]

        # 查看这些用户最近有什么活动消息
        page_size = request.args.get("page_size", 10, int)
        page_index = request.args.get("page_index", 1, int)
        rows = db.session.query(NewsEvent)\
            .filter(NewsEvent.user_id.in_(follow_user_id_list))\
            .order_by(NewsEvent.created_at.desc())\
            .slice((page_index - 1) * page_size, page_index * page_size)
        return [row.to_dict() for row in rows]
