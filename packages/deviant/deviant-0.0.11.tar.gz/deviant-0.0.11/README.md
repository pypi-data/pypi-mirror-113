### DEVIANT - API для получения Стикеров, приложений, групп пользователя и прочего.
 
# Установка:
~~~python
pip install deviant
~~~

>Deviant - Требуеют от вас "Токен" или же "Doken"

* Детальная документация: https://github.com/DarsoX/Deviant/wiki/Documentation-Deviant

## Пример использования Doken:
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')
dev.apps_get(1) 
~~~
Doken можно получить тут: https://vk.com/app7440630

## Пример использования Token:
~~~python
from deviant import Deviant

dev = Deviant(token = 'Ваш Token')
dev.apps_get(1) 
~~~
Token можно получить тут: https://vkhost.github.io/

# Другие методы:

| Метод | Параметр | Описание |
| ----- | -------- | -------- |
| stickers_get() | int(user_id) | Получит стикеры пользователя | 
| stickers_info_get() | int(sticker_id) | Получит информацию о стикере и его наборе |
| apps_get() | int(user_id) | Получит приложения, которые создал пользователь|
| groups_get() | int(user_id) | Получит сообщества, которые создал пользователь|
| balayandex_get() | str(text), init(style) | Балабоба от Yandex |
| translator_emj() | str(text), ru или en | Переводит текст с русского, английського на смайлы |


Вопросы можете задавать в лс: https://vk.com/darsox