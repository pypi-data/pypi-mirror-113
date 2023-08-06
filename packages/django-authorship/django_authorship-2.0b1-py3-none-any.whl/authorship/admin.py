import typing

from django import forms, http
from django.contrib import admin

from . import models


if typing.TYPE_CHECKING:
    _BaseAuthorshipInlineMixin = admin.ModelAdmin
else:
    _BaseAuthorshipInlineMixin = object


class AuthorshipInlineMixin(_BaseAuthorshipInlineMixin):
    """Mixin for a model admin to set created/updated by on save for related
    inline models."""

    def save_formset(
        self,
        request: http.HttpRequest,
        form: forms.Form,
        formset: forms.BaseModelFormSet,
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> None:
        if issubclass(formset.model, models.Authorship):
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save(user=request.user)
            formset.save_m2m()
            for obj in formset.deleted_objects:
                obj.delete()
        else:
            return super().save_formset(
                request, form, formset, *args, **kwargs
            )


class AuthorshipMixin(AuthorshipInlineMixin):
    """Mixin for a model admin to set created/updated by on save."""

    def save_model(
        self,
        request: http.HttpRequest,
        obj: models.Authorship,
        form: forms.ModelForm,
        change: bool,
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> None:
        # Set created_by / updated_by fields using request.user
        if not change:
            obj.created_by = request.user  # type: ignore[assignment]
        obj.updated_by = request.user  # type: ignore[assignment]
        return super().save_model(  # type: ignore[call-arg]
            request, obj, form, change, *args, **kwargs
        )
