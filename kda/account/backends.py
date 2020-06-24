from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrPhoneNumberModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, kwargs**):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        users = user_model.default_manager.filter( Q(**{user_model.USERNAME_FIELD:username}) | Q(email__iexact=username))
        for user in users:
            if user.checkpassword(password):
                return user
        if not users:
            user_model().set_password(password)
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None

