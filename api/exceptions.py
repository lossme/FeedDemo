class ApiBaseException(Exception):
    default_message = "服务异常"
    default_code = 500

    def __init__(self, message=None, code=None):
        super().__init__()
        self._message = message
        self._code = code

    @property
    def code(self):
        return self._code or self.default_code

    @property
    def message(self):
        return self._message or self.default_message

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.message)


class AuthFailed(ApiBaseException):
    default_message = "认证失败"
    default_code = 401


class ParamError(ApiBaseException):
    default_message = "参数错误"
    default_code = 400


class UserNotFound(ApiBaseException):
    default_message = "用户未找到"
    default_code = 404


class UserAlreadyExists(ApiBaseException):
    default_message = "创建失败 用户已存在"
    default_code = 501


class RepoNotFound(ApiBaseException):
    default_message = "仓库未找到"
    default_code = 404


class RepoAlreadyExists(ApiBaseException):
    default_message = "创建失败 仓库已存在"
    default_code = 501
