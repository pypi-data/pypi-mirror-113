from abc import ABC, abstractmethod

from .keyboard import ButtonColors


class ItemContent(ABC):
    """Generic menu item content."""

    __slots__ = ()

    @abstractmethod
    def get_content(self, payload: str) -> dict:
        """Process the payload and return item content.

        Args:
            payload: An incoming message payload.

        Returns:
            Item content.
        """
        pass

    @abstractmethod
    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            Serialized class instance.
        """
        pass


class TextItemContent(ItemContent):
    """A text menu item.

    Attributes:
        text: The item text.
        color: The item color.
    """

    __slots__ = 'text', 'color'

    def __init__(self, text: str, color: int = ButtonColors.DEFAULT) -> None:
        self.text = text
        self.color = color

    def __repr__(self) -> str:
        return f'TextItemContent({repr(self.text)}, {self.color})'

    def get_content(self, payload: str) -> dict:
        return {
            'type': 'button',
            'text': self.text,
            'color': self.color,
            'payload': payload,
        }

    def serialize(self) -> dict:
        res = {
            'text': self.text,
        }

        if self.color != ButtonColors.DEFAULT:
            res['color'] = self.color

        return res
