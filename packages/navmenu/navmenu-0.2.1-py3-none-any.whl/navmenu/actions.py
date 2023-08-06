from abc import ABC, abstractmethod
from typing import Optional, Union

from .responses import Message, Response


class Action(ABC):
    """A generic action. Every action must inherit from this class and override its methods."""

    __slots__ = ()

    @abstractmethod
    def process(self, payload: Optional[dict] = None) -> Union[Message, Response]:
        """Process the payload and return a response.

        Args:
            payload: An incoming message payload.

        Returns:
            A message or a response object.
        """
        pass

    @abstractmethod
    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            A serialized class instance.
        """
        pass


class MessageAction(Action):
    """An action that returns a message.

    Args:
        text: The message text.
    """

    __slots__ = 'text',

    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f'MessageAction({repr(self.text)})'

    def process(self, payload: Optional[dict] = None) -> Message:
        return Message(self.text, payload=payload)

    def serialize(self) -> dict:
        return {
            'text': self.text,
        }


class SubmenuAction(Action):
    """An action that opens a submenu.

    Args:
        menu_name: The name of the menu to open.
    """

    __slots__ = 'menu_name',

    def __init__(self, menu_name: str) -> None:
        self.menu_name = menu_name

    def __repr__(self) -> str:
        return f'SubmenuAction({repr(self.menu_name)})'

    def process(self, payload: Optional[dict] = None) -> Response:
        return Response(menu=self.menu_name)

    def serialize(self) -> dict:
        return {
            'menu_name': self.menu_name,
        }


class GoBackAction(Action):
    """An action that returns user to the one of previous menus.

    Args:
        count: How many times to go back.
    """

    __slots__ = 'count',

    def __init__(self, count: int = 1) -> None:
        self.count = count

    def __repr__(self) -> str:
        return f'GoBackAction({self.count})'

    def process(self, payload: Optional[dict] = None) -> Response:
        return Response(go_back_count=self.count)

    def serialize(self) -> dict:
        res = {}

        if self.count != 1:
            res['count'] = self.count

        return res


class ExecuteAction(Action):
    """An action that executes a code and optionally returns a message with the result.

    Args:
        command: The code to execute.
        return_text: Whether to return result as a message with text.
    """

    __slots__ = 'command', 'return_text'

    def __init__(self, command: str, return_text: bool = False) -> None:
        self.command = command
        self.return_text = return_text

    def __repr__(self) -> str:
        return f'ExecuteAction({repr(self.command)}, {self.return_text})'

    def process(self, payload: Optional[dict] = None) -> Message:
        return Message(str(eval(self.command)) if self.return_text else exec(self.command), payload=payload)

    def serialize(self) -> dict:
        res = {
            'command': self.command,
        }

        if self.return_text is not False:
            res['return_text'] = self.return_text

        return res


class FunctionAction(Action):
    """An action that runs a function and optionally returns a response.

    Args:
        function: The function to run.
    """

    __slots__ = 'function',

    def __init__(self, function) -> None:
        self.function = function

    def __repr__(self) -> str:
        return f'FunctionAction({self.function})'

    def process(self, payload: Optional[dict] = None) -> Union[Message, Response]:
        return self.function(payload)

    def serialize(self) -> dict:
        return {
            'function': self.function.__name__,
        }
