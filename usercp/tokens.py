from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    """it will generate a token that inharitance from django PasswordResetTokenGenerator
       by user id , timestamp and state of avtive
    
    Arguments:
        PasswordResetTokenGenerator {CLASS} -- a built-in class
    
    Returns:
        STRING -- returns a hashed info 
    """

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()