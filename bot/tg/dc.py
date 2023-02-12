from typing import Optional

from pydantic import BaseModel, Field

class MessageForm(BaseModel):
    id: int
    username: str | None = None


class Chat(BaseModel):
    id: int
    username: str | None = None


class Message(BaseModel):
    message_id: int
    from_: MessageForm = Field(..., alias= 'from' )
    chat: Chat
    text: str | None = None

    class Config:
        allow_population_by_field_name = True

class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj] = []


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message

# (update_id=258902349, message=MessageObj(from_=FromObj(id=894785752, unknown_things={'is_bot': False, 'first_name': 'Пабло', 'username': 'luffy2232', 'language_code': 'ru'}), chat=ChatObj(id=894785752, unknown_things={'first_name': 'Пабло', 'username': 'luffy2232', 'type': 'private'}), text='Ffy', unknown_things={'message_id': 24, 'date': 1676045945}), edited_message=None), UpdateObj(update_id=258902350, message=MessageObj(from_=FromObj(id=894785752, unknown_things={'is_bot': False, 'first_name': 'Пабло', 'username': 'luffy2232', 'language_code': 'ru'}), chat=ChatObj(id=894785752, unknown_things={'first_name': 'Пабло', 'username': 'luffy2232', 'type': 'private'}), text='Gggg', unknown_things={'message_id': 25, 'date': 1676045949}), edited_message=None), UpdateObj(update_id=258902351, message=None, edited_message=None), UpdateObj(update_id=258902352, message=None, edited_message=None), UpdateObj(update_id=258902353, message=MessageObj(from_=FromObj(id=894785752, unknown_things={'is_bot': False, 'first_name': 'Пабло', 'username': 'luffy2232', 'language_code': 'ru'}), chat=ChatObj(id=894785752, unknown_things={'first_name': 'Пабло', 'username': 'luffy2232', 'type': 'private'}), text='/start', unknown_things={'message_id': 26, 'date': 1676045980, 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}), edited_message=None), UpdateObj(update_id=258902354, message=MessageObj(from_=FromObj(id=894785752, unknown_things={'is_bot': False, 'first_name': 'Пабло', 'username': 'luffy2232', 'language_code': 'ru'}), chat=ChatObj(id=894785752, unknown_things={'first_name': 'Пабло', 'username': 'luffy2232', 'type': 'private'}), text='Последнее', unknown_things={'message_id': 28, 'date': 1676127322}), edited_message=None), UpdateObj(update_id=258902355, message=MessageObj(from_=FromObj(id=894785752, unknown_things={'is_bot': False, 'first_name': 'Пабло', 'username': 'luffy2232', 'language_code': 'ru'}), chat=ChatObj(id=894785752, unknown_things={'first_name': 'Пабло', 'username': 'luffy2232', 'type': 'private'}), text='kfcn', unknown_things={'message_id': 29, 'date': 1676128065}), edited_message=None)])
