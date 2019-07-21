from pprint import pprint
import requests

HOST = "http://127.0.0.1:5000"
TOKEN_URL = HOST + "/token"
CREATE_USER_URL = HOST + "/user"
FOLLOW_USER_URL = HOST + "/follow"
REPO_URL = HOST + "/repo"
FORK_REPO_URL = HOST + "/fork"
STAR_REPO_URL = HOST + "/star"
FEED_URL = HOST + "/feed"


class FeedApi():

    def __init__(self):
        self.session = requests.Session()

    def create_user(self, username, password):
        payload = {"username": username, "password": password}
        response = self.session.post(CREATE_USER_URL, json=payload)
        return response.json()

    def login(self, username, password):
        payload = {"username": username, "password": password}
        response = self.session.post(TOKEN_URL, json=payload)
        data = response.json()
        self.session.headers.setdefault("token", data["token"])

    def follow(self, username):
        payload = {"username": username}
        response = self.session.post(FOLLOW_USER_URL, json=payload)
        return response.json()

    def create_repo(self, repo_name, repo_desc, repo_tags):
        payload = {"repo_name": repo_name, "repo_desc": repo_desc, "repo_tags": repo_tags}
        response = self.session.post(REPO_URL, json=payload)
        return response.json()

    def get_repos(self, user_id=None):
        response = self.session.get(REPO_URL, params={"user_id": user_id})
        return response.json()

    def start_repo(self, repo_id):
        response = self.session.post(STAR_REPO_URL, json={"repo_id": repo_id})
        return response.json()

    def fork_repo(self, repo_id):
        response = self.session.post(FORK_REPO_URL, json={"repo_id": repo_id})
        return response.json()

    def feed(self, page_index=1, page_size=10):
        response = self.session.get(FEED_URL, params={"page_index": page_index, "page_size": page_size})
        return response.json()


def main():
    default_users = [
        ("user1", "123456"),
        ("user2", "123456"),
        ("user3", "123456"),
        ("user4", "123456"),
        ("user5", "123456"),
    ]

    api = FeedApi()

    # 创建用户
    for username, password in default_users:
        api.create_user(username=username, password=password)

    login_user1 = default_users[0]
    login_user2 = default_users[1]

    user1_api = FeedApi()
    user1_api.login(username=login_user1[0], password=login_user1[1])

    user2_api = FeedApi()
    user2_api.login(username=login_user2[0], password=login_user2[1])

    # 关注用户
    for username, _ in default_users:
        user1_api.follow(username=username)
        user2_api.follow(username=username)

    # 创建仓库
    repo_list = {
        ("repo1", "repo_desc", "python"),
        ("repo2", "repo_desc", "python"),
        ("repo3", "repo_desc", "python"),
        ("repo4", "repo_desc", "python"),
    }
    for repo_name, repo_desc, repo_tags in repo_list:
        user1_api.create_repo(repo_name=repo_name, repo_desc=repo_desc, repo_tags=repo_tags)
        user2_api.create_repo(repo_name=repo_name, repo_desc=repo_desc, repo_tags=repo_tags)

    # 查看 repos
    pprint(user1_api.get_repos())
    pprint(user2_api.get_repos())

    # 查看 fedd
    pprint(user1_api.feed(page_index=1, page_size=2))
    pprint(user2_api.feed(page_index=1, page_size=2))


if __name__ == '__main__':
    main()
