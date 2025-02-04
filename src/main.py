import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import os
from dotenv import load_dotenv


class ProjectBot:
    def __init__(self):
        load_dotenv()
        self.BOT_TOKEN = os.getenv("VK_BOT_TOKEN")
        self.BOT_GROUP_ID = os.getenv("BOT_GROUP_ID")
        if self.BOT_TOKEN is None or self.BOT_GROUP_ID is None:
            raise ValueError("Bot token or group id was not found in .env file")

        self.vk_session = vk_api.VkApi(token=self.BOT_TOKEN)
        self.longpoll = VkBotLongPoll(self.vk_session, int(self.BOT_GROUP_ID))
        self.vk = self.vk_session.get_api()

    def run_longpolling(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.object.message['from_id']
                message_text = event.object.message['text']
                attachments = event.object.message.get('attachments', [])

                # Отправляем приветственное сообщение при первом входе пользователя
                if event.object.message["id"] == 0 or event.object.message["id"] == 1:
                    self.vk.messages.send(
                        user_id=user_id,
                        random_id=get_random_id(),
                        message='Привет! Я бот, который принимает изображения и отправляет их обратно.'
                    )

                # обработка только сообщений с вложениями-изображениями
                if attachments:
                    for attachment in attachments:
                        if attachment['type'] == 'photo':
                            photo = attachment["photo"]
                            owner_id = photo["owner_id"]
                            photo_id = photo["id"]
                            access_key = photo.get("access_key", "")

                            attach_str = f"photo{owner_id}_{photo_id}"
                            if access_key:
                                attach_str += f"_{access_key}"

                            self.vk.messages.send(
                                user_id=user_id,
                                random_id=get_random_id(),
                                attachment=attach_str
                            )
                else:
                    # Игнорируем другие сообщения
                    pass


if __name__ == "__main__":
    bot = ProjectBot()
    bot.run_longpolling()