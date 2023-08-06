import typing
import warnings

from django.http import HttpRequest
from django.views import generic


if typing.TYPE_CHECKING:
    _BaseAuthorshipMixin = generic.edit.FormMixin
else:
    _BaseAuthorshipMixin = object


class AuthorshipMixin(_BaseAuthorshipMixin):
    """Adds the request's ``User`` instance to the form kwargs."""

    request: HttpRequest

    def get_form_kwargs(
        self, *args: typing.Any, **kwargs: typing.Any
    ) -> typing.Dict[str, typing.Any]:
        form_kwargs = super().get_form_kwargs(  # type: ignore[call-arg]
            *args, **kwargs
        )
        form_kwargs.update({"user": self.request.user})
        return form_kwargs


class AuthorshipViewMixin(AuthorshipMixin):
    """AuthorshipViewMixin is deprecated. Use AuthorshipMixin instead."""

    # Renamed for consistency with other mixins.

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        warnings.warn(
            "AuthorshipViewMixin is deprecated - use "
            "AuthorshipMixin instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)  # type: ignore[call-arg]
