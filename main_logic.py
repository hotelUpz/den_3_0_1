from RISK_MANAGMENT.tp_sl_startegies import TAKE_PROFIT_STOP_LOSS_STRATEGIES
import time
from datetime import datetime as dttm
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
                if not self.trailing_tp_sl_shell(self.executed_qty, self.enter_price, self.stop_loss_ratio, self.price_precession, self.last_signal_val, self.sl_risk_reward_multiplier, self.sl_order_id):
                    if not self.stop_bot_flag:
                        msg = "В процессе вебсокет-мониторинга цены возникли какие-то проблемы..."
                        self.handle_messagee(msg)
                    return False
                self.in_position = False
                self.is_trailing_stop_start = False
                if (not self.classikal_martin_gale) or (self.last_win_los != -1):
                    self.last_signal_val = None
                    self.wait_candle_flag = True
                self.order_id = None
                self.sl_order_id, self.tp_order_id = None, None
                self.last_stop_loss_price = None
                self.target_tp_price = None
                return True      
            # /////////////// проверка открыта ли позиция:
            if self.in_position:
                if self.is_closing_position_true(self.symbol):
                    # //////////////////// дополнительные действия после закрытия позиции (отмена оставшихся ордеров, анализ сделки и короткий отчет)
                    self.in_position = False
                    self.close_position_utilites(
                        self.last_signal_val
                    )
                    if (not self.classikal_martin_gale) or (self.last_win_los != -1):
                        self.last_signal_val = None
                        self.wait_candle_flag = True
                    self.order_id = None
                    self.sl_order_id, self.tp_order_id = None, None
                    self.last_stop_loss_price = None
                    self.target_tp_price = None
                    msg = "Бот ищет следующий сигнал"
                    self.handle_messagee(msg)
                    return True
            elif not self.retry_trade:                            
                # ////////////// ищем сигнал если закрыта:                
                start_time = int(time.time()*1000)
                print("начало поиска сигнала")
                print(f"coins_list_len: {len(coins_list)}")
                try:
                    self.symbol, self.current_signal_val, self.cur_price, self.cur_klines_data = self.get_signals(self.indicators_strategy_list, coins_list, self.ema1_period, self.ema2_period, self.ema_trend_line, self.stoch_rsi_over_sell, self.stoch_rsi_over_buy)
                    # print(self.symbol, self.current_signal_val, self.cur_price, self.cur_klines_data)
                except Exception as ex: 
                    pass           
                    # self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}") 
                delta_time = int((int(time.time()*1000) - start_time)/ 1000)
                print(f"конец поиска сигнала: {delta_time} сек")             
                if not self.current_signal_val:                    
                    # self.handle_messagee("нет сигнала")
                    self.is_no_signal_counter += 1
                    if self.is_no_signal_counter % self.show_absent_signal_interval == 0:
                        msg = f"Нет сигнала на протяжение {self.is_no_signal_counter} минут"
                        self.handle_messagee(msg)  
             
            # //////////////// анализ сигнала:
            if self.current_signal_val or self.retry_trade:
                self.retry_trade = False
                self.is_no_signal_counter = 0
                if (self.classikal_martin_gale) and (self.last_win_los == -1):
                    self.current_signal_val = self.last_signal_val                
                # Определяем тип сигнала
                signal_type = "LONG_SIGNAL" if self.current_signal_val == 1 else "SHORT_SIGNAL"
                
                # Сообщения о сигнале
                self.handle_messagee(f"Монета: {self.symbol}")
                self.handle_messagee(f"Наден: {signal_type}")
                
                # Проверяем реверс
                if (self.is_reverse_signal == -1) and ((not self.classikal_martin_gale) or (self.last_win_los != -1) or (self.is_reverse_defencive_mehanizm)):
                    reversed_signal_type = "LONG_SIGNAL" if self.current_signal_val == -1 else "SHORT_SIGNAL"
                    self.handle_messagee(f"Применяем {reversed_signal_type} так как включен реверс")
                    self.current_signal_val *= self.is_reverse_signal                
                # ///
                now_time = dttm.now(self.local_tz)
                ssignal_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
                self.handle_messagee(f"Время сигнала: {ssignal_time}")
                # /////
                self.last_signal_val = self.current_signal_val

                if (self.classikal_martin_gale) and (self.last_win_los == -1):
                    self.cur_klines_data = self.get_klines(self.symbol, self.interval, self.ema_trend_line)
                    self.cur_price = self.cur_klines_data['Close'].iloc[-1]

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
                    self.current_signal_val, self.enter_price, self.cur_klines_data,
                    self.stop_loss_ratio_mode, self.static_stop_loss_ratio_val,
                    self.min_default_ratio, self.max_default_ratio
                )

                self.handle_messagee(f"стоп лосс коэффициент: {self.stop_loss_ratio}")

                standart_sl_tp_set_orders_template_resp = self.standart_sl_tp_set_orders_template(self.enter_price, self.executed_qty, self.stop_loss_ratio, self.current_signal_val)
                if standart_sl_tp_set_orders_template_resp:
                    self.in_position, self.sl_risk_reward_multiplier, _, self.sl_order_id, self.tp_order_id = standart_sl_tp_set_orders_template_resp
                    # print(f"self.tp_order_id: {self.tp_order_id}")
                    # print(self.in_position, self.sl_risk_reward_multiplier, _, self.sl_order_id)

                if not self.in_position:
                    # /////// логика остановки бота на случай если не удалось нормально установить стопы:
                    msg = "Не удалось установить стопы... закройте позицию вручную!!"
                    self.handle_messagee(msg)
                    return False

                if self.stop_loss_global_type == 1:
                    self.is_trailing_stop_start = True # -- флаг входа в трейлинг стоп
                self.current_signal_val = None
            return True
        except Exception as ex:                   
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
        return False
    
