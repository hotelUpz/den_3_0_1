from RISK_MANAGMENT.statistik_raport import STATISTIC
import aiohttp
# from aiohttp_socks import ProxyConnector
import asyncio
import json
import random
import os
import inspect
current_file = os.path.basename(__file__)

class TAKE_PROFIT_STOP_LOSS_STRATEGIES(STATISTIC):
    def __init__(self):  
        super().__init__() 
        # устанавливаем функциии декораторы
        self.calculate_stop_loss_ratio = self.log_exceptions_decorator(self.calculate_stop_loss_ratio)
        self.trailing_sl_engin = self.log_exceptions_decorator(self.trailing_sl_engin)
        self.trailing_tp_sl_shell = self.log_exceptions_decorator(self.trailing_tp_sl_shell)
        self.standart_sl_tp_set_orders_template = self.log_exceptions_decorator(self.standart_sl_tp_set_orders_template)

    def sl_ratio_documentation(self):         
        """
        Методы для расчета коэффициента стоп-лосса:

            1. STATIC: Применяет фиксированное значение стоп-лосса.

            2. VOLATILITY_PERIOD_20: Расчитывает коэффициент стоп-лосса на основе среднего истинного диапазона (ATR) за период = 20 свечей.

            3. LAST_VOLATILITY: Использует максимальное отклонение закрытия второй с конца свечи от её минимума или максимума.

            4. LAST_CANDLE_LENGTH: Рассчитывает коэффициент стоп-лосса как разницу между максимумом и минимумом второй с конца свечи.

            5. LAST_CANDLE_LENGTH/2: Аналогично LAST_CANDLE_LENGTH, но значение делится пополам.

            6. LAST_MINIMUM: Если позиция длинная (direction = 1), используется разница между закрытием-открытием и минимумом второй с конца свечи; если короткая (direction = -1), используется разница между закрытием-открфтием и максимумом второй с конца свечи.
                
            7. ABSOLUTE_MIN: Для длинной позиции рассчитывается разница между ценой входа и абсолютным минимумом свечей периода 20; для короткой позиции - между ценой входа и абсолютным максимумом свечей. Если минимум/максимум выходит за пределы цены входа, возвращается фиксированное значение стоп-лосса.
        
            8. VPVR_LEVEL: высчитывается с учетом ориентирования на ближайшую сильную зону VPVR индикатора.
        
        """
    def tp_sl_strategies_documenttion(self):
        """
        Типы глобальных стратегий стоп-лосса:
            1 -- 'TRAILLING': Трейлинг-стоп, перемещающийся стоп-лосс, следуя за ценой.
            2 -- 'FIXED': Фиксированные стоп-лосс и тейк-профит.
        """

# ///////////////// шаблон для закрытия позиции:
    def close_position_utilites(self, last_signal):
        #//////////////// закрываем сотавшиеся ордера если таковые имеются:
        _ = self.cancel_secondary_open_orders(self.symbol)     

        # //////////// show statistic: ///////////////////////////////
        last_win_los = 0
        init_order_price, oposit_order_price = 0, 0
        last_depo = 0
        last_win_los, init_order_price, oposit_order_price, last_depo = self.last_statistic_control(self.symbol, self.depo)  
        self.daily_trade_history_list.append((last_win_los, init_order_price, oposit_order_price, last_depo))
        self.last_win_los = last_win_los
        if last_win_los == -1:
            self.losses_counter += 1
            if self.is_reverse_defencive_mehanizm:
                self.is_reverse_signal = self.default_reverse_signal*(-1)
        else:
            self.is_reverse_signal = self.default_reverse_signal
            self.losses_counter = 0

        self.post_trade_info_raport(last_signal, last_win_los)

        if self.martin_gale_flag:
            self.depo, self.cur_martin_gale_counter = self.martin_gale_prosess_handler(last_win_los, self.start_depo, self.depo, self.cur_martin_gale_counter, self.max_martin_gale_counter, self.martin_gale_ratio)

