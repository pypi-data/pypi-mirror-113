class InvalidAuthKey(Exception):
    pass

class DefaultStoreTypeError(Exception):
    pass

class LangsTypeError(Exception):
    pass

class TestsTypeError(Exception):
    pass

class TextTypeError(Exception):
    pass

class SubAttributesTypeError(Exception):
    pass

class NotValidTest(Exception):
    pass

class ApiException(Exception):
    pass

class RateLimiterTypeError(Exception):
    pass

class RateLimited(Exception):
    def __init__(self,**kwargs):
        self.raw_data = kwargs.get("raw_data")
    pass
