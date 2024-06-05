from variables import PARAMS
import telebot
from telebot import types
import time

class TG_CONNECTOR(PARAMS):
    def __init__(self) -> None:
        super().__init__()
        # print(TG_TOKEN)      
        self.bot = telebot.TeleBot(self.tg_api_token)
        # print(self.bot)
        self.menu_markup = self.create_menu()
        self.last_message = None
  
    def create_menu(self):
        menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("START")
        button2 = types.KeyboardButton("GO")
        button3 = types.KeyboardButton("STOP")
        # button4 = types.KeyboardButton("SEARCH COINS")
        button5 = types.KeyboardButton("SET TIME_FRAME")
        button6 = types.KeyboardButton("SET DEPO/LEVERAGE")
        button7 = types.KeyboardButton("INDICATORS")
        button8 = types.KeyboardButton("TP/SL")
        button9 = types.KeyboardButton("MARTIN GALE")
        button10 = types.KeyboardButton("DOCUMENTATION")    
        menu_markup.add(button1, button2, button3, button5, button6, button7, button8, button9, button10)        
        return menu_markup

    def connector_func(self, message, response_message):
        retry_number = 3
        decimal = 1.1       
        for i in range(retry_number):
            try:
                self.bot.send_message(message.chat.id, response_message)                
                return message.text
            except Exception as ex:
                print(ex)
                time.sleep(1.1 + i*decimal)                   
        return None