# /////////////// SL RATIO CALCULATIONS:
    def calculate_stop_loss_ratio(self, direction, enter_price, candles_df, stop_loss_ratio_mode, static_stop_loss_ratio_val, min_default_ratio, max_default_ratio):
        if enter_price == 0:
            return        
        # 1. STATIC: Возвращает фиксированное значение стоп-лосса, заданное параметром static_stop_loss_ratio_val
        if stop_loss_ratio_mode == 1:
            return static_stop_loss_ratio_val/ 100
        
        stop_loss_ratio = None
        min_default_ratio = min_default_ratio/ 100
        max_default_ratio = max_default_ratio/ 100
        candles_df = candles_df.tail(self.ema_trend_line)
        # period = int(candles_df.shape[0]/ 2.5) + 1            
        # 2. VOLATILITY_TOTAL_PERIOD: Расчитывает коэффициент стоп-лосса на основе среднего истинного диапазона (ATR) за период, равный половине количества свечей в candles_df, плюс одна свеча
        if stop_loss_ratio_mode == 2:
            # atr_period = int(candles_df.shape[0]) - 1
            _, atr_value  = self.calculate_atr(candles_df, 20)
            stop_loss_ratio = atr_value / enter_price

        # 3. LAST_VOLATILITY: Использует максимальное отклонение закрытия второй с конца свечи от её минимума или максимума
        if stop_loss_ratio_mode == 3:
            last_volatility = max(abs(candles_df['Close'].iloc[-2] - candles_df['Low'].iloc[-2]), abs(candles_df['Close'].iloc[-2] - candles_df['High'].iloc[-2]), abs(candles_df['Open'].iloc[-2] - candles_df['Low'].iloc[-2]), abs(candles_df['Open'].iloc[-2] - candles_df['High'].iloc[-2]))
            # print(f"last_volatility: {last_volatility}")
            stop_loss_ratio = last_volatility / enter_price

        # 4. LAST_CANDLE_LENGTH: Рассчитывает коэффициент стоп-лосса как разницу между максимумом и минимумом второй с конца свечи
        if stop_loss_ratio_mode == 4:
            last_candle = abs(candles_df['High'].iloc[-2] - candles_df['Low'].iloc[-2])
            # print(f"last_candle: {last_candle}")
            stop_loss_ratio = last_candle / enter_price

        # 5. LAST_CANDLE_LENGTH/2: Аналогично LAST_CANDLE_LENGTH, но значение делится пополам.
        if stop_loss_ratio_mode == 5:
            last_candle_1 = abs(candles_df['High'].iloc[-2] - candles_df['Low'].iloc[-2])/ 2
            # print(f"last_candle/2: {last_candle}")
            stop_loss_ratio = last_candle_1 / enter_price
        
        # 6. LAST_MINIMUM: Если позиция длинная (direction = 1), используется разница между закрытием и минимумом второй с конца свечи; если короткая (direction = -1), используется разница между закрытием и максимумом второй с конца свечи        
        if stop_loss_ratio_mode == 6:
            if direction == 1:
                last_min = max(abs(candles_df['Close'].iloc[-2] - candles_df['Low'].iloc[-2]), abs(candles_df['Open'].iloc[-2] - candles_df['Low'].iloc[-2]))
                # print(f"last_min: {last_min}")                
            elif direction == -1:              
                last_min = max(abs(candles_df['Close'].iloc[-2] - candles_df['High'].iloc[-2]), abs(candles_df['Open'].iloc[-2] - candles_df['High'].iloc[-2]))
                # print(f"last_max: {last_max}")           
            stop_loss_ratio = last_min / enter_price

        # 7. ABSOLUTE_MIN: Для длинной позиции рассчитывается разница между ценой входа и абсолютным минимумом свечей периода 20; для короткой позиции - между ценой входа и абсолютным максимумом. Если минимум/максимум выходит за пределы цены входа, возвращается фиксированное значение стоп-лосса
        if stop_loss_ratio_mode == 7:   
            last_20_candles = candles_df.iloc[-20:]         
            if direction == 1:                
                absolute_min = last_20_candles['Low'].min()
                if absolute_min >= enter_price:
                    return min_default_ratio
                else:
                    stop_loss_ratio = (enter_price - absolute_min) / enter_price
            elif direction == -1:
                absolute_max = last_20_candles['High'].max()
                if absolute_max <= enter_price:
                    return min_default_ratio
                else:
                    stop_loss_ratio = abs(enter_price - absolute_max) / enter_price

        if stop_loss_ratio_mode == 8:
            if self.indicators_strategy_number == 10:
                if self.vpvr_level_line is not None:
                    stop_loss_ratio = abs(enter_price - self.vpvr_level_line) / enter_price
                else:
                    stop_loss_ratio = 0
            else:
                immediate_vpvr_level_defender_val = None
                vpvr = self.calculate_vpvr(candles_df)                       
                vpvr_levels = self.find_vpvr_levels(vpvr)
                immediate_vpvr_level_defender_val = self.immediate_vpvr_level_defender(enter_price, vpvr_levels)                
                if immediate_vpvr_level_defender_val:
                    stop_loss_ratio = abs(enter_price - immediate_vpvr_level_defender_val[1]) / enter_price
                else:
                    stop_loss_ratio = 0

        if stop_loss_ratio is not None:
            if stop_loss_ratio <= min_default_ratio:
                print(f"stop_loss_ratio: {stop_loss_ratio}")
                self.handle_messagee(f"stop_loss_ratio < {min_default_ratio}: {stop_loss_ratio <= min_default_ratio}") 
                return min_default_ratio
            elif stop_loss_ratio >= max_default_ratio:
                self.handle_messagee(f"stop_loss_ratio > {max_default_ratio}: {stop_loss_ratio >= max_default_ratio}") 
                return max_default_ratio
        
        return stop_loss_ratio
    
