from infoo import INFO
import time
import os
import inspect
current_file = os.path.basename(__file__)

class TEMPLATES(INFO):
    def __init__(self):  
        super().__init__()
        # устанавливаем функциии декораторы
        self.for_set_open_position_temp = self.log_exceptions_decorator(self.for_set_open_position_temp)
        self.for_set_stops_orders_temp = self.log_exceptions_decorator(self.for_set_stops_orders_temp)
        self.set_leverage_template = self.log_exceptions_decorator(self.set_leverage_template)
        self.get_top_coins_template = self.log_exceptions_decorator(self.get_top_coins_template)
        self.intradaction_templates = self.log_exceptions_decorator(self.intradaction_templates)
        self.make_orders_template_shell = self.log_exceptions_decorator(self.make_orders_template_shell)
        self.make_sl_tp_template = self.log_exceptions_decorator(self.make_sl_tp_template)

    # ////////////////////////////////////// 
    def set_leverage_template(self):
        self.handle_messagee("Устанавливаем кредитное плечо:")           
        set_leverage_resp = self.set_leverage(self.symbol, self.lev_size)
        self.handle_messagee(str(set_leverage_resp))
        return True 
    
    def get_top_coins_template(self):
        all_binance_tickers = self.get_all_tickers()
        coinsMarket_tickers = []
        if self.in_coinMarketCup_is:
            coinsMarket_tickers = self.coin_market_cup_top(self.TOP_MARKET_CUP) 
        return self.go_filter(all_binance_tickers, coinsMarket_tickers)

    def intradaction_templates(self):
        try:            
            self.handle_messagee('Устанавливаем тип маржи')                          
            set_margin_resp = self.set_margin_type(self.symbol, self.margin_type)
            self.handle_messagee(str(set_margin_resp)) 
            # Устанавливаем кредитное плечо
            if not self.was_change_leverage_true:
                self.set_leverage_template()            
            # Выводим торговые данные
            trade_data_mess = f"Основные торговые данные:\nМонета: {self.symbol}\nРазмер ставки: {self.depo}\nКредитное плечо: {self.lev_size}"
            self.handle_messagee(trade_data_mess)
            trade_params_mess = f"Текущие параметры стратегии:\nСтратегия индикатора: {self.indicators_strategy_text_patterns[f"{self.indicators_strategy_number}"]}\nСтратегия TP/SL: {self.stop_loss_global_type_text_patterns[f"{self.stop_loss_global_type}"]}\nСпособ расчета стоп лосс коэффициента: {self.stop_loss_ratio_mode_text_patterns[f"{self.stop_loss_ratio_mode}"]}\nСоотношение риска к прибыли (только для фиксированного типа стоп лосса): {self.risk_reward_ratio}"
            self.handle_messagee(trade_params_mess)

        except Exception as ex:
            self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}") 

    def make_orders_template_shell(self):
        def make_orders_template(qty, market_type, target_price):
            order_answer = {}
            response_list = []        
            side = 'BUY' if self.direction * self.is_reverse_signal == 1 else 'SELL'
            try:
                order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
                response_list.append(order_answer)
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")  
            return response_list, self.response_order_logger(order_answer, side, market_type) 
        
        self.last_direction = self.direction = 1 * self.is_reverse_signal if self.current_signal_val == "LONG_SIGNAL" else -1 * self.is_reverse_signal
        self.response_trading_list, self.create_order_success_flag = make_orders_template(self.qty, 'MARKET', None)

        if not self.create_order_success_flag:
            msg = "Что-то пошло не так. Выключаемся!.."
            self.handle_messagee(msg)
            return False       
        
        return True

    def make_sl_tp_template(self, qty, market_type_list, target_price_list):
        order_answer = None
        response_success_list = []
        side = 'BUY' if self.direction * self.is_reverse_signal == -1 else 'SELL'
        for market_type, target_price in zip(market_type_list, target_price_list):
            try:
                order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
                response_success_list.append(self.response_order_logger(order_answer, side, market_type))
                time.sleep(0.1)
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
        return all(response_success_list)

    def for_set_open_position_temp(self):
        symbol_info = self.get_excangeInfo() 
        # print(symbol_info)
        self.cur_klines_data = self.get_klines(self.symbol, self.interval, 2) 
        self.cur_price = self.cur_klines_data['Close'].iloc[-1]
        # print(f"cur_price: {cur_price}")
        self.qty, self.price_precession = self.usdt_to_qnt_converter(self.symbol, self.depo, symbol_info, self.cur_price)
        self.handle_messagee(f"qty, cur_price:\n{self.qty}, {self.cur_price}")           
        # self.from_anomal_view_to_normal([self.qty, self.cur_price])    
    
    def for_set_stops_orders_temp(self, response_trading_list, qty, cur_price):
        executed_qty = float(response_trading_list[0].get('executedQty', qty))
        self.last_enter_price = enter_price = float(response_trading_list[0].get('avgPrice', cur_price))
        self.handle_messagee(f"qty, enter_price:\n{executed_qty}, {enter_price}")
        # self.from_anomal_view_to_normal([executed_qty, enter_price])  
        return enter_price, executed_qty