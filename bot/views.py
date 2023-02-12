from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from TodoList_App import settings
from bot.serializers import BotTgSerializer
from bot.tg.client import TgClient


class VeryficationView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BotTgSerializer



    def update(self, request, *args, **kwargs):
        serializer: BotTgSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def perform_update(self, serializer):
        tg_user = serializer.save()
        TgClient(settings.KEY_TG_BOT).send_message(
            chat_id=tg_user.chat_id,
            text='[verification has been completed]'
        )