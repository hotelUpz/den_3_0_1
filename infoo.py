import time
from utils import UTILS, time_correction_val
import os, inspect
current_file = os.path.basename(__file__)

class INFO(UTILS):
    def __init__(self):
        super().__init__()
        # устанавливаем функциии декораторы
        self.stop_logic_documentation = self.log_exceptions_decorator(self.stop_logic_documentation)
        self.post_trade_info_raport = self.log_exceptions_decorator(self.post_trade_info_raport)
        self.response_order_logger = self.log_exceptions_decorator(self.response_order_logger)

    def stop_logic_documentation(self):         
        """
        Типы глобальных стратегий стоп-лосса:
            (Регулируется параметром self.stop_loss_global_type. В интерфейсе телеграм бота -- соответсвующий номер стратегии. По умолчанию равен 2 (фиксированные стоп лосс/тейк профит))

            1 -- 'TRAILLING': Трейлинг-стоп, перемещающийся стоп-лосс, следуя за ценой.
            2 -- 'FIXED': Фиксированные стоп-лосс и тейк-профит.
            3 -- 'SIGNAL_USUAL': Закрытие позиции по сигналам. Классический вариант, где стоп-лосс и тейк-профит отсутствуют.
            4 -- 'SIGNAL_ADVANCED': Закрытие позиции по сигналам или по стоп-лосс/тейк-профиту.
        .................

        Методы для расчета коэффициента стоп-лосса:
            (Регулируется параметром self.stop_loss_ratio_mode. В интерфейсе телеграм бота -- соответсвующий номер метода. По умолчанию равен 1 (статический коэффициент, равный установленному значению. Сейчас стоит 1 % (в процентах))

            - fixed_stop_loss_ratio_val %: Фиксированное значение стоп-лосса для типа 'STATIC'.
            - min_default_ratio %: Минимальное значение коэффициента стоп-лосса по умолчанию.

            1. STATIC: Возвращает фиксированное значение стоп-лосса, заданное параметром fixed_stop_loss_ratio_val.

            2. VOLATILITY_TOTAL_PERIOD: Расчитывает коэффициент стоп-лосса на основе среднего истинного диапазона (ATR) за период, равный половине количества свечей в candles_df, плюс одна свеча.

            3. LAST_VOLATILITY: Использует максимальное отклонение закрытия второй с конца свечи от её минимума или максимума.

            4. LAST_CANDLE_LENGTH: Рассчитывает коэффициент стоп-лосса как разницу между максимумом и минимумом второй с конца свечи.

            5. LAST_CANDLE_LENGTH/2: Аналогично LAST_CANDLE_LENGTH, но значение делится пополам.

            6. LAST_MINIMUM: Если позиция длинная (direction = 1), используется разница между закрытием и минимумом второй с конца свечи; если короткая (direction = -1), используется разница между закрытием и максимумом второй с конца свечи.
                
            7. ABSOLUTE_MIN: Для длинной позиции рассчитывается разница между ценой входа и абсолютным минимумом всех свечей всего периода; для короткой позиции - между ценой входа и абсолютным максимумом всех свечей. Если минимум/максимум выходит за пределы цены входа, возвращается фиксированное значение стоп-лосса.

            В случае, если рассчитанный коэффициент стоп-лосса меньше минимального значения (min_default_ratio), возвращается значение 0.002.
        .............................

        - risk_reward_ratio = '1:1.5' -- соотношение риска к прибыли. только для 'FIXED или для'SIGNAL_ADVANCED типов стратегий'

        """

    def post_trade_info_raport(self, last_signal, last_win_los):
        
        post_trade_piece_message = ""
        result_message = ""
        if last_signal == 'LONG_SIGNAL':
            post_trade_piece_message = 'Лонговая'
        elif last_signal == 'SHORT_SIGNAL':
            post_trade_piece_message = 'Шортовая'
        
        closure_message = f"{post_trade_piece_message} позиция была закрыта"
        self.handle_messagee(closure_message)
        
        result_message = ""
        if last_win_los == 1:
            result_message = f"Последняя {post_trade_piece_message} сделка была закрыта в плюс"
        elif last_win_los == -1:
            result_message = f"Последняя {post_trade_piece_message} сделка была закрыта в минус"
        else:
            result_message = f"Последняя {post_trade_piece_message} сделка была закрыта в ноль"       

        self.handle_messagee(result_message)
        return True

    def response_order_logger(self, order_answer, side, market_type): 
        if order_answer is not None:
            specific_key_list = ["orderId", "symbol", "type", "side", "avgPrice", "executedQty", "activatePrice", "priceRate", "stopPrice"]
            order_answer_str = ""
            try:
                # order_time = self.milliseconds_to_datetime(order_answer.get('updateTime') + time_correction_val)
                ms_order_time = int(time.time()* 1000) + time_correction_val
                order_time = self.milliseconds_to_datetime(ms_order_time)
                for k, v in order_answer.items():
                    if k in specific_key_list:
                        order_answer_str += f"{k}: {v}\n"
                order_answer_str = 'Время создания ордера:' + ' ' + order_time + '\n' + order_answer_str 
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
                
            status = order_answer.get('status')
            mess_text = ""
            if status in ['FILLED', 'NEW', 'PARTIALLY_FILLED']:
                if status == 'FILLED' or status == 'NEW':
                    mess_text = f'{side} позиция {market_type} типа была открыта успешно!'
                elif status == 'PARTIALLY_FILLED':
                    mess_text = f'{side} позиция {market_type} типа была открыта со статусом PARTIALLY_FILLED'

                self.handle_messagee(mess_text)
                if order_answer_str:
                    self.handle_messagee(order_answer_str)
                else:
                    self.handle_messagee("Не удалось получить торговые данные")
                return True

        error_message = f"При попытке создания ордера возникла ошибка. Текст ответа:\n {order_answer}"
        error_message_2 = f'{side} позиция {market_type} типа не была открыта...'
        self.handle_messagee(error_message)
        self.handle_messagee(error_message_2)                
        return False