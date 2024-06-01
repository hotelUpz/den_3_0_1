from tg_interfaces import TG_MANAGER

def go():
    try:
        print('Пожалуйста перейдите в интерфейс вашего телеграм бота!') 
        bot = TG_MANAGER()
        bot.run()
    except Exception as ex: 
        print(ex)
if __name__=="__main__":
    go()