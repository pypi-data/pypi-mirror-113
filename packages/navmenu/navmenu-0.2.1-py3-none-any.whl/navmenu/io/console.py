from typing import Callable, Sequence

from navmenu.io.base import BaseIO
from navmenu.menu_manager import MenuManager
from navmenu.responses import Message

SEPARATOR = '-' * 20


def send_default(message):
    print(message)


def format_message(message: Message) -> str:
    actions = ''

    if message.keyboard is not None:
        for line in message.keyboard.lines:
            actions += ' | '.join(f"{i.payload}: {i.text}" for i in line) + '\n'

    if actions:
        return f'{SEPARATOR}\n{message.text}\n{SEPARATOR}\n{actions}{SEPARATOR}'
    else:
        return f'\n{message.text}'


class ConsoleIO(BaseIO):
    def __init__(self, menu_manager: MenuManager, send: Callable = send_default) -> None:
        super().__init__(menu_manager)

        self.send = send

    def process(self, text: str) -> Sequence[str]:
        res = []

        try:
            messages = self.menu_manager.select(text)

        except ValueError:
            res.append(format_message(Message('Invalid command')))

        else:
            res += [format_message(i) for i in messages]

        message = self.menu_manager.get_message()
        res.append(format_message(message))

        return res

    def start_loop(self) -> None:
        """Process messages and respond to them."""
        self.send(format_message(self.menu_manager.get_message()))

        while True:
            res = self.process(input('Command: '))
            for message in res:
                self.send(message)
