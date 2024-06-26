from RISK_MANAGMENT.martin_galee import MARTIN_GALE
import os
import inspect
current_file = os.path.basename(__file__)

class STATISTIC(MARTIN_GALE):
    def __init__(self):  
        super().__init__()
        # устанавливаем функциии декораторы
        self.last_statistic_control = self.log_exceptions_decorator(self.last_statistic_control) 
        self.statistic_calculations = self.log_exceptions_decorator(self.statistic_calculations)
        self.show_statustik = self.log_exceptions_decorator(self.show_statustik)

    def last_statistic_control(self, symbol, depo):        
        init_order_price, oposit_order_price = 0, 0
        try:
            orders = self.get_all_orders(symbol)
            orders= sorted(orders, key=lambda x: x["time"], reverse=True)
            the_orders = []
            for order in orders:
                if len(the_orders) == 2:
                    break
                try:
                    if order["status"] == 'FILLED':                        
                        the_orders = [order] + the_orders                        
                except:
                    pass
            init_order_price = float(the_orders[0].get('avgPrice', None))
            oposit_order_price = float(the_orders[1].get('avgPrice', None))
            if the_orders[0].get('side', None) == the_orders[1].get('side', None):
                return 0, 0, 0, depo
            if the_orders[0].get('side', None) == 'BUY':
                if init_order_price - oposit_order_price > 0:
                    return -1, init_order_price, oposit_order_price, depo
                elif init_order_price - oposit_order_price < 0:
                    return 1, init_order_price, oposit_order_price, depo
            elif the_orders[0].get('side', None) == 'SELL':
                if init_order_price - oposit_order_price > 0:
                    return 1, init_order_price, oposit_order_price, depo
                elif init_order_price - oposit_order_price < 0:
                    return -1, init_order_price, oposit_order_price, depo
        except Exception as ex:
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
        return 0, init_order_price, oposit_order_price, depo
  
    def statistic_calculations(self, daily_trade_history_list, symbol):
        result_statistic_dict = {}
        result_statistic_dict["symbol"] = symbol
        win_to_loss_statistik = "0:0"
        max_profit_abs = 0
        max_loss_abs = 0
        best_performance = 0
        max_drawdown = 0
        total_profit_abs = 0
        total_losses_abs = 0

        if not isinstance(daily_trade_history_list, list) or len(daily_trade_history_list) == 0:
            return "Нет данных для анализа"

        try:
            win_count = sum(1 for win_los, _, _, _ in daily_trade_history_list if win_los == 1)
            loss_count = sum(1 for win_los, _, _, _ in daily_trade_history_list if win_los == -1)
            win_to_loss_statistik = f"{win_count}:{loss_count}"
        except Exception as ex:
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
        result_statistic_dict["Отношение Плюсовых сделок к Минусовым"] = win_to_loss_statistik

        try:
            total_result_list = []
            for win_los, init_order_price, oposit_order_price, last_depo in daily_trade_history_list:
                if win_los == 1:
                    total_result_list.append((abs(init_order_price - oposit_order_price) / init_order_price) * last_depo)
                elif win_los == -1:
                    total_result_list.append(-1 * (abs(init_order_price - oposit_order_price) / init_order_price) * last_depo)

            if total_result_list:
                max_profit_abs = max(x for x in total_result_list if x > 0)
                max_loss_abs = min(x for x in total_result_list if x < 0)
                total_profit_abs = sum(x for x in total_result_list if x > 0)
                total_losses_abs = sum(x for x in total_result_list if x < 0)

                current_positive_sum = 0
                current_negative_sum = 0

                for t in total_result_list:
                    if t > 0:
                        current_positive_sum += t
                        if current_negative_sum < 0:
                            max_drawdown = min(max_drawdown, current_negative_sum)
                            current_negative_sum = 0
                    elif t < 0:
                        current_negative_sum += t
                        if current_positive_sum > 0:
                            best_performance = max(best_performance, current_positive_sum)
                            current_positive_sum = 0

                best_performance = max(best_performance, current_positive_sum)
                max_drawdown = min(max_drawdown, current_negative_sum)
        except Exception as ex:
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

        result_statistic_dict["Суммарный доход ($)"] = total_profit_abs
        result_statistic_dict["Суммарный убыток ($)"] = total_losses_abs
        result_statistic_dict["Прибыль (без учета комиссии) ($)"] = total_profit_abs - abs(total_losses_abs)

        if result_statistic_dict["Прибыль (без учета комиссии) ($)"] > 0:
            result_statistic_dict["Результат торговли за день"] = "Сегодня стратегия сработала в плюс"
        elif result_statistic_dict["Прибыль (без учета комиссии) ($)"] < 0:
            result_statistic_dict["Результат торговли за день"] = "Сегодня стратегия сработала в минус"
        else:
            result_statistic_dict["Результат торговли за день"] = "Сегодня стратегия сработала в ноль"

        result_statistic_dict["Максимально прибыльная сделка ($)"] = max_profit_abs
        result_statistic_dict["Максимально убыточная сделка ($)"] = max_loss_abs
        result_statistic_dict["Перфоманс (максимальная сумма серии удачных сделок) ($)"] = best_performance
        result_statistic_dict["Максимальная просадка ($)"] = max_drawdown

        result_string = "\n".join(f"{key}: {value}" for key, value in result_statistic_dict.items())
        return result_string

    def show_statustik(self):
        self.cur_date = self.date_of_the_month()
        if self.last_date < self.cur_date:
            self.is_time_to_show_done = False
            self.last_date = self.cur_date

        if self.is_time_to_show_statistik(self.show_statistic_hour) and not self.is_time_to_show_done:
            result_statistic_dict = ""
            result_statistic_dict = self.statistic_calculations(self.daily_trade_history_list, self.symbol)                   
            self.handle_messagee(f"Показатели торгов за сутки:\n{result_statistic_dict}")                             
            self.daily_trade_history_list = []
            self.is_time_to_show_done = True 