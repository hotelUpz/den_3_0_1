from RISK_MANAGMENT.tp_sl_startegies import TAKE_PROFIT_STOP_LOSS_STRATEGIES
import time
import os
import inspect
current_file = os.path.basename(__file__)

class ENGINS(TAKE_PROFIT_STOP_LOSS_STRATEGIES):
    def __init__(self):
        super().__init__()
        # устанавливаем функциии декораторы
        self.engin_1_2 = self.log_exceptions_decorator(self.engin_1_2)

    def engin_1_2(self, coins_list):
        try:
            if self.is_trailing_stop_start:  
                if not self.trailing_tp_sl_shell(self.executed_qty, self.enter_price, self.stop_loss_ratio, self.price_precession, self.last_signal_val):
                    msg = "Что-то пошло не так... закройте позицию вручную!!"
                    self.handle_messagee(msg)
                    return False
                self.in_position = False
                self.is_trailing_stop_start = False
                self.last_signal_val = None
                self.wait_candle_flag = True
                return True      
            # /////////////// проверка открыта ли позиция:
            if self.in_position:
                if self.is_closing_position_true(self.symbol):
                    # //////////////////// дополнительные действия после закрытия позиции (отмена оставшихся ордеров, анализ сделки и короткий отчет)
                    self.in_position = False
                    self.is_trailing_stop_start = False
                    self.close_position_utilites(
                        self.last_signal_val
                    )
                    self.last_signal_val = None
                    self.wait_candle_flag = True
                    msg = "Бот ищет следующий сигнал"
                    self.handle_messagee(msg)
                    return True
            else:                            
                # # ////////////// ищем сигнал если закрыта:                
                # start_time = int(time.time()*1000)
                # print("начало поиска сигнала")
                # print(f"coins_list_len: {len(coins_list)}")
                try:
                    self.symbol, self.current_signal_val, self.cur_price, self.cur_klines_data = self.get_signals(self.indicators_strategy_list, coins_list, self.ema1_period, self.ema2_period, self.ema_trend_line, self.stoch_rsi_over_sell, self.stoch_rsi_over_buy)
                except Exception as ex: 
                    pass 
                    # self.symbol, self.current_signal_val, self.cur_price, self.cur_klines_data = None, None, None, None                 
                    # self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}") 
                # delta_time = int((int(time.time()*1000) - start_time)/ 1000)
                # print(f"конец поиска сигнала: {delta_time} сек")             
                if not self.current_signal_val:                    
                    # self.handle_messagee("нет сигнала")
                    self.is_no_signal_counter += 1
                    if self.is_no_signal_counter % self.show_absent_or_signal_every == 0:
                        msg = f"Нет сигнала на протяжение {self.is_no_signal_counter} минут"
                        self.handle_messagee(msg)  
             
            # //////////////// анализ сигнала:
            if self.current_signal_val:
                self.is_no_signal_counter = 0
                # ///////////////// сообщение о сигнале:
                self.handle_messagee(f"Монета: {self.symbol}")
                self.handle_messagee(self.current_signal_val)
                self.last_signal_val = self.current_signal_val
                self.for_set_open_position_temp()
                                        
                if self.qty == "Too_litle_size":
                    msg = "Размер депозита для данной монеты слишком мал. Ищем другую монету"
                    self.handle_messagee(msg)
                    self.black_coins_list.append(self.symbol)
                    self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]
                    self.wait_candle_flag = True
                    return 2
                
                if not self.make_orders_template_shell():
                    self.black_coins_list.append(self.symbol)
                    self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]
                    self.wait_candle_flag = True
                    return 2
                # //////////// вычисляем стопы:
                self.enter_price, self.executed_qty = self.for_set_stops_orders_temp(self.response_trading_list, self.qty, self.cur_price)
                self.stop_loss_ratio = self.calculate_stop_loss_ratio(
                    self.direction, self.enter_price, self.cur_klines_data,
                    self.stop_loss_ratio_mode, self.static_stop_loss_ratio_val,
                    self.min_default_ratio, self.max_default_ratio
                )

                self.handle_messagee(f"стоп лосс коэффициент: {self.stop_loss_ratio}")
                if self.stop_loss_global_type == 2:
                    self.in_position = self.fixed_sl_strategy(self.enter_price, self.executed_qty, self.stop_loss_ratio)
                    # ////////////
                    if not self.in_position:
                        # /////// логика остановки бота на случай если не удалось нормально установить стопы:
                        msg = "Не удалось установить стопы... закройте позицию вручную!!"
                        self.handle_messagee(msg)
                        return False
                # /////////////
                # обнуляем сигнал для 1, 2 стратегий стоп лосса. Переходим на следующую итерацию
                self.current_signal_val = None
                if self.stop_loss_global_type == 1:
                    self.is_trailing_stop_start = True # -- флаг входа в трейлинг стоп
            return True
        except Exception as ex:                   
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
        return False
    
