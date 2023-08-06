from abc import ABC, abstractmethod
from typing import Tuple


class BaseContent(ABC):
    """Generic menu content."""

    __slots__ = ()

    def __getitem__(self, key):
        return getattr(self, key)

    @abstractmethod
    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            A serialized class instance.
        """
        pass


class Content(BaseContent):
    """Text menu content.

    Args:
        text: The menu text.
    """

    __slots__ = 'text',

    def __init__(self, text: str = None) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f'Content({repr(self.text)})'

    @staticmethod
    def keys() -> Tuple[str]:
        return 'text',

    def serialize(self) -> dict:
        res = {}

        if self.text is not None:
            res['text'] = self.text

        return res
