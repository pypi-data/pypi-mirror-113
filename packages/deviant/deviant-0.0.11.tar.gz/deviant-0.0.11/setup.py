# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['deviant']
setup_kwargs = {
    'name': 'deviant',
    'version': '0.0.11',
    'description': 'Модуль для работы с Deviant Api',
    'long_description': '### DEVIANT - API для получения Стикеров, приложений, групп пользователя и прочего.\n \n# Установка:\n~~~python\npip install deviant\n~~~\n\n>Deviant - Требуеют от вас "Токен" или же "Doken"\n\n* Детальная документация: https://github.com/DarsoX/Deviant/wiki/Documentation-Deviant\n\n## Пример использования Doken:\n~~~python\nfrom deviant import Deviant\n\ndev = Deviant(doken = \'Ваш DOKEN\')\ndev.apps_get(1) \n~~~\nDoken можно получить тут: https://vk.com/app7440630\n\n## Пример использования Token:\n~~~python\nfrom deviant import Deviant\n\ndev = Deviant(token = \'Ваш Token\')\ndev.apps_get(1) \n~~~\nToken можно получить тут: https://vkhost.github.io/\n\n# Другие методы:\n\n| Метод | Параметр | Описание |\n| ----- | -------- | -------- |\n| stickers_get() | int(user_id) | Получит стикеры пользователя | \n| stickers_info_get() | int(sticker_id) | Получит информацию о стикере и его наборе |\n| apps_get() | int(user_id) | Получит приложения, которые создал пользователь|\n| groups_get() | int(user_id) | Получит сообщества, которые создал пользователь|\n| balayandex_get() | str(text), init(style) | Балабоба от Yandex |\n| translator_emj() | str(text), ru или en | Переводит текст с русского, английського на смайлы |\n\n\nВопросы можете задавать в лс: https://vk.com/darsox',
    'author': 'Deviant',
    'author_email': 'darsox.anime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DarsoX/Deviant/wiki/Documentation-Deviant',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