# //////////////// trailing sl:
    def trailing_sl_engin(self, cur_price, qty, enter_price, stop_loss_ratio, stop_loss_step_counter, trigger_step_counter, next_trigger_price, sl_order_id, is_problem_to_moved_sl, price_precession, sl_risk_reward_multiplier, last_signal_val, last_stop_loss_price): 
        if cur_price:
            jump_next_trigger_price_condition = False
            tp_condition = False
            sl_condition = False

            if last_signal_val == 1:
                jump_next_trigger_price_condition = cur_price >= next_trigger_price 
                tp_condition = cur_price >= self.target_tp_price
                sl_condition = cur_price <= last_stop_loss_price
            else:
                jump_next_trigger_price_condition = cur_price <= next_trigger_price 
                tp_condition = cur_price <= self.target_tp_price
                sl_condition = cur_price >= last_stop_loss_price
            
            if tp_condition or sl_condition:
                return stop_loss_step_counter, trigger_step_counter, sl_order_id, next_trigger_price, is_problem_to_moved_sl, True, last_stop_loss_price

            if jump_next_trigger_price_condition:
                # print("jump_next_trigger_price_condition")
                stop_loss_step_counter += 1
                trigger_step_counter += 1
            
                last_stop_loss_price = stop_loss_price = enter_price * (1 + last_signal_val * stop_loss_ratio * sl_risk_reward_multiplier * stop_loss_step_counter)
                next_trigger_price = enter_price * (1 + last_signal_val * stop_loss_ratio * sl_risk_reward_multiplier * trigger_step_counter)
                
                pies_of_frase = "Двигаем стоп лосс на:"
                self.handle_messagee(f"{pies_of_frase} {stop_loss_price}. Счетчик перемещений = {trigger_step_counter-1}")
                side= 'BUY' if last_signal_val == -1 else 'SELL'
                if sl_order_id:
                    # ////////// отменяем предыдущий стоп лосс:
                    cancel_order_answer = self.cancel_order_by_id(self.symbol, sl_order_id)
                    if cancel_order_answer is not None and cancel_order_answer.get('status', None) == 'CANCELED':
                        # ///////// устанавливаем следующий стоп лосс ордер:
                        sl_order_answer = self.make_order(
                            self.symbol,
                            qty,
                            side,
                            'STOP_MARKET',
                            round(stop_loss_price, price_precession)
                        )       

                        # response_order_logger_answer = self.response_order_logger(
                        #     sl_order_answer, 
                        #     side, 
                        #     'STOP_MARKET'
                        #     )

                        sl_order_id = sl_order_answer.get('orderId', None)
                        # is_problem_to_moved_sl = (not response_order_logger_answer) or (sl_order_id is None)    
                        is_problem_to_moved_sl = (sl_order_id is None)                        

        return stop_loss_step_counter, trigger_step_counter, sl_order_id, next_trigger_price, is_problem_to_moved_sl, False, last_stop_loss_price
    
    def trailing_tp_sl_shell(self, qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id):
        async def stop_logic_price_monitoring(qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id):
            # print(qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id)
            # /////////////////////////////////////  
            url = 'wss://stream.binance.com:9443/ws/'
            # /////////////////////////////////////
            max_retries = 10
            max_async_cycle_retries = 5
            retry_delay = 1  # seconds
            retries = 0            
            # /////////////////////////////////////
            seconds_counter = 0
            seconds_counter_for_closing = 0
            # /////////////////////////
            is_problem_to_moved_sl = False
            is_check_position = False     
            stop_loss_step_counter = -1
            trigger_step_counter = 1   
            last_stop_loss_price = self.last_stop_loss_price        
            next_trigger_price = enter_price * (1 + (last_signal_val * stop_loss_ratio * trigger_step_counter))
            # print(f"next_trigger_price_220str: {next_trigger_price}")
            # /////////////////////////////////////
            while retries < max_retries:
                if self.stop_bot_flag:
                    return False         
                try:
                    # connectorr = None
                    # if self.is_proxies_true:
                    #     connectorr = ProxyConnector.from_url(f'socks5://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_socks5_port}')
                    
                    # async with aiohttp.ClientSession(connector=connectorr) as session:
                    #     async with session.ws_connect(url + f"{self.symbol}@kline_1s") as ws:
                    timeout = aiohttp.ClientTimeout(total=20)
                    async with aiohttp.ClientSession(timeout=timeout) as session:
                        async with session.ws_connect(url + f"{self.symbol}@kline_1s", proxy=self.proxy_url if self.is_proxies_true else None) as ws:
                            subscribe_request = {
                                "method": "SUBSCRIBE",
                                "params": [f"{self.symbol.lower()}@kline_1s"],
                                "id": random.randrange(11,111111)
                            }
                            print('Stop_logic_price_monitoring start processing!')
                            async_cycle_retries = 0                     
                            try:
                                await ws.send_json(subscribe_request)
                            except:
                                pass

                            async for msg in ws:
                                if self.stop_bot_flag:
                                    return False
                                if async_cycle_retries >= max_async_cycle_retries:
                                    try:
                                        await ws.close()
                                    except:
                                        pass                                
                                    break
                                try:
                                    if msg.type == aiohttp.WSMsgType.TEXT:                                    
                                        data = json.loads(msg.data)
                                        kline_websocket_data = data.get('k', {})
                                        if kline_websocket_data:
                                            cur_price = float(kline_websocket_data.get('c'))
                                            # print(f"last_close_price websocket: {cur_price}")                         

                                            if (seconds_counter == 2) or (is_check_position):
                                                # print("try to check is_close_pos_true")
                                                if self.closing_by_ema_crossover_flag:
                                                    if seconds_counter_for_closing == 60:  
                                                        self.closing_by_ema_crossover_signal_shell()                          
                                                        seconds_counter_for_closing = 0                                            

                                                if self.is_closing_position_true(self.symbol):
                                                    self.sl_order_id = sl_order_id
                                                    self.close_position_utilites(
                                                        last_signal_val
                                                    )                                                            
                                                    msg = "Бот ищет следующий сигнал"
                                                    self.handle_messagee(msg)
                                                    return True
                                                if is_problem_to_moved_sl:
                                                    return False                                                    
                                                seconds_counter = 0
                                
                                            stop_loss_step_counter, trigger_step_counter, sl_order_id, next_trigger_price, is_problem_to_moved_sl, is_check_position, last_stop_loss_price = self.trailing_sl_engin(cur_price, qty, enter_price, stop_loss_ratio, stop_loss_step_counter, trigger_step_counter, next_trigger_price, sl_order_id, is_problem_to_moved_sl, price_precession, sl_risk_reward_multiplier, last_signal_val, last_stop_loss_price)
                                                
                                            seconds_counter += 1
                                            seconds_counter_for_closing += 1
                                            continue
                                          
                                except Exception as ex:
                                    pass
                                async_cycle_retries += 1
                                        
                except Exception as ex:
                    self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")  
                retries += 1
                try:
                    await ws.close()
                except:
                    pass   
                await asyncio.sleep(retry_delay + ((2 * retries)/10))

            return False
        
        if not asyncio.run(stop_logic_price_monitoring(qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id)):
            return False 
        return True
    