class MAIN_CONTROLLER(ENGINS):
    def __init__(self):  
        super().__init__()

    def main_func(self):
        # self.last_date = self.date_of_the_month()        
        empty_candidate_list_counter = 0
        engin_answ = None
        trade_params_mess = (
            f"Текущие параметры стратегии:\n"
            f"Стратегия индикатора: {self.indicators_strategy_text_patterns[f'{self.indicators_strategy_number}']}\n"
            f"Стратегия TP/SL: {self.stop_loss_global_type_text_patterns[f'{self.stop_loss_global_type}']}\n"
            f"Способ расчета стоп лосс коэффициента: {self.stop_loss_ratio_mode_text_patterns[f'{self.stop_loss_ratio_mode}']}\n"
            f"Значение статического стоп лосс коэффициента: {self.static_stop_loss_ratio_val}\n"
            f"Минимальное значение стоп лосс коэффициента: {self.min_default_ratio}\n"
            f"Максимальное значение стоп лосс коэффициента: {self.max_default_ratio}\n" 
            f"Тайм фрейм: {self.interval}\n"            
            f"Соотношение риска к прибыли (только для фиксированного типа стоп лосса): {self.risk_reward_ratio}"
        )
        self.handle_messagee(trade_params_mess)      
        martin_gale_status = "включен" if self.martin_gale_flag else "отключен"
        self.handle_messagee(f"Мартин Гейл {martin_gale_status}") 
        if self.martin_gale_flag and self.max_martin_gale_counter_auto_true:
            self.is_martin_gale_true_template()
        get_coins_counter = 0
        get_coins_counter_reset_until = 30
        is_show_statistic_true, next_show_statistic_time = None, None
        next_show_statistic_time = self.get_next_show_statistic_time()

        while True:

            if self.losses_counter == self.losses_until_value:
                self.stop_bot_flag = True
                self.handle_messagee(f"Количество неудачных сделок достигло лимита {self.losses_until_value}!! Рекомендуем пересмотреть торговую стратегию или изменить настройки бота!")
            
            if self.stop_bot_flag:
                msg = "Bot остановлен!"
                self.handle_messagee(msg)
                self.run_flag = False                
                return
            
            # ////////////// отчет суточной статистики: 
            is_show_statistic_true, next_show_statistic_time = self.show_statistic_signal(next_show_statistic_time)
            if is_show_statistic_true:
                result_string = ""
                result_string = self.statistic_calculations(self.daily_trade_history_list)
                if result_string:
                    self.handle_messagee(f"Показатели торгов за сутки:\n{result_string}")                    
                else:
                    self.handle_messagee("Нет данных для показа статистики")
                self.daily_trade_history_list = []

            if self.wait_candle_flag:
                self.wait_candle_flag = False
                wait_time = self.time_calibrator(self.kline_time, self.time_frame)
                msg = f"Ждем закрытия последней {self.interval} свечи. Осталось {round(wait_time/60, 2)} минут"
                self.handle_messagee(msg)
                self.candidate_symbols_list = self.get_top_coins_template()
                self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]
                # mess_resp = 'Список монет кандидатов:\n' + '\n'.join(self.candidate_symbols_list)
                # self.handle_messagee(mess_resp)
            else:
                wait_time = self.time_calibrator(1, 'm') if not self.in_position else 30    
            time.sleep(wait_time)
            get_coins_counter += 1
            if get_coins_counter == get_coins_counter_reset_until:
                self.candidate_symbols_list = self.get_top_coins_template()
                self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]
                get_coins_counter = 0           

            if self.stop_loss_global_type in [1,2]:                
                if self.candidate_symbols_list:
                    engin_answ = self.engin_1_2(self.candidate_symbols_list)
                    if not engin_answ:
                        self.stop_bot_flag = True
                        continue
                else:
                    empty_candidate_list_counter += 1 
                if empty_candidate_list_counter == 30:
                    self.handle_messagee("Список монет кандидатов пуст на протяжение 30 попыток поиска...")
                    empty_candidate_list_counter = 0

