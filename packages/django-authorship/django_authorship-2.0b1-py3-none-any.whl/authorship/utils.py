from django.contrib import auth
from django.contrib.auth import models

from . import settings


def get_website_user() -> models.AbstractBaseUser:
    """Get a generic 'website' user.

    Can be used to specify the required user when there is no direct link to
    a real user.
    """

    UserModel = auth.get_user_model()
    user, created = UserModel.objects.get_or_create(**settings.WEBSITE_USER)

    if created:
        user.set_unusable_password()
        user.is_active = False
        user.save()

    return user
