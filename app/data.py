import requests


class DataApi:
    def __init__(self, user_token, api_version='5.131'):
        self.user_token = user_token
        self.api = api_version

    def get_countries_list(self):
        method = 'database.getCountries'

        params = {
            'need_all': '1',
            'count': '235',
            'access_token': self.user_token,
            'v': self.api
        }

        resp_url = f'https://api.vk.com/method/{method}'

        return requests.get(resp_url, params).json()['response']['items']

    def get_cities_list(self, country_id):
        method = 'database.getCities'

        params = {
            'country_id': country_id,
            'need_all': '0',
            'count': '30',
            'access_token': self.user_token,
            'v': self.api
        }
        resp_url = f'https://api.vk.com/method/{method}'

        return requests.get(resp_url, params).json()['response']['items']

    def get_user_info(self, user_id):
        try:
            method = 'users.get'

            fields = """
            sex, bdate, city, country, relation,
            movies, music, books, interests
            """

            params = {
                'user_ids': user_id,
                'access_token': self.user_token,
                'fields': fields,
                'v': self.api
            }

            resp_url = f'https://api.vk.com/method/{method}'
            resp = requests.get(resp_url, params).json()

            return resp['response'][0]

        except IndexError:
            return False

        except KeyError:
            return False

    def get_profile_pics(self, user_id):
        method = 'photos.get'

        params = {
            'user_id': user_id,
            'album_id': 'profile',
            'extended': '1',
            'access_token': self.user_token,
            'v': self.api
        }

        resp_url = f'https://api.vk.com/method/{method}'
        resp = requests.get(resp_url, params).json()

        pics_pack = {}
        try:
            popular_pics = sorted(
                resp['response']['items'],
                key=lambda k: k['likes']['count'] + k['comments']['count'],
                reverse=True
            )[0:3]
            for pic in popular_pics:
                if 'owner_id' not in pics_pack.keys():
                    pics_pack['owner_id'] = pic['owner_id']
                    pics_pack['pics_ids'] = []
                pics_pack['pics_ids'].append(pic['id'])

        except KeyError:
            pass

        finally:
            return pics_pack
