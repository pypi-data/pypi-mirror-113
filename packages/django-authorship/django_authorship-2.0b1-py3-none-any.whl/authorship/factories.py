from django.conf import settings


try:
    import factory
except ImportError as error:
    message = f"{error}. Try running `pip install factory_boy`."
    raise ImportError(message)


class AuthorshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    created_by = factory.SubFactory("authorship.factories.UserFactory")

    updated_by = factory.SelfAttribute("created_by")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ["username"]

    username = factory.Sequence(lambda n: f"user-{n}")


class UserFakerFactory(UserFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ["username"]

    first_name = factory.Faker("first_name")

    last_name = factory.Faker("last_name")

    username = factory.LazyAttribute(
        lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}"
    )

    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
