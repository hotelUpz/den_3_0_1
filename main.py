# from tg_interfaces import TG_MANAGER
from main_logic import MAIN_CONTROLLER

def go():
    try:
        MAIN_CONTROLLER().main_func()
        # print('Пожалуйста перейдите в интерфейс вашего телеграм бота!') 
        # bot = TG_MANAGER()
        # bot.run()
    except Exception as ex: 
        print(ex)
if __name__=="__main__":
    go()