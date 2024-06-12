from datetime import datetime as dttm
from utils import UTILS
import os, inspect
current_file = os.path.basename(__file__)

class INFO(UTILS):
    def __init__(self):
        super().__init__()
        # устанавливаем функциии декораторы
        self.post_trade_info_raport = self.log_exceptions_decorator(self.post_trade_info_raport)
        self.response_order_logger = self.log_exceptions_decorator(self.response_order_logger)

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
                now_time = dttm.now(self.local_tz)
                order_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
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