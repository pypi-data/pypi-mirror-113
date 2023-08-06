import json
from typing import Optional, Sequence

from navmenu.io.base import BaseIO
from navmenu.keyboard import Keyboard
from navmenu.menu_manager import MenuManager
from navmenu.responses import Message


class TelegramMessage:
    def add_keyboard_button(self, payload: dict, text: str) -> None:
        self.rows[-1].append({
            'text': text,
            'callback_data': json.dumps(payload, ensure_ascii=False, separators=(',', ':')),
        })

    def format_keyboard(self, keyboard: Keyboard) -> str:
        for row in keyboard.lines:
            self.rows.append([])

            for button in row:
                payload = {'a': button.payload}

                self.add_keyboard_button(payload, button.text)

        return json.dumps({
            'inline_keyboard': self.rows,
        }, ensure_ascii=False, separators=(',', ':'))

    def __init__(self, text: str, keyboard: Keyboard = None) -> None:
        self.text = text

        self.rows = []
        self.keyboard = None
        if keyboard is not None:
            self.keyboard = self.format_keyboard(keyboard)


def format_message(message: Message) -> TelegramMessage:
    return TelegramMessage(message.text, message.keyboard)


class TelegramIO(BaseIO):
    def __init__(self, menu_manager: MenuManager) -> None:
        super().__init__(menu_manager)

    def process(self, user_id: int, text: Optional[str], payload: dict) -> Sequence[TelegramMessage]:
        res = []

        action = payload['a'] if 'a' in payload else text

        final_payload = {
            **payload,
            'user_id': user_id,
            'text': text,
        }

        if self.menu_manager.state_handler.create(user_id):
            return format_message(
                self.menu_manager.get_message(user_id=user_id, payload=final_payload)
            ),

        current_state = self.menu_manager.state_handler.get(user_id)

        try:
            messages = self.menu_manager.select(action, user_id=user_id, payload=final_payload)

        except ValueError:
            return TelegramMessage('Invalid command'),

        else:
            res += [format_message(i) for i in messages]

        new_state = self.menu_manager.state_handler.get(user_id)
        if current_state != new_state:
            message = self.menu_manager.get_message(user_id=user_id, payload=final_payload)

            res.append(format_message(message))

        return res
