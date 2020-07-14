class BaseError(Exception):
    def __init__(self, message):
        # 初始化父类
        super().__init__(self)
        self.message = message


class ServiceError(BaseError):
    pass


class ForbiddenError(BaseError):
    pass


class UnauthorizedError(BaseError):
    pass
