import time
import requests
from data import DataApi
from settings import ANSWERS


class Search:
    def __init__(self, user_token, user_id, service_api, client_info, api_version='5.131'):
        self.user_token = user_token
        self.user_id = user_id
        self.api = api_version
        self.data = DataApi(user_token)
        self.serv = service_api
        self.client_info = client_info
        self.answers = ANSWERS

    def check_bdate(self):
        while True:
            bdate = self.serv.receive_m()['text']

            if len(bdate.split('.')) == 3:
                self.client_info['bdate'] = bdate
                return bdate

            else:
                self.serv.send_m(self.answers['error_bdate_input'])
                self.serv.send_m(self.answers['bdate_input_format'])

    def get_bdate(self):
        if not self.client_info.get('bdate'):
            self.serv.send_m(self.answers['error_bdate'])
            self.serv.send_m(self.answers['bdate_input_format'])
            return self.check_bdate()
        elif len(self.client_info['bdate'].split('.')) != 3:
            self.serv.send_m(self.answers['error_bdate'])
            self.serv.send_m(self.answers['bdate_input_format'])
            return self.check_bdate()
        else:
            return self.client_info['bdate']

    def get_search_age(self):
        bdate = self.get_bdate().split('.')
        age = int(time.strftime('%Y')) - int(bdate[-1])
        age_from = str(age - 3)
        age_to = str(age + 3)
        return {'age_from': age_from, 'age_to': age_to}

    def check_relation(self):
        while True:
            relation = self.serv.receive_m()['text']

            relation_types = {'1', '2', '3', '4', '5', '6', '7', '8'}

            if relation in relation_types:
                return relation

            else:
                self.serv.send_m(self.answers['error_relation_input'])
                self.serv.send_m(self.answers['relation_input_format'])

    def get_relation(self):
        if not self.client_info.get('relation'):
            self.serv.send_m(self.answers['error_relation'])
            self.serv.send_m(self.answers['relation_input_format'])
            return self.check_relation()
        else:
            return self.client_info['relation']

    def check_country(self):
        while True:
            input_country = self.serv.receive_m()['text']

            for country in self.data.get_countries_list():
                if country['title'].lower() == input_country.lower():
                    print(country['id'])
                    return country['id']

            else:
                self.serv.send_m(self.answers['error_country_input'])
                self.serv.send_m(self.answers['country_input_format'])

    def get_country(self):
        if not self.client_info.get('country'):
            self.serv.send_m(self.answers['error_country'])
            self.serv.send_m(self.answers['country_input_format'])
            return self.check_country()
        else:
            return self.client_info['country']['id']

    def get_city(self):
        if not self.client_info.get('city'):
            self.serv.send_m(self.answers['error_city'])
            self.serv.send_m(self.answers['city_input_format'])
            input_city = self.serv.receive_m()['text']
            return input_city
        else:
            return self.client_info['city']['title']

    def search_params(self):

        fields = 'id, sex, bdate, city, relation'

        params = {
            'count': '30',
            'age_from': self.get_search_age()['age_from'],
            'age_to': self.get_search_age()['age_to'],
            'country': self.get_country(),
            'hometown': self.get_city(),
            'sex': '2' if self.client_info['sex'] == '1' else '1',
            'status': self.get_relation(),
            'has_photo': '1',
            'access_token': self.user_token,
            'fields': fields,
            'v': self.api
        }

        return params

    def search_users(self):
        method = 'users.search'

        resp_url = f'https://api.vk.com/method/{method}'
        resp = requests.get(resp_url, self.search_params()).json()

        users_pack = {}
        for user in resp['response'].get('items'):

            profile_pics = self.data.get_profile_pics(user['id'])
            if profile_pics:

                attach = ''
                for pic in profile_pics['pics_ids']:
                    attach += f'photo{profile_pics["owner_id"]}_{pic},'

                user_url = f'https://vk.com/id{user["id"]}'
                msg = f'{user["first_name"]} {user["last_name"]} {user_url}'

                users_pack[user['id']] = {
                    'msg': msg,
                    'attach': attach
                }

        return users_pack
