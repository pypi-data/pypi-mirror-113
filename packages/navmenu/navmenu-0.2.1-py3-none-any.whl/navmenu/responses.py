from typing import Optional

from navmenu.keyboard import Keyboard


class Message:
    """An object that represents a message.

    Args:
        text: The message text.
        keyboard: The message keyboard.
        payload: The message payload.
    """

    __slots__ = 'keyboard', 'text'

    def __init__(
            self, text: Optional[str] = None, keyboard: Optional[Keyboard] = None, payload: Optional[dict] = None
    ) -> None:
        if payload is None:
            payload = {}

        self.keyboard = keyboard

        self.text = text.format(**payload) if text is not None else None

    def __repr__(self) -> str:
        return f'Message({repr(self.text)}, {self.keyboard})'


class Response:
    """An object that represents a message and can be used to change the current menu.

    Args:
        message: The message.
        menu: The name of the menu to go to.
        go_back_count: How many steps to go back.
    """

    __slots__ = 'message', 'menu', 'go_back_count'

    def __init__(
            self, message: Optional[Message] = None, menu: Optional[str] = None, go_back_count: Optional[int] = None
    ) -> None:
        self.message = message
        self.menu = menu
        self.go_back_count = go_back_count

    def __repr__(self) -> str:
        return f'Response({self.message}, {repr(self.menu)}, {self.go_back_count})'
