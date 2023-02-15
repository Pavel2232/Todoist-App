from pydantic import BaseModel, Field

"""Классы pydantic для удобной структуры сообщений из телеграмм"""


class MessageForm(BaseModel):
    id: int
    username: str | None = None


class Chat(BaseModel):
    id: int
    username: str | None = None


class Message(BaseModel):
    message_id: int
    from_: MessageForm = Field(..., alias='from')
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
