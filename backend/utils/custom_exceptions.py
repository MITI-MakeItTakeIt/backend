from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


class UnactivatedUserDenied(exceptions.PermissionDenied):
    default_detail = _('활성화되지 않은 사용자입니다.')
    default_code = "unactivated_user"
    