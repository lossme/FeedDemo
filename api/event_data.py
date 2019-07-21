import json

from . import db
from .models import NewsEvent, User, UserRepo

EVENT_TYPE_FORK = 0
EVENT_TYPE_CREATE_REPO = 1
EVENT_TYPE_STARRED_USER = 2
EVENT_TYPE_STARRED_REPO = 3


class EventDataBase():

    def save(self):
        event = NewsEvent(user_id=self.user_id,
                          event_type=self.event_type,
                          event_data=json.dumps(self.to_dict()))
        db.session.add(event)
        db.session.commit()

    @staticmethod
    def read_repo_info(repo_id):
        repo = db.session.query(UserRepo).filter_by(id=repo_id).first()
        return repo.to_dict()

    @staticmethod
    def read_user_info(user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        return user.to_dict()


class ForkRepoEventData(EventDataBase):
    event_type = EVENT_TYPE_FORK

    def __init__(self, user_id, target_repo_id):
        self.user_id = user_id
        self.target_repo_id = target_repo_id

    def to_dict(self):

        return {
            "user_id": self.user_id,
            "target_repo": self.read_repo_info(repo_id=self.target_repo_id)
        }


class CreateRepoEventData(EventDataBase):
    event_type = EVENT_TYPE_CREATE_REPO

    def __init__(self, user_id, target_repo_id):
        self.user_id = user_id
        self.target_repo_id = target_repo_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "target_repo": self.read_repo_info(repo_id=self.target_repo_id)
        }


class StarredUserEventData(EventDataBase):
    event_type = EVENT_TYPE_STARRED_USER

    def __init__(self, user_id, target_user_id):
        self.user_id = user_id
        self.target_user_id = target_user_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "target_user": self.read_user_info(user_id=self.target_user_id)
        }


class StarredRepoEventData(EventDataBase):
    event_type = EVENT_TYPE_STARRED_REPO

    def __init__(self, user_id, target_repo_id):
        self.user_id = user_id
        self.target_repo_id = target_repo_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "target_repo": self.read_repo_info(repo_id=self.target_repo_id)
        }
