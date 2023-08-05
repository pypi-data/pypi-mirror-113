import requests


'''
███████████████████████████████████████ Author: vk.com/darsox | Серёжа Бухтояров
█────███───██─█─██───██────██─██─██───█ GitHub: https://github.com/DarsoX/Deviant
█─██──██─████─█─███─███─██─██──█─███─██ PyPI: https://pypi.org/project/deviant/
█─██──██───██─█─███─███────██─█──███─██ Groups: https://vk.com/db.user
█─██──██─████───███─███─██─██─██─███─██ Licens: Copyright 2021-2023 deviantapi@gmail.com.
█────███───███─███───██─██─██─██─███─██ Distributed under the Boost Software License, Version 1.0.
███████████████████████████████████████ See https://www.boost.org/LICENSE_1_0.txt
'''



class Deviant(object):
    def __init__(self, doken = '', token = ''):
        super(Deviant, self).__init__()
        if doken != '':
            self.doken = doken
        if token != '':
            self.doken = token

    def stickers_full_get(self,id,type = 1):
        url = 'https://deviantapi.pythonanywhere.com/api/StickersFullGet'

        querystring = {"id":id,"doken":self.doken,'type':type}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def stickers_get(self,id):
        url = 'https://deviantapi.pythonanywhere.com/api/StickersGet'

        querystring = {"id":id,"doken":self.doken}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def stickers_info_get(self,id):
        url = 'https://deviantapi.pythonanywhere.com/api/StickersInfoGet'

        querystring = {"id":id,"doken":self.doken}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def apps_get(self,id):
        url = 'https://deviantapi.pythonanywhere.com/api/AppsGet'

        querystring = {"id":id}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def groups_get(self,id):
        url = 'https://deviantapi.pythonanywhere.com/api/GroupsGet'

        querystring = {"id":id}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def balayandex_get(self,text,style = 0):

        url = 'https://deviantapi.pythonanywhere.com/api/BlaYandex'

        querystring = {"text":text, 'style': style}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def translator_emj(self,text,lang = 'ru'):

        url = 'https://deviantapi.pythonanywhere.com/api/TranslatorEmj'

        querystring = {"text":text, 'lang': lang}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def generator(self):

        url = 'https://deviantapi.pythonanywhere.com/api/KeyGenerator'

        querystring = {}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

    def get_chat_link(self):

        #Method author: https://vk.com/slikkness

        url = 'https://deviantapi.pythonanywhere.com/api/ChatsLink'

        querystring = {}

        payload = ""
        response = requests.request("POST", url, data=payload, params=querystring)

        return response.json()

