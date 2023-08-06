from types import ModuleType
from typing import Optional, Sequence

from . import actions
from . import contents
from . import item_contents
from . import items
from . import menus


def filter_kwargs(data: dict, extra_excludes: Optional[Sequence] = None) -> dict:
    if extra_excludes is None:
        extra_excludes = ()

    return {k: v for k, v in data.items() if k not in ['type', *extra_excludes]}


def deserialize_action(data: dict, function_container: ModuleType):
    class_ = getattr(actions, data['type'])

    if 'function' in data:
        return class_(
            **filter_kwargs(data, ('function', )),
            function=getattr(function_container, data['function']),
        )

    else:
        return class_(**filter_kwargs(data))


def deserialize_item_content(data: dict):
    return getattr(item_contents, data['type'])(**filter_kwargs(data))


def deserialize_item(data: dict, function_container: ModuleType):
    kwargs = filter_kwargs(data, ('action', 'content'))

    if 'action' in data:
        kwargs['action'] = deserialize_action(data['action'], function_container)

    if 'content' in data:
        kwargs['content'] = deserialize_item_content(data['content'])

    return getattr(items, data['type'])(**kwargs)


def deserialize_content(data: dict):
    return getattr(contents, data['type'])(**filter_kwargs(data))


def deserialize_menu(data: dict, function_container: ModuleType, custom_menu_handlers):
    class_ = getattr(menus, data['type'])

    if 'items' in data:
        return class_(
            **filter_kwargs(data, ('content', 'items', 'default_action')),
            content=deserialize_content(data['content']),
            items=[deserialize_item(i, function_container) for i in data['items']],
            default_action=(
                deserialize_action(data['default_action'], function_container) if 'default_action' in data else None
            ),
        )

    else:
        return class_(
            **filter_kwargs(data, ('handler', )),
            handler=next(i for i in custom_menu_handlers if i.__name__ == data['handler']),
        )


def deserialize(data: dict, function_container: ModuleType = None, custom_menu_handlers: Sequence = None) -> dict:
    """Deserialize the dictionary to a menu list.

    Args:
        data: Data to deserialize.
        function_container: A module that contains custom functions to be called by actions.
        custom_menu_handlers: A sequence of custom classes to control menus.

    Returns:
        A dictionary mapping menu names to menus.
    """
    return {
        menu_name: deserialize_menu(menu, function_container, custom_menu_handlers)
        for menu_name, menu in data['menus'].items()
    }
