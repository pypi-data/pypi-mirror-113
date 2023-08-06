import typing

from django import forms
from django.contrib.auth import models as auth


if typing.TYPE_CHECKING:
    _BaseAuthorshipMixin = forms.ModelForm
else:
    _BaseAuthorshipMixin = object


class AuthorshipMixin(_BaseAuthorshipMixin):
    """Mixin for a :py:class:`~django.forms.ModelForm` which sets
    ``created_by`` and ``updated_by`` fields for the instance when saved.

    Requires that a ``User`` instance be passed in to the constructor. Views
    which utilise :py:class:`~authorship.views.AuthorshipViewMixin` handle this
    already.

    """

    def __init__(
        self,
        user: auth.AbstractBaseUser,
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> None:
        """

        :param user: A user instance, used to set ``created_by`` /
            ``updated_by`` fields on save.

        """
        self.user = user
        super().__init__(*args, **kwargs)

    def save(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> auth.AbstractBaseUser:
        self.instance.updated_by = self.user
        if not self.instance.created_at:
            self.instance.created_by = self.user

        return super().save(*args, **kwargs)
