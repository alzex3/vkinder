from app.handler import Handler
from settings import COMMUNITY_TOKEN, USER_TOKEN, ANSWERS

if __name__ == '__main__':
    bot = Handler(COMMUNITY_TOKEN, USER_TOKEN, ANSWERS)
    bot.main_menu()
