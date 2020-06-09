import json

from telebot import TeleBot
from config import token
from models import State, Review


class ReviewBlock:
    def __init__(self, token):
        self._token = token
        self._bot = TeleBot(self._token)

        self._MESSAGES = {
            0: 'Enter your name', 1: 'Enter your last name',
            2: 'Enter your email', 3: 'Enter your phone',
            4: 'Enter your review', 5: 'Thank you for your review'
        }

        self._REVIEW_STEPS = {
            1: 'name', 2: 'last_name',
            3: 'email', 4: 'phone',
            5: 'review'
        }

        self._review_dict = {}

        @self._bot.message_handler(commands=["start"])
        def _start(message):
            self._start_command(message)

        @self._bot.message_handler(content_types=['text'])
        def _review(message):
            self._review_command(message)

        self._bot.polling()

    @staticmethod
    def _get_user_state(chat_id):
        states = json.loads(State.objects.get(chat_id=chat_id).to_json())
        return states['state']

    @staticmethod
    def _update_user_state(chat_id, new_state):
        State.objects(chat_id=chat_id).update_one(state=new_state)

    def _get_current_message(self, chat_id):
        return self._MESSAGES[self._get_user_state(chat_id)]

    def _start_command(self, message):
        chat_id = message.chat.id
        self._bot.send_message(message.chat.id, 'Hello. Leave your review.')
        try:
            State.objects.create(chat_id=chat_id)
        except Exception:
            self._update_user_state(chat_id, 0)
        self._bot.send_message(chat_id, self._get_current_message(chat_id))
        self._update_user_state(chat_id, self._get_user_state(chat_id) + 1)

    def _review_command(self, message):
        chat_id = message.chat.id
        state = self._get_user_state(chat_id)
        message_text = self._get_current_message(chat_id)
        self._bot.send_message(chat_id, message_text)
        self._review_dict[self._REVIEW_STEPS[state]] = message.text
        self._update_user_state(chat_id, state + 1)
        if self._get_user_state(chat_id) >= len(self._MESSAGES):
            Review.objects.create(**self._review_dict)
            self._update_user_state(chat_id, 0)


if __name__ == '__main__':
    review_block = ReviewBlock(token)

