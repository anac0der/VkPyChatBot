import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from footbot import Bot

token = "0123456789"
vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)


def write_mess(user_id, message):
    random_id = random.randint(-2 ** 32, 2 ** 32)
    vk.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'message': message})


users_bot_class_dict = {}

print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        try:
            if event.to_me:
                user_id = event.user_id
                print('New message:')
                print(f'For me by: {user_id}', end=' ')

                user_id = event.user_id
                if user_id not in users_bot_class_dict:
                    users_bot_class_dict[user_id] = Bot(event.user_id)

                write_mess(event.user_id, users_bot_class_dict[user_id].update_screen(event.text))
                print('Text: ', event.text)
        except TimeoutError:
            write_mess(270461087, "ОШИБКА!!!")
            print("ERROR OCCURED")


