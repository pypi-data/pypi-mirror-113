import json
from typing import Optional, Sequence

from navmenu.io.base import BaseIO
from navmenu.keyboard import ButtonColors, Keyboard
from navmenu.menu_manager import MenuManager
from navmenu.responses import Message


VK_BUTTON_COLORS = {
    ButtonColors.DEFAULT: 'default',
    ButtonColors.PRIMARY: 'primary',
    ButtonColors.POSITIVE: 'positive',
    ButtonColors.NEGATIVE: 'negative',
}


class VKMessage:
    def add_keyboard_button(self, payload: dict, text: str, color: int) -> None:
        self.rows[-1].append({
            'color': VK_BUTTON_COLORS[color],
            'action': {
                'type': 'text',
                'label': text,
                'payload': payload,
            },
        })

    def format_keyboard(self, keyboard: Keyboard) -> str:
        for row in keyboard.lines:
            self.rows.append([])

            for button in row:
                payload = {'a': button.payload}

                self.add_keyboard_button(payload, button.text, button.color)

        return json.dumps({
            'one_time': False,
            'inline': False,
            'buttons': self.rows,
        }, ensure_ascii=False, separators=(',', ':'))

    def __init__(self, text: str, keyboard: Keyboard = None) -> None:
        self.text = text

        self.rows = []
        self.keyboard = None
        if keyboard is not None:
            self.keyboard = self.format_keyboard(keyboard)


def format_message(message: Message) -> VKMessage:
    return VKMessage(message.text, message.keyboard)


class VKIO(BaseIO):
    def __init__(self, menu_manager: MenuManager) -> None:
        super().__init__(menu_manager)

    def process(self, user_id: int, text: Optional[str], payload: dict) -> Sequence[VKMessage]:
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
            return VKMessage('Invalid command'),

        else:
            res += [format_message(i) for i in messages]

        new_state = self.menu_manager.state_handler.get(user_id)
        if current_state != new_state:
            message = self.menu_manager.get_message(user_id=user_id, payload=final_payload)

            res.append(format_message(message))

        return res
