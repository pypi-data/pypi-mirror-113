# Deviant
_Модуль, позволяющий обращаться к Deviant Api который позволяет добавлять в вашего бота ВК новый функционал_

* Язык: Python
* Разработчик: [DarsoX](https://vk.com/darsox)
* Модуль: [Pypi](https://pypi.org/project/deviant/)
* Поддержать автора: Z565980380935
***
![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true) - Требуется Doken или Token

> 1. [Установка модуля](#setup)
>> 2. [Doken](#setup)
>> 3. [Token](#setup)
> 4. [StickersGet](#StickersGet) - Получение наборов стикеров юзера ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true)
> 5. [StickersInfoGet](#StickersInfoGet) - Получение информации о стикере ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true)
> 6. [StickersFullGet](#StickersFullGet ) - Получение наборов стикеров юзера 〔 Детально 〕 ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true)
> 7. [SystemInfo](#SystemInfo) - Получение информации о номере телефона, почте и 2FA по токену. ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true)
> 8. [AppsGet](#AppsGet) - Получение информации о приложениях пользователя вк
> 9. [GroupsGet](#GroupsGet) - Получение информации о группах пользователя вк
> 10. [BalaYandex](#BalaYandex) - Балабоба от яндекса
> 11. [TranslatorEmj](#TranslatorEmj) - Переводчик текста в эмоджи
> 12. [KeyGenerator](#KeyGenerator)- Генератор ключей
> 13. [GetChatsLink](#GetChatsLink) - Получает ссылку на чат и информацию по нем. 〔 https://vk.com/slikkness 〕
> 14. [GetTesterInfo](#GetTesterInfo) - Получение карточки тестировщика пользователя.
> 15. [Ping](#Ping ) - Получение карточки тестировщика пользователя.


***

# <a name="setup"></a> Установка модуля:

* Bash: `pip install deviant`

* Pythonanywhere: `pip3 install --user deviant`

* Requirements.txt: `deviant == 0.0.9`



***
## <a name="Doken"></a> Пример использования Doken:
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')
dev.apps_get(1) 
~~~
Doken можно получить тут: https://vk.com/app7440630

## <a name="Token"></a> Пример использования Token:
~~~python
from deviant import Deviant

dev = Deviant(token = 'Ваш Token')
dev.apps_get(1) 
~~~
Token можно получить тут: https://vkhost.github.io/

***

## ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true) <a name="StickersGet"></a> StickersGet (Получение наборов стикеров юзера): 
* Метод: stickers_get(user_id)
* Описание: Получение стикеров пользователя в вк.
* Параметры: _user_id_ - ID пользователя вконтакте.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.stickers_get(1)
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|count - Количество наборов у пользователя.
----|count_max - Всего наборов в вк.
----|stickers - Массив с наборами пользователя.
------|name - Название стикер-пака.
------|price - Стоимость набора
------|id - ID набора.
----|rub - Общая цена наборов в рублях.
----|uah- Общая цена наборов  в гривне.
----|cost- Общая цена наборов  в голосах.
~~~


***

## ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true) <a name="StickersFullGet"></a> StickersFullGet (Получение наборов стикеров юзера 〔 Детально 〕):
* Метод: stickers_full_get(user_id,type)
* Описание: Получение стикеров пользователя в вк детальней, чем метод "StickersGet".
* Параметр 1: _user_id_ - ID пользователя вконтакте.
* Параметр 2: _type_ - число от 1 до 6.
> 1 - Возвращает все стили и стикеры.
> 2 - Возвращает только платные стикеры.
> 3 - Возвращает только платные стили.
> 4 - Возвращает только бесплатные стикеры.
> 5 - Возвращает только бесплатные стили.
> 6 - Возвращает ВСЕ.

* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.stickers_full_get(1,1)
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|count - Массив с количествами.
------|count_user_all - Количество Стикеров и Стилей пользователя.
------|count_max - Количество Стикеров и Стилей в ВК.
------|count_style- Количество стилей Пользователя.
------|count_pack - Количество паков Пользователя.
------|count_don_pack - Количество платных паков Пользователя.
------|count_don_style - Количество платных стилей Пользователя.
----|price - Массив с стоимостью.
------|price_all_rub - Все стикеры и стили в рублях.
------|price_all_vote- Все стикеры и стили в голосах.
------|price_pack_rub - Все стикеры в рублях.
------|price_pack_vote - Все стикеры в голосах.
------|price_style_rub - Все стили в рублях.
------|price_style_vote - Все стили в голосах.
----|sticker = Массив с категориями стикеров.
------|sticker_all - Массив со всеми наборами стикеров и стилями пользователя.
--------|id - ID набора.
--------|name - Название набора.
--------|price - Цена в голосах.
--------|rub - Цена в рублях.
--------|style - является ли набор стилем.
------|sticker_user_don - Массив со всеми платными наборами пользователя.
--------|id - ID набора.
--------|name - Название набора.
--------|price - Цена в голосах.
--------|rub - Цена в рублях.
------|sticker_user_free - Массив со всеми бесплатными наборами пользователя.
--------|id - ID набора.
--------|name - Название набора.
--------|price - Цена в голосах.
--------|rub - Цена в рублях.
------|style_user_don - Массив со всеми платными стилями пользователя.
--------|id - ID набора.
--------|name - Название набора.
--------|price - Цена в голосах.
--------|rub - Цена в рублях.
------|style_user_free - Массив со всеми бесплатными стилями пользователя.
--------|id - ID набора.
--------|name - Название набора.
--------|price - Цена в голосах.
--------|rub - Цена в рублях.
~~~




***

## ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true) <a name="StickersInfoGet"></a> StickersInfoGet (Получение информации о стикере):
* Метод: stickers_info_get(sticker_id)
* Описание: Получает информацию о стикере.
* Параметры: _sticker_id_ - ID стикера вконтакте.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.stickers_get(66)
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|sticker_pack - Массив с информацией о наборе стикера.
------|id - ID набора.
------|name - Название набора.
------|description - Описание набора.
------|author - Автор набора.
------|stikers - Количество стикеров в наборе.
------|value - Массив с информацией о покупке набора.
--------|purchase - Тип покупки.
--------|golos - Цена в голосах.
--------|rub- Цена в рублях.
----|sticker_info - Массив с информацией о стикере.
------|id - ID стикера.
------|tag - Ключевые слова стикера.
~~~

***

## ![doken](https://github.com/DarsoX/Deviant/blob/main/DOKEN.png?raw=true)<a name="SystemInfo"></a> SystemInfo (Получение информации о номере телефона, почте и 2FA по токену.):
* Метод: get_system_info()
* Описание: Получает информации о номере телефона, почте и 2FA по токену пользователя.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.get_system_info()
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|2FA - Включена ли 2FA авторизация.
----|phone - Привязанный номер телефона к странице.
----|email - Привязанный email к странице.
----|ping_vk - Время ответа сервера Вк.
----|ping_deviant - Время ответа сервера Deviant.
~~~


***

## <a name="AppsGet"></a> AppsGet (Получение информации о приложениях пользователя вк):
* Метод: apps_get(user_id)
* Описание: Получает информацию о приложениях которые создал пользователь в вк.
* Параметры: _user_id_ - ID пользователя вконтакте.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.apps_get(66)
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|count - Количество приложений пользователя.
----|apps - Массив с приложениями.
------|name - Название приложения.
------|users - Количество пользователей приложения.
------|id - ID приложения в вк.
~~~



***

## <a name="GroupsGet"></a> GroupsGet (Получение информации о группах пользователя вк):
* Метод: groups_get(user_id)
* Описание: Получает информацию о группах которые создал пользователь в вк.
* Параметры: _user_id_ - ID пользователя вконтакте.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.groups_get(1)
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|count - Количество групп пользователя.
----|groups - Массив с приложениями.
------|name - Название группы.
------|member - Количество участников группы.
------|id - ID группы в вк.
------|verified - Верификация группы.
~~~

***

## <a name="BalaYandex"></a> BalaYandex (Балабоба от яндекса):
* Метод: balayandex_get(text,style)
* Описание: Функционал Балабоба от яндекса - генерирует текст за заданным предложением.
* Параметр 1: _text_ - Ваше предложение, слово на которое должен запустится генератор.
* Параметр 2: _style_ - Индекс стиля от 0 до 11. (Параметр не обязательный, если не указать будет "Без стиля")
> 0. Без стиля (По стандарту) 
> 1. Теория заговора
> 2. ТВ-Репортажи
> 3. Тосты
> 4. Пацанские цитаты
> 5. Рекламные слоганы
> 6. Короткие истории
> 7. Подписи в инсту
> 8. Википедия
> 9. Синопсы Фильмов
> 10. Гороскоп
> 11. Народные мудрости

* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.balayandex_get('Deviant', 9)
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|text - Сгенерированный текст.
----|key - Текст который вы передали.
~~~



***

## <a name="TranslatorEmj"></a> TranslatorEmj (Переводчик текста в эмоджи):
* Метод: translator_emj(text,lang)
* Описание: Переводит текст с английского или русского в эмоджи.
* Параметр 1: text - Слово или предложение, которое необходимо перевести.
* Параметр 2: lang - Язык с которого нужно перевести, поддерживает только _ru_ и _en_
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.translator_emj('Привет','ru')
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|text - переведённый текст.
~~~

***

## <a name="KeyGenerator"></a> KeyGenerator (Генератор ключей):
* Метод: generator()
* Описание: Генерирует случайный ключ.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.generator()
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|code- генерируемый текст
~~~


***

## <a name="GetChatsLink"></a> GetChatsLink (Получает ссылку на чат и информацию по нем.):
* Метод: get_chat_link()
* Автор: https://vk.com/slikkness
* Описание: Получает информацию о случайной беседе и ссылку на вход в нее.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.get_chat_link()
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|name - Название чата.
----|user - Количество участников чата.
----|creator - ID создателя чата.
----|online_admin - Онлайн админ или нет.
----|online_user - Количество частников в онлайне.
----|bots - Массив с ботами в чате.
------|name - Название бота.
------|id - ID бота.
----|link - Ссылка на чат.
~~~

***

## <a name="GetTesterInfo"></a> GetTesterInfo (Проверяет, является ли пользователь тестером вк.):
* Метод: get_tester()
* Параметр 1: id - user_id пользователя вк.
* Описание: Получает информации о карточке тестировщика пользователя.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.get_tester()
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|status - Статус пользователя в программе.
----|ball - Количество баллов.
----|reports  - Количество Репортов.
----|top  - Место в рейтинге.
~~~

***

## <a name="Ping"></a> Ping (Получает информацию о пинге):
* Метод: get_ping()
* Описание: Получает информации о пинге.
* Пример: 
~~~python
from deviant import Deviant

dev = Deviant(doken = 'Ваш DOKEN')

deviant_info = dev.get_ping()
print(deviant_info)
~~~

* Результат:
~~~python
--|deviant - Массив с результатом.
----|ping_vk - Время ответа сервера Вк.
----|ping_deviant - Время ответа сервера Deviant.
~~~