from rest_framework.exceptions import ValidationError

from users.serializers import UserInfoCheckSerializer

class UserInfoCheckResponse:
    _serializer_class = UserInfoCheckSerializer
    _valid_fields = {
        'email': '이메일',
        'nickname': '닉네임'
    }
    _MESSAGE = {
        "valid": "사용 가능한 %s입니다",
        "unique": "사용중인 %s입니다.",
        "invalid": "유효하지 않은 %s입니다.",
        "blank": "유효하지 않은 %s입니다.",
        "null": "유효하지 않은 %s입니다."
    }
    
    def __init__(self, data):
        if not set(data.keys()).intersection(set(self._valid_fields.keys())):
            raise ValidationError()
        self._data = data
        
    def is_valid(self):
        _serializer = self._serializer_class(data=self._data)
        _serializer.is_valid()
        self.to_response(_serializer)

    def to_response(self, serializer):
        if serializer.errors:
            is_available = 0
            field = list(serializer.errors.keys())[0]
            code = serializer.errors[field][0].code
            message = self._MESSAGE[code]%self._valid_fields[field]
        else:
            is_available = 1
            field = list(serializer.data.keys())[0]
            message = self._MESSAGE['valid']%self._valid_fields[field]
        
        self._response = {
            "is_availble": is_available,
            "message": message
        }

    @property
    def response(self):
        if not hasattr(self, '_response'):
            msg = ".is_valid()를 먼저 호출해야 합니다."
            raise AssertionError(msg)
        return self._response