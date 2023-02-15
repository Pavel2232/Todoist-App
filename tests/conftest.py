from pytest_factoryboy import register

from tests.factories import GoalCategoryFactory, BoardFactory, BoardParticipantFactory, UserFactory, GoalFactory, \
    CommentFactory

pytest_plugins = 'tests.fixtures'

register(GoalCategoryFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(UserFactory)
register(GoalFactory)
register(CommentFactory)

