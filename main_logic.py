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

    def engin_1_2(self):
        try:
            if self.is_trailing_stop_start:  
                if not self.trailing_tp_sl_shell(self.executed_qty, self.enter_price, self.stop_loss_ratio, self.price_precession, self.last_signal_val):
                    msg = "Что-то пошло не так... закройте позицию вручную!!"
                    self.handle_messagee(msg)
                    return False
                self.in_position = False
                self.is_trailing_stop_start = False
                self.last_signal_val = None
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
                    msg = "Бот ищет следующий сигнал"
                    self.handle_messagee(msg)
                    return True
            else:                            
                # ////////////// ищем сигнал если закрыта:
                self.cur_klines_data = self.get_klines(self.symbol, self.interval, self.ema_trend_line)                 
                self.current_signal_val = self.get_signals(
                    self.indicators_strategy_list,
                    self.cur_klines_data, self.ema1_period,
                    self.ema2_period,
                    self.ema_trend_line,
                    self.stoch_rsi_over_sell, self.stoch_rsi_over_buy
                )
                if not self.current_signal_val:
                    self.is_no_signal_counter += 1
                    if self.is_no_signal_counter % self.show_absent_or_signal_every == 0:
                        msg = f"Нет сигнала на протяжение {self.is_no_signal_counter} минут"
                        self.handle_messagee(msg)
            # ////////////// отчет суточной статистики:                
            # self.show_statustik()
            # ///////////                
            # //////////////// анализ сигнала:
            if self.current_signal_val:
                self.is_no_signal_counter = 0
                # ///////////////// сообщение о сигнале:
                self.handle_messagee(self.current_signal_val)
                self.last_signal_val = self.current_signal_val
                self.for_set_open_position_temp()
                                        
                if self.qty == "Too_litle_size":
                    msg = "Размер депозита для данной монеты слишком мал. Выберите другие опции и попробуйте еще раз..."
                    self.handle_messagee(msg)
                    # /////// логика остановки бота на случай если зазмер депозита слишком мал:
                    return False
                
                if not self.make_orders_template_shell():
                    # /////// логика остановки бота на случай если не удалось нормально открыть позицию:
                    return False
                # //////////// вычисляем стопы:
                self.enter_price, self.executed_qty = self.for_set_stops_orders_temp(self.response_trading_list, self.qty, self.cur_price)
                self.stop_loss_ratio = self.calculate_stop_loss_ratio(
                    self.direction, self.enter_price, self.cur_klines_data,
                    self.stop_loss_ratio_mode, self.static_stop_loss_ratio_val,
                    self.min_default_ratio
                )

                self.handle_messagee(f"стоп лосс коэффициент: {self.stop_loss_ratio}")
                if self.stop_loss_global_type == 2:
                    self.in_position = self.fixed_sl_strategy(self.enter_price, self.executed_qty, self.stop_loss_ratio)
                    # ////////////
                    if not self.in_position:
                        # /////// логика остановки бота на случай если не удалось нормально установить стопы:
                        msg = "Что-то пошло не так... закройте позицию вручную!!"
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
        self.run_flag = True
        self.stop_bot_flag = False
        first_iter_flag = True
        self.last_date = self.date_of_the_month()
        self.intradaction_templates()
        martin_gale_status = "включен" if self.martin_gale_flag else "отключен"
        self.handle_messagee(f"Мартин Гейл {martin_gale_status}") 
        if self.max_martin_gale_counter_auto_true:
            self.is_martin_gale_true_template()

        while True:

            if self.losses_counter == self.losses_until_value:
                self.stop_bot_flag = True
                self.handle_messagee(f"Количество неудачных сделок достигло лимита {self.losses_until_value}!! Рекомендуем пересмотреть торговую стратегию или изменить настройки бота!")
            
            if self.stop_bot_flag:
                msg = "Bot остановлен!"
                self.handle_messagee(msg)
                self.run_flag = False
                return

            time_arg = 1
            if first_iter_flag:
                first_iter_flag = False
                msg = "Бот ищет сигнал для входа в позицию. Процесс поиска может занять неопределенное время. Хорошего вам дня!"
                self.handle_messagee(msg)
                time_arg = self.kline_time
            wait_time = self.time_calibrator(time_arg, self.time_frame) if not self.in_position else 30    
            time.sleep(wait_time)
            # time.sleep(5)

            if self.stop_loss_global_type in [1,2]:
                if not self.engin_1_2():
                    self.stop_bot_flag = True
                    continue