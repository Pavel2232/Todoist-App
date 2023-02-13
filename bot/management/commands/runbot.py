import datetime

from django.core.management import BaseCommand

from TodoList_App import settings
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, Status, GoalCategory

class ModelForCreate:

    def __init__(self):
        self._steps = None
        self.name_goal = None


    def check_steps(self):
        """Проверка на каком мы этапе создания"""
        if self._steps:
            return self._steps
        else:
            self._steps = 'start'
            return self._steps
    def choose_category(self):
        self._steps = "Выбираем категорию"
        return self._steps

    def title(self):
        self._steps = "Придумываем название"
        return self._steps

    def create_goal(self):
        self._steps = "Создание цели"
        return self._steps

    def due_data(self):
        self._steps = "Дедлайн"
        return self._steps

    def cancel_commands(self):
        self._steps = None
        return self._steps


steps = ModelForCreate()
class Command(BaseCommand):


    def __init__(self):
        super().__init__()
        self.tg_client = TgClient(token=settings.KEY_TG_BOT)
        self.__tg_user: TgUser | None = None
        self.offset = 0
        self.category = []

    @property
    def tg_user(self) -> TgUser:
        if self.__tg_user:
            return self.__tg_user
        raise RuntimeError('User does not exist')



    def handle(self,*args,**options):
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1

                self.__tg_user, _ = TgUser.objects.get_or_create(
                    chat_id= item.message.chat.id,
                    defaults={'username':item.message.from_.username}
                )
                if self.tg_user.user_id:
                    self._handle_verified_user(item.message)
                else:
                    self._handle_unverified_user(item.message)




    def _handle_unverified_user(self,message: Message):
        verification_code = self.tg_user.set_verification_code()


        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f"verification code {verification_code}"
        )

    def _handle_verified_user(self,message: Message):
        if message.text.startswith('/'):
            self._handle_command(message)
        elif steps.check_steps() == "Выбираем категорию":
            self.__handle_check_category_message(message)
        elif steps.check_steps() == "Придумываем название":
            self._handle_create_massege(message)
        elif steps.check_steps() == "Дедлайн":
            self._handle_dedline_massege(message)
        elif steps.check_steps() == "Создание цели":
            self._handle_create_goal(message)
        else:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text= 'Неизвестные команды'
            )


    def _handle_command(self,message: Message):
        match message.text:
            case '/goals':
                self._handle_goals_command(message)

            case '/create':
                self._handle_category_command(message)
                steps.choose_category()
                self.tg_client.send_message(
                    chat_id=message.chat.id,
                    text="Выберите категорию")

            case '/cancel':
                self._handle_cancel_command(message)




    def _handle_cancel_command(self, message: Message):
        steps.check_steps()
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='Введите команду'
        )

    def _handle_goals_command(self,message: Message):
        goals: list[str] = list(
            Goal.objects.filter(category__board__participants__user= self.tg_user.user_id)
            .exclude(status=Status.archived).values_list('title',flat=True)
        )

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='\n'.join(goals) if goals else 'No goals'
        )

    def _handle_category_command(self,message: Message):
        category: list[str] = list(
            GoalCategory.objects.filter(board__participants__user= self.tg_user.user_id)
            .exclude(is_deleted=True).values_list('title',flat=True)
        )
        self.category = category
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='\n'.join(category) if category else 'No category'
        )


    def __handle_check_category_message(self,message: Message):
        if message.text in self.category:
            self.create_category = GoalCategory.objects.get(title=message.text)
            steps.title()
            self._handle_verified_user(message)
        else:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text="введите Предложенную")

    def _handle_create_massege(self, message: Message):
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text="Введите название")
        steps.due_data()

    def _handle_dedline_massege(self, message: Message):
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text="Дедлайн через сколько дней?")
        steps.create_goal()

    def _handle_create_goal(self,message:Message):
        steps.name_goal = message.text
        if steps.name_goal:
            future_date = datetime.datetime.today() + datetime.timedelta(days=int(message.text))
            Goal.objects.create(title=message.text, user=self.tg_user.user, category=self.create_category,
                                due_date=future_date)
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text='Цель успешно создана'
            )
        steps.cancel_commands()