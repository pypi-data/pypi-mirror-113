from typing import Dict, Optional, Sequence

from .menus import BaseMenu
from .state import StateHandler
from .responses import Message, Response


class MenuManager:
    """A class that manages menus and transitions between them.

    Args:
        menus: A dictionary mapping menu names to menus.
        state_handler: The menu state manager to store users' states.
    """

    __slots__ = 'menus', 'state_handler'

    def __init__(self, menus: Dict[str, BaseMenu], state_handler: StateHandler) -> None:
        self.menus = menus
        self.state_handler = state_handler

    def __repr__(self) -> str:
        return f'MenuManager({self.menus}, {self.state_handler})'

    def get_message(self, user_id: int = None, payload: Optional[dict] = None) -> Message:
        """Get a message representing the current menu.

        Args:
            user_id: A value used to identify the user.
            payload: An incoming message payload.

        Returns:
            A message representing the current menu.
        """
        state = self.state_handler.get(user_id)

        return self.menus[state].get_message(payload)

    def select(self, action: str, user_id: int = None, payload: Optional[dict] = None) -> Sequence[Message]:
        """Select an item in the current menu based on action and payload.

        This method handles current menu changes.

        Args:
            action: A string indicating selected menu button.
            user_id: A value used to identify the user.
            payload: An incoming message payload.

        Returns:
            A list of messages.

        Raises:
            ValueError: An invalid action was provided.
        """
        state = self.state_handler.get(user_id)

        actions = self.menus[state].select(action, payload)
        if actions is not None:
            messages = []
            for res in actions:
                if isinstance(res, Message):
                    messages.append(res)

                elif isinstance(res, Response):
                    if res.message:
                        messages.append(res.message)

                    if res.go_back_count:
                        self.state_handler.go_back(user_id, res.go_back_count)

                    if res.menu:
                        self.state_handler.set(user_id, res.menu)

                        enter_res = self.menus[res.menu].enter(payload)
                        if isinstance(enter_res, Message):
                            messages.append(enter_res)

            return messages

        else:
            raise ValueError('An invalid action was provided')

    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            A serialized class instance.
        """
        return {
            'menus': {menu_name: {
                'type': menu.__class__.__name__,
                **menu.serialize(),
            } for menu_name, menu in self.menus.items()},
        }
