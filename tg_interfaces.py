from main_logic import MAIN_CONTROLLER
import os
import inspect
current_file = os.path.basename(__file__)

class TG_MANAGER(MAIN_CONTROLLER):
    def __init__(self):
        super().__init__()  
        self.stop_redirect_flag = False  
        self.trades_data_redirect_flag = False
        self.set_time_frame_flag = False
        self.martin_gale_redirect_flag = False
        self.indicators_redirect_flag = False
        self.set_time_ema_periods_flag = False
        self.tp_sl_redirect_flag = False
        self.add_in_dlack_list_flag = False
        self.documentation_redirect_flag = False

    def run(self):  
        try: 
            @self.bot.message_handler(commands=['start'])
            @self.bot.message_handler(func=lambda message: message.text == 'START')
            def handle_start_input(message):
                if self.block_acess_flag:
                    response_message = "Это вам не пароль от вифи взламывать!!!"
                    message.text = self.connector_func(message, response_message)
                else:   
                    self.start_day_date = self.date_of_the_month()          
                    self.bot.send_message(message.chat.id, "Пожалуйста введите код доступа..", reply_markup=self.menu_markup)                   
                    self.stop_bot_flag = False
                    self.start_flag = True

            @self.bot.message_handler(func=lambda message: self.start_flag)
            def handle_start_redirect(message): 
                self.start_flag = False               
                try:
                    cur_day_date = None                    
                    value_token = message.text.strip()
                    cur_day_date = self.date_of_the_month()

                    if self.start_day_date != cur_day_date:
                        self.start_day_date = cur_day_date
                        self.block_acess_flag = False
                        self.block_acess_counter = 0

                    if value_token == self.seq_control_token and not self.block_acess_flag:
                        self.seq_control_flag = True  
                        # ////////////////////////////////////////////////////////////////////
                        try:                                                       
                            # self.bot.send_message(message.chat.id, response_message, reply_markup=self.menu_markup)
                            self.last_message = message
                            if self.run_flag:
                                message.text = self.connector_func(message, "Сперва остановите робота ..")
                            else:
                                message.text = self.connector_func(message, "Здравствуйте! Для начала работы выберите одну из опций.(Начать торговлю нажмите 'GO')")                               
                                # self.main_func() 
                        except Exception as ex: 
                            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
                        # ////////////////////////////////////////////////////////////////////                       

                    elif value_token != self.seq_control_token and not self.block_acess_flag:                               
                        self.block_acess_counter += 1
                        if self.block_acess_counter >= self.veryf_attemts_number:
                            self.block_acess_flag = True                            
                            response_message = "Попытки доступа исчерпаны. Попробуйте в другой раз"
                            message.text = self.connector_func(message, response_message)
                        else:
                            response_message = "Пожалуйста введите действителный код доступа"
                            message.text = self.connector_func(message, response_message)
                except Exception as ex: 
                    self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'GO')             
            def handle_go(message):
                if self.seq_control_flag:                    
                    if self.run_flag:
                        message.text = self.connector_func(message, "Сперва остановите робота ..")
                    else:                                    
                        self.bot.send_message(message.chat.id, f'Да благословит вас Бог {self.my_name}!')
                        self.default_tg_vars() 
                        self.init_some_params()
                        self.init_main_file_variables()
                        self.run_flag = True
                        self.seq_control_flag = True
                        self.stop_bot_flag = False
                        self.last_message = message
                        self.main_func()
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")      
            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'STOP')             
            def handle_stop(message):
                if self.seq_control_flag:
                    self.last_message = message
                    self.bot.send_message(message.chat.id, "Остановить бота? (y/n)")
                    self.stop_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.stop_redirect_flag)             
            def handle_stop_redirect(message):
                self.last_message = message
                self.stop_redirect_flag = False
                if message.text.strip().upper() == 'Y':                    
                    self.stop_bot_flag = True 
                    self.bot.send_message(message.chat.id, "Немного подождите...")                   
                else:
                    self.bot.send_message(message.chat.id, "Бот не был остановлен...") 
            # /////////////////////////////////////////////////////////////////////////////// 
            @self.bot.message_handler(func=lambda message: message.text == 'SET TIME_FRAME')             
            def handle_set_timeFrame(message):
                self.last_message = message               
                if self.seq_control_flag:
                    self.set_time_frame_flag = True
                    self.bot.send_message(message.chat.id, "Введите таймфрейм. Напиример '5m' или '1h' (без пробелов)")
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.set_time_frame_flag)             
            def handle_set_timeFrame_redirect(message):
                self.set_time_frame_flag = False
                dataa = message.text.strip()
                self.kline_time = int(float(dataa[:-1]))
                self.time_frame = dataa[-1]
                self.interval = str(self.kline_time) + self.time_frame   
                self.bot.send_message(message.chat.id, f"Тайм фрейм изменен и составляет {self.interval}")         
            # ////////////////////////////////////////////////////////////////////////////
            # # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'SET DEPO/LEVERAGE')             
            def handle_trades_data(message):
                self.last_message = message
                if self.seq_control_flag:
                    self.bot.send_message(message.chat.id, "Введите размер депозита (в usdt) и кредитное плечо. Например: 20 2")
                    self.trades_data_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.trades_data_redirect_flag)             
            def handle_trades_data_redirect(message):
                # self.last_message = message
                self.trades_data_redirect_flag = False
                dataa = [x for x in message.text.split(' ') if x and x.strip()]              
                self.start_depo = self.depo = round(float(dataa[0]), 2)
                self.lev_size = int(float(dataa[1])) 
                self.bot.send_message(message.chat.id, f"Текущий депозит: {self.depo}")
                if self.set_leverage_template():
                    self.bot.send_message(message.chat.id, f"Текущее кредитное плечо: {self.lev_size}")                    
                else:
                    self.bot.send_message(message.chat.id, f"Не удалось установить кредитное плеч...") 
                
                self.was_change_leverage_true = True
            # /////////////////////////////////////////////////////////////////////////////// 

            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'MARTIN GALE')             
            def handle_martin_gale(message):
                self.last_message = message
                if self.seq_control_flag:
                    self.bot.send_message(message.chat.id, "Введите через пробел флаг МАртин Гейла (1 или 0), множитель депозита (например 2) и счетчик Мартин Гейла (до скольки раз умножиать позицию). Пример ввода: 0 2 3")
                    self.martin_gale_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.martin_gale_redirect_flag)             
            def handle_martin_gale_redirect(message):
                # self.last_message = message
                self.martin_gale_redirect_flag = False
                dataa = [x for x in message.text.split(' ') if x and x.strip()]
                self.martin_gale_flag = int(float(dataa[0]))
                self.martin_gale_ratio = float(dataa[1])
                self.max_martin_gale_counter = float(dataa[2]) 
                self.bot.send_message(message.chat.id, f"Изменились следующие настройки Мартин Гейла:\nmartin_gale_flag: {self.martin_gale_flag}\nmartin_gale_ratio: {self.martin_gale_ratio}\nmax_martin_gale_counter: {self.max_martin_gale_counter}")

            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'INDICATORS')             
            def handle_indicators(message):
                self.last_message = message
                if self.seq_control_flag:
                    self.bot.send_message(message.chat.id, "Введите номер стратегии индикатора")
                    self.indicators_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.indicators_redirect_flag)             
            def handle_indicators_redirect(message):
                # self.last_message = message
                self.indicators_redirect_flag = False
                self.indicators_strategy_number = int(float(message.text.strip()))
                self.ema_settings()
                self.bot.send_message(message.chat.id, f"Текущий номер стратегии индикатора: {self.indicators_strategy_number}")

            # /////////////////////////////////////////////////////////////////////////////// 
            @self.bot.message_handler(func=lambda message: message.text == 'SET EMA PERIOD')             
            def handle_set_ema_periods(message):
                self.last_message = message               
                if self.seq_control_flag:
                    self.set_time_ema_periods_flag = True
                    self.bot.send_message(message.chat.id, "Введите длины волн через пробел. Например: 5, 20, 200. Где 200 - длина тренда")
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.set_time_ema_periods_flag)             
            def handle_set_ema_periods_redirect(message):
                self.set_time_ema_periods_flag = False
                dataa = [x for x in message.text.split(' ') if x and x.strip()]
                self.ema1_period = int(float(dataa[0]))
                self.ema2_period = int(float(dataa[1]))
                self.ema_trend_line = int(float(dataa[2]))
                self.ema_settings()
                self.bot.send_message(message.chat.id, f"Настройки волн EMA применены успешно!")         
            # ////////////////////////////////////////////////////////////////////////////
            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'TP/SL')             
            def handle_tp_sl(message):
                self.last_message = message
                if self.seq_control_flag:
                    self.bot.send_message(message.chat.id, "Введите через пробел номер глобальной стратегии TP/SL (1 или 2), способ расчета стоп лосс коэффициента (1 - 7), значение статического стоп лосс коэффициента в процентах, например 1 и соотношение риска к прибыли (1:4). Пример ввода: 2 1 0.5 1:4")
                    self.tp_sl_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.tp_sl_redirect_flag)             
            def handle_tp_sl_redirect(message):
                # self.last_message = message
                self.tp_sl_redirect_flag = False
                dataa = [x for x in message.text.split(' ') if x and x.strip()]
                self.stop_loss_global_type = int(float(dataa[0]))
                self.stop_loss_ratio_mode = int(float(dataa[1]))
                self.static_stop_loss_ratio_val = float(dataa[2])
                self.risk_reward_ratio = dataa[3]
                self.bot.send_message(message.chat.id, "Настройки стоп лосс стратегии применены успешно!")  

            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'ADD TO BLACK LIST')             
            def handle_add_in_dlack_list(message):
                self.last_message = message
                if self.seq_control_flag:
                    if self.run_flag:                            
                        self.bot.send_message(message.chat.id, "Введите монету которую хотите внести в черный список. Напиример etcusdt")
                        self.add_in_dlack_list_flag = True
                    else:
                        message.text = self.connector_func(message, "Сперва запустите робота командой 'GO'")                   
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.add_in_dlack_list_flag)             
            def handle_add_in_dlack_list_redirect(message):
                self.add_in_dlack_list_flag = False
                black_coin = None
                black_coin = message.text.strip().upper()
                self.black_coins_list.append(black_coin)
                self.bot.send_message(message.chat.id, f"Монета {black_coin} была добавлена в черный список. Текущий черный список: {self.black_coins_list}")

            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'DOCUMENTATION')             
            def handle_documentation(message):
                self.last_message = message
                if self.seq_control_flag:
                    self.bot.send_message(message.chat.id, "Введите соответствующий номер интересующего вас вопроса:\n1 -- Стратегии индикаторов\n2 -- Стратегии TP/SL\n3 -- Способы расчета стоп лосс коэффициента")
                    self.documentation_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.documentation_redirect_flag)             
            def handle_documentation_redirect(message):
                self.documentation_redirect_flag = False
                dataa = message.text.strip()
                mess = ""
                if dataa == '1':
                    mess = self.indicators_documentation.__doc__
                elif dataa == '2':
                    mess = self.tp_sl_strategies_documenttion.__doc__
                elif dataa == '3':
                    mess = self.sl_ratio_documentation.__doc__
                else:
                    mess = "Нажмите кнопку заново и введите корректные данные"                 
                if mess:
                    self.bot.send_message(message.chat.id, mess)                
            # self.bot.polling()
            self.bot.infinity_polling()
        except Exception as ex:
            print(ex)
            # self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")