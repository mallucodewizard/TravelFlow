from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed


class User:
    """
    A custom user object that mimics the essential attributes
    Django expects, such as is_authenticated.
    """
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.is_authenticated = True

    def __str__(self):
        return self.username


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Override the default get_user to avoid database lookups.
        """
        try:
            user_id = validated_token.get('user_id')
            username = validated_token.get('username')
            if not user_id or not username:
                raise AuthenticationFailed("Invalid token payload.")

            # Return a custom user-like object
            return User(user_id=user_id, username=username)
        except KeyError:
            raise InvalidToken("Token payload missing 'user_id' or 'username'.")
