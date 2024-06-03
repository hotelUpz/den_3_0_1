from tg_interfaces import TG_MANAGER
from main_logic import MAIN_CONTROLLER
from SETTINGS import is_terminal_only 

def go():
    try:
        if is_terminal_only:
            MAIN_CONTROLLER().main_func()
        else:
            print('Пожалуйста перейдите в интерфейс вашего телеграм бота!') 
            bot = TG_MANAGER()
            bot.run()
    except Exception as ex: 
        print(ex)
if __name__=="__main__":
    go()