from pytest_factoryboy import register

from tests.factories import GoalCategoryFactory

register(GoalCategoryFactory)

pytest_plugins = 'tests.fixtures'
