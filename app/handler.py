from app.service import ServiceApi
from app.data import DataApi
from app.search import Search
from app.base import ResultsBase


class Handler:
    def __init__(self, community_token, user_token, answers, user_id='', client_id='', api_version='5.131'):
        self.comm_token = community_token
        self.user_token = user_token
        self.answers = answers
        self.user_id = user_id
        self.client_id = client_id
        self.api = api_version
        self.search = None
        self.base = None
        self.serv = ServiceApi(community_token)
        self.data = DataApi(user_token)

    def main_menu(self):
        while True:
            msg = self.serv.receive_m()

            self.serv.bot_user = msg['from_id']

            command = msg['text']
            if command == 'начать':
                self.serv.send_m(self.answers['first_hello'])
                self.serv.send_m(self.answers['second_hello'])

                while True:
                    client_id = self.serv.receive_m()['text']
                    client_info = self.data.get_user_info(client_id)

                    if client_info:
                        self.client_id = client_info.get('id')
                        self.search = Search(self.user_token, self.user_id, self.serv, client_info)
                        self.base = ResultsBase(self.client_id)
                        self.serv.send_m(self.answers['client_found'])

                        if self.base.is_saved():
                            self.serv.send_m(self.answers['saved'])
                        self.search_menu()

                    else:
                        self.serv.send_m(self.answers['client_error'])

            else:
                self.serv.send_m(self.answers['main_command_error'])

    def search_menu(self):
        for vk_user_id, result in self.search.search_users().items():
            if not self.base.is_shown(vk_user_id):

                self.base.add_shown(vk_user_id)

                self.serv.send_m(result['msg'], result['attach'])
                self.serv.send_m(self.answers['search_next'])

                while True:
                    command = self.serv.receive_m()['text']
                    if command == 'дальше':
                        break
                    elif command == 'помощь':
                        self.serv.send_m(self.answers['search_help'])
                    elif command == 'выход':
                        self.serv.send_m(self.answers['search_finish'])
                        return
                    else:
                        self.serv.send_m(self.answers['search_command_error'])

        else:
            self.serv.send_m(self.answers['users_shown'])
            return
