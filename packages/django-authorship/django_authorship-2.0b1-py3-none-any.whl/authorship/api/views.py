from rest_framework import request, serializers


class AuthorshipMixin:

    request: request.HttpRequest

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        serializer.save(
            created_by=self.request.user, updated_by=self.request.user
        )

    def perform_update(self, serializer: serializers.ModelSerializer) -> None:
        serializer.save(updated_by=self.request.user)
