from sqlalchemy import Column, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from passlib.apps import custom_app_context as pwd_context

from . import db


class NewsEvent(db.Model):
    __tablename__ = 'news_event'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    event_type = Column(TINYINT(4), nullable=False)
    event_data = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def to_dict(self):
        return {
            "event_id": self.id,
            "user_id": self.user_id,
            "event_data": self.event_data,
            "event_type": self.event_type,
            "create_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class UserFollow(db.Model):
    __tablename__ = 'user_follow'
    __table_args__ = (
        Index('follow_unique', 'user_id', 'follow_user_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    follow_user_id = Column(INTEGER(11), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class User(db.Model):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(40), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    @staticmethod
    def hash_password(password):
        password_hash = pwd_context.encrypt(password)
        return password_hash

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def to_dict(self):
        return {
            "user_id": self.id,
            "username": self.username,
        }


class UserRepo(db.Model):
    __tablename__ = 'user_repo'
    __table_args__ = (
        Index('repo_unique', 'user_id', 'repo_name', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    repo_name = Column(String(40), nullable=False)
    repo_desc = Column(String(128), nullable=False)
    repo_tags = Column(String(1024), nullable=False)
    repo_type = Column(TINYINT(4), nullable=False)
    origin_repo_id = Column(INTEGER(11), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    REPO_TYPE_CREATE = 0
    REPO_TYPE_FORK = 1

    def to_dict(self):
        return {
            "repo_id": self.id,
            "user_id": self.user_id,
            "repo_name": self.repo_name,
            "repo_desc": self.repo_desc,
            "repo_tags": self.repo_tags,
            "repo_type": ["create", "fork"][self.repo_type],
            "origin_repo_id": self.origin_repo_id,
            "create_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class RepoFork(db.Model):
    __tablename__ = 'repo_fork'
    __table_args__ = (
        Index('fork_unique', 'user_id', 'repo_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    repo_id = Column(INTEGER(11), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class RepoStar(db.Model):
    __tablename__ = 'repo_star'
    __table_args__ = (
        Index('star_unique', 'user_id', 'repo_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    repo_id = Column(INTEGER(11), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
