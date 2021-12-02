import random
import requests


class ServiceApi:

    def __init__(self, community_token, bot_user=None, api_version='5.131'):
        self.bot_user = bot_user
        self.comm_token = community_token
        self.api = api_version

    def get_group_id(self):
        method = 'groups.getById'

        params = {
            'access_token': self.comm_token,
            'v': self.api
        }
        resp_url = f'https://api.vk.com/method/{method}'

        return requests.get(resp_url, params).json()['response'][0]['id']

    def get_longpoll_server(self):
        method = 'groups.getLongPollServer'

        params = {
            'group_id': self.get_group_id(),
            'access_token': self.comm_token,
            'v': self.api
        }
        resp_url = f'https://api.vk.com/method/{method}'

        return requests.get(resp_url, params).json()['response']

    def receive_m(self):
        longpoll = self.get_longpoll_server()

        while True:
            resp_url = f'{longpoll["server"]}?act=a_check&key={longpoll["key"]}&ts={longpoll["ts"]}&wait=20'

            resp = requests.get(resp_url).json()
            updates = resp['updates']
            if updates:
                for update in updates:
                    if update['type'] == 'message_new':
                        message = {
                            'from_id': update['object']['message']['from_id'],
                            'text': update['object']['message']['text'].lower()
                        }
                        return message

            longpoll['ts'] = resp['ts']

    def send_m(self, msg=None, attach=None):
        method = 'messages.send'

        params = {
            'user_id': self.bot_user,
            'access_token': self.comm_token,
            'message': msg,
            'attachment': attach,
            'random_id': random.randint(0, 10000),
            'v': self.api
        }
        resp_url = f'https://api.vk.com/method/{method}'

        return requests.get(resp_url, params).json()