# /////////////// TP_SL fixed type:
    def standart_sl_tp_set_orders_template(self, enter_price, executed_qty, stop_loss_ratio, current_signal_val):

        target_prices_list = []   
        market_type_list = []
        in_position = False
        if self.secondary_orders_type == 1:
            market_type_list = ['STOP_MARKET', 'TAKE_PROFIT_MARKET']            
        elif self.secondary_orders_type == 2:            
            market_type_list = ['STOP_MARKET', 'LIMIT']
        else:
            self.handle_messagee("Параметр 'self.secondary_orders_type' невалидный. Перезапустите бота и установите правильные настройки!")
            return
        
        # if self.only_stop_loss_flag:
        sl_risk_reward_multiplier = float(self.risk_reward_ratio.split(':')[0].strip())     
        self.last_stop_loss_price = target_sl_price = round((enter_price * (1 - current_signal_val * stop_loss_ratio * sl_risk_reward_multiplier)), self.price_precession)
        
        price_precession = self.price_precession_limit if self.secondary_orders_type == 2 else self.price_precession 
        # if self.only_take_profit_flag:       
        tp_risk_reward_multiplier = float(self.risk_reward_ratio.split(':')[1].strip())
        self.target_tp_price = target_tp_price = round((enter_price * (1 + current_signal_val * stop_loss_ratio * tp_risk_reward_multiplier)), price_precession)

        target_prices_list = [target_sl_price, target_tp_price]
        if self.only_stop_loss_flag:
            market_type_list.pop(1)
            target_prices_list.pop(1)
        if self.only_take_profit_flag:
            market_type_list.pop(0)
            target_prices_list.pop(0)

        in_position, sl_order_id, tp_order_id = self.make_sl_tp_template(executed_qty, market_type_list, target_prices_list)

        return in_position, sl_risk_reward_multiplier, tp_risk_reward_multiplier, sl_order_id, tp_order_id    
    
    def closing_by_ema_crossover_signal_shell(self):
        def closing_by_ema_crossover_signal():
            try:
                df = self.get_klines(self.symbol, self.interval, self.ema_trend_line)
                if not self.swirch_to_WMA_flag:
                    df = self.calculate_ema(df)
                else:
                    df = self.calculate_wma(df)
                ema_crossover_defender_val = self.ema_crossover_defender(df)
                if self.last_signal_val == 1:                 
                    if ema_crossover_defender_val == "S":
                        print(f"ema_crossover close pos signal!")
                        self.current_signal_val = self.last_signal_val*(-1)
                        if not self.make_orders_template_shell():
                            return 0
                        return 1
                    return 2
                
                elif self.last_signal_val == -1:                 
                    if ema_crossover_defender_val == "L":
                        print(f"ema_crossover close pos signal!")
                        self.current_signal_val = self.last_signal_val*(-1)
                        if not self.make_orders_template_shell():
                            return 0
                        return 1
                    return 2
                
                return 3
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")  
            return
        
        closing_by_ema_crossover_signal_repl = closing_by_ema_crossover_signal()
        if closing_by_ema_crossover_signal_repl == 1:
            self.handle_messagee("Позиция закрыта по сигналу кроссовер")
        elif closing_by_ema_crossover_signal_repl == 0:
            self.handle_messagee("Не удалось закрыть позицию по сигналу кроссовер")
        elif closing_by_ema_crossover_signal_repl == 3:
            self.handle_messagee("Информаци о направленности последней сделки недоступна")
        elif closing_by_ema_crossover_signal_repl is None:
            self.handle_messagee("В процессе попытки закрыть позицию по сигналу возникли какие-то ошибки")
        