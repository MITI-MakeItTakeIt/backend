from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int

import six


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)
    
    def check_token(self, user, token):

        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return False

        if (self._num_seconds(self._now()) - ts) > settings.USER_ACTIVATION_EMAIL_TIMEOUT:
            return False
                
        return True


user_activation_token = UserActivationTokenGenerator()
