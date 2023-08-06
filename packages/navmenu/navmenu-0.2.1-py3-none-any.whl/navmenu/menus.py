import collections.abc
from abc import ABC, abstractmethod
from typing import Iterator, Optional, Sequence

from .actions import Action
from .contents import BaseContent
from .items import BaseItem
from .responses import Message
from .keyboard import KeyboardButton, Keyboard


class BaseMenu(ABC):
    """A generic menu."""

    __slots__ = ()

    @abstractmethod
    def select(self, action: str, payload=None) -> Optional[Iterator[Message]]:
        """Select an item based on action and payload and optionally return one or multiple messages.

        Args:
            action: A string indicating selected menu button.
            payload: An incoming message payload.

        Returns:
            None or a list of messages.
        """
        pass

    @abstractmethod
    def get_message(self, payload: Optional[dict] = None) -> Message:
        """Get a message representing the menu.

        Args:
            payload: An incoming message payload.

        Returns:
            A message representing the menu.
        """
        pass

    @abstractmethod
    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            A serialized class instance.
        """
        pass

    def enter(self, payload: Optional[dict] = None) -> Optional[Message]:
        """Enter the menu and optionally return a message.

        Args:
            payload: An incoming message payload.

        Returns:
            None or a message.
        """
        pass


class Menu(BaseMenu):
    """A menu with fixed content and list of items.

    Args:
        content: The menu content.
        items: A sequence of menu items.
        default_action: The action to select when the provided action does not exist.
    """

    __slots__ = 'content', 'items', 'default_action'

    def __init__(
            self,
            content: BaseContent,
            items: Optional[Sequence[BaseItem]] = None,
            default_action: Optional[Action] = None,
    ) -> None:
        if items is None:
            items = []

        self.content = content
        self.items = items
        self.default_action = default_action

    def __repr__(self) -> str:
        return f'Menu({self.content}, {self.items}, {repr(self.default_action)})'

    def select(self, action: str, payload: Optional[dict] = None) -> Optional[Iterator[Message]]:
        target_item = next((
            i for i in self.items if (isinstance(i, BaseItem) and i.name == action and i.is_available(payload))
        ), None)

        if target_item is None:
            if self.default_action:
                return self.default_action.process(payload),

            return

        return target_item.on_select(payload)

    def get_message(self, payload: Optional[dict] = None) -> Message:
        if payload is None:
            payload = {}

        keyboard = Keyboard()
        for item in self.items:
            if item.is_available(payload):
                kwargs = item.get_content()

                if kwargs['type'] == 'button':
                    del kwargs['type']

                    if 'text' in kwargs:
                        kwargs['text'] = kwargs['text'].format(**payload)

                    keyboard.add_button(KeyboardButton(**kwargs))

                elif kwargs['type'] == 'line_break':
                    keyboard.add_line()

        return Message(payload=payload, keyboard=keyboard, **self.content)

    def add_item(self, item: BaseItem) -> None:
        """Add the item to the menu.

        Args:
            item: The item to add.

        Raises:
            RuntimeError: The menu's item list is immutable.
        """
        try:
            self.items.append(item)
        except AttributeError:
            raise RuntimeError('The menu\'s item list is immutable')

    def serialize(self) -> dict:
        res = {
            'content': {
                'type': self.content.__class__.__name__,
                **self.content.serialize(),
            }
        }

        if self.items:
            res['items'] = [{
                'type': item.__class__.__name__,
                **item.serialize(),
            } for item in self.items]

        if self.default_action:
            res['default_action'] = {
                'type': self.default_action.__class__.__name__,
                **self.default_action.serialize(),
            }

        return res


class CustomMenu(BaseMenu):
    """A menu that is controlled by a custom class.

    Args:
        handler: A class containing "select", "get_message" and "enter" methods.
    """

    __slots__ = 'handler',

    def __init__(self, handler) -> None:
        super().__init__()

        self.handler = handler

    def __repr__(self) -> str:
        return f'CustomMenu({self.handler})'

    def select(self, action: str, payload: Optional[dict] = None) -> Optional[Iterator[Message]]:
        res = self.handler.select(action, payload)

        return res if isinstance(res, collections.abc.Sequence) else (res, )

    def get_message(self, payload: Optional[dict] = None) -> Optional[Message]:
        return self.handler.get_message(payload)

    def serialize(self) -> dict:
        res = {
            'handler': self.handler.__name__
        }

        return res

    def enter(self, payload: Optional[dict] = None) -> Optional[Message]:
        return self.handler.enter(payload)