class MAIN_CONTROLLER(ENGINS):
    def __init__(self):  
        super().__init__()

    def stratigiee_info(self):
        asnty_strategyy = "да" if self.is_reverse_signal == -1 else "нет"
        is_proxyy = "да" if self.is_proxies_true else "нет"
        trade_params_mess = (
            f"Текущие параметры стратегии:\n"
            f"Стратегия индикатора: {self.indicators_strategy_number} -- {self.indicators_strategy_text_patterns[f'{self.indicators_strategy_number}']}\n"
        )

        if self.indicators_strategy_number not in [8,9]:
            trade_params_mess += (
                f"Длина короткой EMA: {self.ema1_period}\n"
                f"Длина длинной EMA: {self.ema2_period}\n"                
            )

        if self.indicators_strategy_number in [2, 4, 6, 7, 9]:
            trade_params_mess += (
                f"Длина тренда EMA: {self.ema_trend_line}\n"
            )
        if self.indicators_strategy_number in [5, 6]:
            trade_params_mess += (
                f"Уровень перепроданности stoch_rsi: {self.stoch_rsi_over_sell}\n"
                f"Уровень перекупленности stoch_rsi: {self.stoch_rsi_over_buy}\n"
            )
        trade_params_mess += (
            f"Антистратегия (противоположный сигнал): {asnty_strategyy}\n"
            f"Прокси соединение: {is_proxyy}\n"            
            f"Стратегия TP/SL: {self.stop_loss_global_type} -- {self.stop_loss_global_type_text_patterns[f'{self.stop_loss_global_type}']}\n"
            f"Способ расчета стоп лосс коэффициента: {self.stop_loss_ratio_mode} -- {self.stop_loss_ratio_mode_text_patterns[f'{self.stop_loss_ratio_mode}']}\n"
        )

        if self.stop_loss_ratio_mode == 1:
            trade_params_mess += f"Значение статического стоп лосс коэффициента: {self.static_stop_loss_ratio_val}\n"
        else:
            trade_params_mess += (
                f"Минимальное значение стоп лосс коэффициента: {self.min_default_ratio}\n"
                f"Максимальное значение стоп лосс коэффициента: {self.max_default_ratio}\n"
            )

        martin_gale_status = "включен" if self.martin_gale_flag else "отключен"        
        trade_params_mess += (
            f"Тайм фрейм: {self.interval}\n"
            f"Соотношение риска к прибыли: {self.risk_reward_ratio}\n"
            f"Мартин Гейл {martin_gale_status}\n"
        )
        
        if self.martin_gale_flag:
            if self.losses_until_value <= self.max_martin_gale_counter:
                self.losses_until_value = self.max_martin_gale_counter + 1
            martin_gale_auto_countt = "да" if self.max_martin_gale_counter_auto_true == 1 else "нет"
            play_by_leveragee = "да" if self.play_by_leverage == 1 else "нет"
            if self.martin_gale_flag and self.max_martin_gale_counter_auto_true:
                self.is_martin_gale_true_template()
            trade_params_mess += (  
                f"Классический Мартин Гейл: {'да' if self.classikal_martin_gale else 'нет'}\n"              
                f"Множитель Мартин Гейла: {self.martin_gale_ratio}\n"
                f"Автоматически расчитывать допустимый счетчик Мартин Гейла: {martin_gale_auto_countt}\n"
                f"Счетчик Мартин Гейла (сколько раз умножать позицию): {self.max_martin_gale_counter}\n"
                f"Умножать депозит за счет кредитных плечей: {play_by_leveragee}\n"
            )

        self.handle_messagee(trade_params_mess)

    def main_func(self):
        # self.last_date = self.date_of_the_month()        
        empty_candidate_list_counter = 0
        engin_answ = None
        get_coins_counter = 0
        get_coins_counter_reset_until = 30
        is_show_statistic_true, next_show_statistic_time = None, None
        self.stratigiee_info()
        next_show_statistic_time = self.get_next_show_statistic_time()

        while True:
            time.sleep(0.01)

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
            elif (self.is_trailing_stop_start == True) or (self.classikal_martin_gale and self.last_win_los == -1):
                wait_time = 0
                if self.in_position:
                    wait_time = 1
            else:
                wait_time = self.time_calibrator(1, 'm') if not self.in_position else 2
            time.sleep(wait_time)
            get_coins_counter += 1
            if get_coins_counter == get_coins_counter_reset_until:
                if not self.classikal_martin_gale or self.last_win_los != -1:
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

