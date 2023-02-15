import factory
import faker
from django.utils import timezone
from factory.django import DjangoModelFactory

from core.models import User
from goals.models import GoalCategory, Board, Goal, BoardParticipant, GoalComment


class DatesFactoryMixin(DjangoModelFactory):
    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    update = factory.LazyFunction(timezone.now)




class BoardFactory(DatesFactoryMixin):
    class Meta:
        model = Board

    title = factory.Faker('sentence')

    @factory.post_generation
    def with_owner(self,create,owner,**kwargs):
        if owner:
            BoardParticipant.objects.create(
                board=self,
                user=owner,
                role=BoardParticipant.Role.owner
            )

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User


    username = factory.Faker('user_name')
    password = "10203040x"
    email= 'test@test.com'



    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs,password_repeat="10203040x")


class BoardParticipantFactory(DatesFactoryMixin):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

class GoalCategoryFactory(DatesFactoryMixin):
    class Meta:
        model = GoalCategory

    title = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(DatesFactoryMixin):
    class Meta:
        model = Goal

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    category = factory.SubFactory(GoalCategoryFactory)
    due_date = factory.LazyFunction(timezone.now)


class CommentFactory(DatesFactoryMixin):
    class Meta:
        model = GoalComment

    text = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)