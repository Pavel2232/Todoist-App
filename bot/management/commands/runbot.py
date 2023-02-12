import logging
import time

from django.core.management import BaseCommand
from django.db import transaction

from TodoList_App import settings
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, Status, GoalCategory



class Command(BaseCommand):


    def __init__(self):
        super().__init__()
        self.tg_client = TgClient(token=settings.KEY_TG_BOT)
        self.__tg_user: TgUser | None = None
        self.offset = 0

    @property
    def tg_user(self) -> TgUser:
        if self.__tg_user:
            return self.__tg_user
        raise RuntimeError('User does not exist')



    def handle(self,*args,**options):
        offset = 0
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
        else:
            ...
            # self.__handle_message(message)

    def _handle_command(self,message: Message):
        match message.text:
            case '/goals':
                self._handle_goals_command(message)
            # case '/cancel':
            #     self._handle_cancel(message)









    # def __handle_message(self,message: Message):
    #     self.tg_client.send_message(
    #         chat_id=message.chat.id,
    #         text='Задайте команду'
    #     )

    # def _handle_cancel(self,message: Message):
    #     self.tg_client.send_message(
    #         chat_id=message.chat.id,
    #         text='Операция отменена'
    #     )



    def _handle_goals_command(self,message: Message):
        goals: list[str] = list(
            Goal.objects.filter(category__board__participants__user= self.tg_user.user_id)
            .exclude(status=Status.archived).values_list('title',flat=True)
        )

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='\n'.join(goals) if goals else 'No goals'
        )
    #
    # def _handle_category_command(self,message: Message):
    #     goals: list[str] = list(
    #         GoalCategory.objects.filter(board__participants__user= self.tg_user.user_id)
    #         .exclude(is_deleted=True).values_list('title',flat=True)
    #     )
    #     self.goals = goals
    #     self.tg_client.send_message(
    #         chat_id=message.chat.id,
    #         text='\n'.join(goals)  if goals else 'No goals'
    #     )

    # def _handle_create_command(self,message: Message):
    #     if message.text not in self.goals:
    #         self.tg_client.send_message(
    #             chat_id= message.chat.id,
    #             text= 'Введите предложенную категорию, создавать категории пока не умею'
    #         )
    #         self.get_category = False
    #     category = GoalCategory.objects.get(title=message.text)
    #     self.get_category = True
    #     self.tg_client.send_message(
    #         chat_id=message.chat.id,
    #         text='Название цели?'
    #     )
    #
    #     title = message.text
    #     with transaction.atomic():
    #         result = Goal.objects.create(title=title,category=category,user=self.tg_user.user_id)
    #
    #     self.tg_client.send_message(
    #         chat_id=message.chat.id,
    #         text=result.objects.values_list('title',flat=True)
    #     )

