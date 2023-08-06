# navmenu

A library to create multilevel menus for chatbots.

[![PyPI Version](https://img.shields.io/pypi/v/navmenu.svg)](https://pypi.org/project/navmenu/)
[![Python Versions](https://img.shields.io/pypi/pyversions/navmenu.svg)](https://pypi.org/project/navmenu/)
[![Documentation Status](https://readthedocs.org/projects/navmenu/badge/?version=latest)](https://navmenu.readthedocs.io/en/latest/)
[![Tests](https://github.com/rashidsh/navmenu/workflows/Tests/badge.svg)](https://github.com/rashidsh/navmenu/actions)

## Installation

navmenu can be installed with pip:
```bash
pip3 install navmenu
```

## Introduction

First, import everything you will need:
```python
from navmenu import MenuManager
from navmenu.actions import MessageAction, SubmenuAction, GoBackAction
from navmenu.contents import Content
from navmenu.io import ConsoleIO
from navmenu.item_contents import TextItemContent
from navmenu.items import Item
from navmenu.menus import Menu
from navmenu.state import MemoryStateHandler
```

Then, create a menu with one item:
```python
menu = Menu(Content('Welcome!'), [
    Item('print', TextItemContent('print text'), MessageAction('Text message'))
])
```

`'print'` is the internal menu item name. It can be any string but **must be unique within menu**.

Also, you can add items to menus later:
```python
new_item = Item('hello', TextItemContent('say hello'), MessageAction('Hello!'))
menu.add_item(new_item)
```

Every menu should be wrapped in a `MenuManager`:
```python
menu_manager = MenuManager({
    'main_menu': menu
}, MemoryStateHandler('main_menu'))
```

`MemoryStateHandler('main_menu')` means that the user state will be saved in memory. It will not persist between app restarts. `'main_menu'` is the name of the first menu to show.

Finally, show the menu to a user:
```python
io = ConsoleIO(menu_manager)
io.start_loop()
```

## Links

- [Documentation](https://navmenu.readthedocs.io/en/latest/)
- [Examples](https://github.com/rashidsh/navmenu/tree/master/examples)
- [License](https://github.com/rashidsh/navmenu/blob/master/LICENSE)
