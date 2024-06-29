# # # # import pandas as pd
# # # # import matplotlib.pyplot as plt
# # # # from api_binance import BINANCE_API


# # # # def calculate_vpvr(data, min_bins=10, max_bins=50):
# # # #     # Вычисляем динамическое количество корзин (bins) на основе количества свечей
# # # #     num_candles = 240
# # # #     bins = min(max(min_bins, num_candles // 10), max_bins)
# # # #     data = data.tail(240)
# # # #     # print(data)        
# # # #     # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
# # # #     price_range = pd.cut(data['Close'], bins=bins)
# # # #     vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
# # # #     return vpvr

# # # # def find_vpvr_levels(vpvr, num_levels=2):
# # # #     # Поиск наиболее объемных зон VPVR
# # # #     top_vpvr_indexes = vpvr.nlargest(num_levels).index
# # # #     vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
# # # #     return vpvr_levels

# # # # def immediate_vpvr_level_defender(cur_price, vpvr_levels):
# # # #     disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
# # # #                 (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
# # # #     if not disposition:
# # # #         immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
# # # #         strongest_volum_level = [0, 0]

# # # #         for _, _, m, v in vpvr_levels:
# # # #             cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
# # # #             if cur_volum_level > strongest_volum_level[0]:
# # # #                 strongest_volum_level = [cur_volum_level, m]                                

# # # #         if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
# # # #             return "L", immediate_level
# # # #         elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
# # # #             return "S", immediate_level
# # # #         elif strongest_volum_level[1] > cur_price:
# # # #             return "L", strongest_volum_level[1]
# # # #         elif strongest_volum_level[1] < cur_price:
# # # #             return "L", strongest_volum_level[1]

# # # #     return

# # # # def plot_vpvr(vpvr):
# # # #     plt.barh(vpvr.index.astype(str), vpvr.values, height=0.5)
# # # #     plt.ylabel('Price Range')
# # # #     plt.xlabel('Volume')
# # # #     plt.title('Volume Profile Visible Range (VPVR)')
# # # #     plt.show()

# # # # df = BINANCE_API().get_klines('BTCUSDT', '5m', 20)
# # # # vpvr = calculate_vpvr(df)
# # # # cur_price = df["Close"].iloc[-1]
# # # # print(f"cur_price: {cur_price}")

# # # # immediate_vpvr_level_defender_val = None
# # # # vpvr = calculate_vpvr(df)                       
# # # # vpvr_levels = find_vpvr_levels(vpvr)
# # # # immediate_vpvr_level_defender_val = immediate_vpvr_level_defender(cur_price, vpvr_levels)

# # # # if immediate_vpvr_level_defender_val:
# # # #     if immediate_vpvr_level_defender_val[0] == 'L':
# # # #         print("vpr indicator: Long")
# # # #     elif immediate_vpvr_level_defender_val[0] == 'S':
# # # #         print("vpr indicator: Short")
# # # #     print(f"level: {immediate_vpvr_level_defender_val[1]}")

# # # # plot_vpvr(vpvr)

    
# # # #     # def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
# # # #     #     symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
# # # #     #     # print(symbol_data)
# # # #     #     # //////////////////////
# # # #     #     quantity_precision = int(float(symbol_data['quantityPrecision']))
# # # #     #     price_precision = int(float(symbol_data['pricePrecision']))
# # # #     #     # print(f"quantity_precision: {quantity_precision}")
# # # #     #     min_notional = int(float(next((f['notional'] for f in symbol_data['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 0)))
# # # #     #     if depo <= min_notional:
# # # #     #         depo = min_notional
# # # #     #     if (quantity_precision == 0 and (depo / cur_price) < 1) or depo < 5:
# # # #     #         return "Too_litle_size", None            
# # # #     #     return round(depo / cur_price, quantity_precision), price_precision 


# # # # def count_decimal_places(number):
# # # #     if isinstance(number, (int, float)):
# # # #         # Преобразуем число в строку
# # # #         number_str = f'{number:.10f}'.rstrip('0')
# # # #         # Проверяем наличие десятичной точки
# # # #         if '.' in number_str:
# # # #             # Возвращаем количество знаков после запятой
# # # #             return len(number_str.split('.')[1])
# # # #     return 0

# # # # import math
# # # # str_number = '1.00105'
# # # # float_number = float(str_number)
# # # # price_precision_limit = count_decimal_places(float_number)
# # # # print(price_precision_limit)

# # # import aiohttp
# # # import asyncio
# # # import random
# # # import json
# # # from aiohttp_socks import ProxyConnector
# # # from api_binance import BINANCE_API

# # # class WEbss(BINANCE_API):
# # #     def __init__(self):  
# # #         super().__init__()

# # #     def trailing_tp_sl_shell(self):
# # #         async def stop_logic_price_monitoring():
# # #             # print(qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id)
# # #             symbol = 'BTCUSDT'
# # #             # /////////////////////////////////////  
# # #             url = 'wss://stream.binance.com:9443/ws/'
# # #             # /////////////////////////////////////
# # #             max_retries = 10
# # #             retry_delay = 1  # seconds
# # #             retries = 0
# # #             # /////////////////////////////////////

# # #             while retries < max_retries:            
# # #                 try:
# # #                     if self.is_proxies_true:
# # #                         connector = ProxyConnector.from_url(f'socks5://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_socks5_port}')
# # #                     async with aiohttp.ClientSession(connector=connector if self.is_proxies_true else None) as session:

# # #                         async with session.ws_connect(url + f"{symbol}@kline_1s") as ws:
# # #                             subscribe_request = {
# # #                                 "method": "SUBSCRIBE",
# # #                                 "params": [f"{symbol.lower()}@kline_1s"],
# # #                                 "id": random.randrange(11,111111)
# # #                             }
# # #                             # print('Stop_logic_price_monitoring start processing!')                       
# # #                             try:
# # #                                 await ws.send_json(subscribe_request)
# # #                             except:
# # #                                 pass

# # #                             async for msg in ws:
# # #                                 if msg.type == aiohttp.WSMsgType.TEXT:
# # #                                     try:
# # #                                         data = json.loads(msg.data)
# # #                                         kline_websocket_data = data.get('k', {})
# # #                                         if kline_websocket_data:
# # #                                             try:
# # #                                                 cur_price = float(kline_websocket_data.get('c'))
# # #                                                 print(f"last_close_price: {cur_price}")                              
                                
# # #                                             except Exception as ex:
# # #                                                 # print(ex)
# # #                                                 pass
                                            
# # #                                     except Exception as ex:
# # #                                         continue

# # #                 except Exception as ex:
# # #                     print(f"An error occurred: {ex}")
# # #                     retries += 1
# # #                     await asyncio.sleep(retry_delay * (2 ** retries))  # Exponential backoff
# # #             return
        
# # #         asyncio.run(stop_logic_price_monitoring())

# # # WEbss().trailing_tp_sl_shell()



# #     # def cancel_order_by_id(self, symbol, orderId, retries=3):
# #     #     attempt = 0
# #     #     while attempt < retries:
# #     #         try:
# #     #             params = {
# #     #                 'symbol': symbol,
# #     #                 'orderId': orderId,
# #     #                 'timestamp': int(time.time() * 1000)
# #     #             }
# #     #             params = self.get_signature(params)
# #     #             resp = self.HTTP_request('other', self.cancel_order_url, method='DELETE',
# #     #                                     headers=self.headers, params=params, proxies=self.proxiess)
# #     #             if resp.status_code == 200:
# #     #                 return resp
# #     #         except Exception as ex:
# #     #             print(f"Ошибка при отмене ордера {orderId}: {ex}")
# #     #         attempt += 1
# #     #         sleep(1)
# #     #     return None

# #     # def cancel_secondary_open_orders(self, symbol):
# #     #     id_list = [self.sl_order_id, self.tp_order_id]
# #     #     for orderId in id_list:
# #     #         if orderId is not None:
# #     #             resp = self.cancel_order_by_id(symbol, orderId)
# #     #             if resp is not None:
# #     #                 print(f"Ордер {orderId} успешно отменен.")
# #     #             else:
# #     #                 print(f"Не удалось отменить ордер {orderId}")
# #     #     return

# # # import ta

# # #     def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
# # #         data[f"EMA{ema1_period}"] = ta.trend.ema_indicator(data['Close'], window=ema1_period)
# # #         data[f"EMA{ema2_period}"] = ta.trend.ema_indicator(data['Close'], window=ema2_period)
# # #         data[f"EMA{ema3_period}"] = ta.trend.ema_indicator(data['Close'], window=ema3_period) 
# # #         data.dropna(inplace=True)
# # #         return data
# # import pandas as pd
# # import pandas_ta as ta
# # from tradingview_ta import get_multiple_analysis
# # from random import choice
# # from api_binance import BINANCE_API
# # import time

# # class INDICATORS(BINANCE_API):
# #     def __init__(self) -> None:
# #         super().__init__()  
# #         # устанавливаем функциии декораторы
# #         self.calculate_ema = self.log_exceptions_decorator(self.calculate_ema)
# #         self.calculate_atr = self.log_exceptions_decorator(self.calculate_atr)

# #     def indicators_documentation(self):
# #         """
# #             # номера стратегии индикаторов:
# #             1 -- 'ema_crossover': классическая стратегия прересечения двух ema (кроссовер)
# #             2 -- 'ema_crossover + trend_line': кроссовер ema плюс ориентироваться на линию тренда ema. Период равен ema_trend_line (сейчас 240). (Смотри в настройках программы)
# #             3 -- 'ema_crossover + stoch_rsi_crossover': ema кроссовер плюс кроссовер стохастик-рси
# #             4 -- 'ema_crossover + stoch_rsi_crossover + trend_line': ema кроссовер плюс кроссовер стохастик-рси плюс линия тренда
# #             5 -- 'ema_crossover + stoch_rsi_overTrade': ema кроссовер плюс овертрейд стохастик-рси
# #             6 -- 'ema_crossover + stoch_rsi_overTrade + trend_line': то же что и предыдущий, но плюс ориентрироваться на линию тренда
# #             7 - 'smart_random + trend_line' # рандомный выбор сигнала c ориентацией на тренд. Рекомендуется использовать только для тестов
# #             8 -- 'trading_view_ind' -- индикатор библиотеки трейдинг вью
# #             9 -- 'trading_view_ind + trend_line' -- индикатор библиотеки трейдинг вью + трендовая линия
# #             10 -- 'ema_crossover + vpvr_level' # кроссовер ema плюс + vpvr индикатор
# #         """
   
# #     def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
# #         close = data['Close']
# #         ema1 = close.ewm(span=ema1_period, adjust=False).mean()
# #         ema2 = close.ewm(span=ema2_period, adjust=False).mean()
# #         ema3 = close.ewm(span=ema3_period, adjust=False).mean()
# #         data[f"EMA{ema1_period}"] = ema1
# #         data[f"EMA{ema2_period}"] = ema2
# #         data[f"EMA{ema3_period}"] = ema3
# #         data.dropna(inplace=True)

# #         return data    

# #     def calculate_stoch_rsi(self, data):
# #         close = data['Close']
# #         window = 14
# #         smooth1 = 3
# #         smooth2 = 3

# #         # Рассчитываем RSI
# #         delta = close.diff()
# #         gain = delta.where(delta > 0, 0)
# #         loss = -delta.where(delta < 0, 0)

# #         avg_gain = gain.rolling(window=window, min_periods=1).mean()
# #         avg_loss = loss.rolling(window=window, min_periods=1).mean()

# #         rs = avg_gain / avg_loss
# #         rsi = 100 - (100 / (1 + rs))

# #         # Рассчитываем стохастический RSI
# #         min_rsi = rsi.rolling(window=window, min_periods=1).min()
# #         max_rsi = rsi.rolling(window=window, min_periods=1).max()

# #         stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)
# #         stoch_rsi_k = stoch_rsi.rolling(window=smooth1, min_periods=1).mean()
# #         stoch_rsi_d = stoch_rsi_k.rolling(window=smooth2, min_periods=1).mean()

# #         data['StochRSI_%K'] = stoch_rsi_k * 100  # Приводим к диапазону 0-100
# #         data['StochRSI_%D'] = stoch_rsi_d * 100  # Приводим к диапазону 0-100
# #         data.dropna(inplace=True)

# #         return data

# #     def calculate_atr(self, data, atr_period):
# #         high = data['High']
# #         low = data['Low']
# #         close = data['Close']

# #         # Рассчитываем True Range
# #         tr = []
# #         for i in range(1, len(data)):
# #             tr_high_low = high.iloc[i] - low.iloc[i]
# #             tr_high_close_prev = abs(high.iloc[i] - close.iloc[i - 1])
# #             tr_low_close_prev = abs(low.iloc[i] - close.iloc[i - 1])
# #             true_range = max(tr_high_low, tr_high_close_prev, tr_low_close_prev)
# #             tr.append(true_range)

# #         # Рассчитываем ATR
# #         atr = [None] * len(data)
# #         atr[atr_period - 1] = sum(tr[:atr_period]) / atr_period  # Первое значение ATR

# #         for i in range(atr_period, len(data)):
# #             atr[i] = (atr[i - 1] * (atr_period - 1) + tr[i]) / atr_period
        
# #         data[f"ATR{atr_period}"] = atr
# #         data.dropna(inplace=True)

# #         return data, atr[-1]


# #     # def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
# #     #     data[f"EMA{ema1_period}"] = ta.ema(data['Close'], length=ema1_period)
# #     #     data[f"EMA{ema2_period}"] = ta.ema(data['Close'], length=ema2_period)
# #     #     data[f"EMA{ema3_period}"] = ta.ema(data['Close'], length=ema3_period) 
# #     #     data.dropna(inplace=True)
# #     #     return data
    
# #     # def calculate_stoch_rsi(self, data):
# #     #     stoch_rsi = ta.stochrsi(data['Close'], length=14, rsi_length=14, k=3, d=3)
# #     #     data['StochRSI_%K'] = stoch_rsi['STOCHRSIk_14_14_3_3']
# #     #     data['StochRSI_%D'] = stoch_rsi['STOCHRSId_14_14_3_3']
# #     #     data.dropna(inplace=True)
# #     #     return data 
    
# #     # def calculate_atr(self, data, atr_period):
# #     #     data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
# #     #     data.dropna(inplace=True)
# #     #     return data, data[f"ATR{atr_period}"].iloc[-1]
    
# #     def calculate_vpvr(self, data, min_bins=10, max_bins=50):
# #         # Вычисляем динамическое количество корзин (bins) на основе количества свечей
# #         num_candles = self.ema_trend_line
# #         bins = min(max(min_bins, num_candles // 10), max_bins)
# #         data = data.tail(self.ema_trend_line)
# #         # print(data)        
# #         # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
# #         price_range = pd.cut(data['Close'], bins=bins)
# #         vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
# #         return vpvr

# #     def find_vpvr_levels(self, vpvr, num_levels=2):
# #         # Поиск наиболее объемных зон VPVR
# #         top_vpvr_indexes = vpvr.nlargest(num_levels).index
# #         vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
# #         return vpvr_levels
    
# #     def immediate_vpvr_level_defender(self, cur_price, vpvr_levels):
# #         disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
# #                     (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
# #         if not disposition:
# #             immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
# #             strongest_volum_level = [0, 0]

# #             for _, _, m, v in vpvr_levels:
# #                 cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
# #                 if cur_volum_level > strongest_volum_level[0]:
# #                     strongest_volum_level = [cur_volum_level, m]                                

# #             if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
# #                 return "L", immediate_level
# #             elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
# #                 return "S", immediate_level
# #             elif strongest_volum_level[1] > cur_price:
# #                 return "L", strongest_volum_level[1]
# #             elif strongest_volum_level[1] < cur_price:
# #                 return "L", strongest_volum_level[1]

# #         return
    
# #     # /////// trading view indicator:
# #     def get_tv_signals(self, coins_list):

# #         all_coins_indicators = None
# #         signals_list = []      
# #         symbols = [f"BINANCE:{x}" for x in coins_list if x]

# #         all_coins_indicators = get_multiple_analysis(symbols=symbols,
# #                             screener='crypto',                    
# #                             interval=self.interval)

# #         for _, item in all_coins_indicators.items():
# #             recommendation = None
# #             symbol = None
# #             try:
# #                 symbol = item.symbol
# #                 recommendation = item.summary["RECOMMENDATION"]
# #             except:
# #                 continue
# #             if (recommendation == 'STRONG_BUY'):
# #                 signals_list.append((symbol, 1))          

# #             elif (recommendation == 'STRONG_SELL'):
# #                 signals_list.append((symbol, -1))             

# #         return signals_list  



# # def calculate_atr1(data, atr_period=14):
# #     data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
# #     data.dropna(inplace=True)
# #     return data, data[f"ATR{atr_period}"].iloc[-1]
# # def calculate_atr2(data, atr_period=14):
# #     high = data['High'].values
# #     low = data['Low'].values
# #     close = data['Close'].values

# #     tr = [0] * len(data)
# #     atr = [0] * len(data)

# #     tr[0] = high[0] - low[0]

# #     # Calculate True Range (TR)
# #     for i in range(1, len(data)):
# #         tr_high_low = high[i] - low[i]
# #         tr_high_close_prev = abs(high[i] - close[i - 1])
# #         tr_low_close_prev = abs(low[i] - close[i - 1])
# #         tr[i] = max(tr_high_low, tr_high_close_prev, tr_low_close_prev)

# #     # Calculate ATR
# #     atr[atr_period - 1] = sum(tr[:atr_period]) / atr_period

# #     for i in range(atr_period, len(data)):
# #         atr[i] = (atr[i - 1] * (atr_period - 1) + tr[i]) / atr_period

# #     data_copy = data.copy()
# #     data_copy[f"ATR{atr_period}"] = atr
# #     data_copy.dropna(inplace=True)

# #     return data_copy, atr[-1]

# # # Пример использования
# # indnd = INDICATORS()
# # data = indnd.get_klines('BTCUSDT', '1m', 240)

# # # Вызов функции calculate_atr2
# # new_data1, atr_value1 = calculate_atr1(data)
# # new_data2, atr_value = calculate_atr2(data)

# # # Вывод результата
# # # print(new_data2)
# # print(f"Последнее значение ATR{14}: {atr_value1}")
# # print(f"Последнее значение ATR{14}: {atr_value}")



# # # indnd = INDICATORS()

# # # data = indnd.get_klines('BTCUSDT', '1m', 240)
# # # # new_data1 = calculate_atr1(data)
# # # new_data2 = calculate_atr2(data)
# # # # new_data1 = calculate_stoch_rsi_pandas_ta(data)
# # # # new_data2 = calculate_stoch_rsi(data)
# # # # print(new_data1)
# # # print(new_data2)

# # def fooo(init_order_price, oposit_order_price, depo):
# #     if - 0.009 <= (abs(init_order_price - oposit_order_price)/ init_order_price)* depo <= 0.009:
# #         return 0, init_order_price, oposit_order_price   
# #     if init_order_price - oposit_order_price > 0:
# #         return -1, init_order_price, oposit_order_price
# #     elif init_order_price - oposit_order_price < 0:
# #         return 1, init_order_price, oposit_order_price

# # print(fooo(0.000041, 0.000041000004, 10))






# # from infoo import INFO
# # import time
# # import os
# # import inspect

# # current_file = os.path.basename(__file__)

# # class TEMPLATES(INFO):
# #     def __init__(self):
# #         super().__init__()
# #         # устанавливаем функции-декораторы
# #         self.for_set_open_position_temp = self.log_exceptions_decorator(self.for_set_open_position_temp)
# #         self.for_set_stops_orders_temp = self.log_exceptions_decorator(self.for_set_stops_orders_temp)
# #         self.set_leverage_template = self.log_exceptions_decorator(self.set_leverage_template)
# #         self.get_top_coins_template = self.log_exceptions_decorator(self.get_top_coins_template)
# #         self.set_trade_nessasareses_templates = self.log_exceptions_decorator(self.set_trade_nessasareses_templates)
# #         self.make_orders_template_shell = self.log_exceptions_decorator(self.make_orders_template_shell)
# #         self.make_sl_tp_template = self.log_exceptions_decorator(self.make_sl_tp_template)

# #     def set_leverage_template(self):
# #         self.handle_messagee("Устанавливаем кредитное плечо:")
# #         set_leverage_resp = self.set_leverage(self.symbol, self.lev_size)
# #         self.handle_messagee(str(set_leverage_resp))
# #         return True 

# #     def get_top_coins_template(self):
# #         all_binance_tickers = self.get_all_tickers()
# #         coinsMarket_tickers = []
# #         if self.in_coinMarketCup_is:
# #             coinsMarket_tickers = self.coin_market_cup_top(self.TOP_MARKET_CUP)
# #         return self.go_filter(all_binance_tickers, coinsMarket_tickers)

# #     def set_trade_nessasareses_templates(self):
# #         try:
# #             set_margin_resp = self.set_margin_type(self.symbol, self.margin_type)
# #             self.handle_messagee(str(set_margin_resp))
# #             if not self.was_change_leverage_true:
# #                 self.set_leverage_template()
# #             trade_data_mess = f"Размер ставки: {self.depo}\nКредитное плечо: {self.lev_size}"
# #             self.handle_messagee(trade_data_mess)
# #         except Exception as ex:
# #             self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")

# #     def make_orders_template_shell(self):
# #         def make_orders_template(qty, market_type, target_price):
# #             order_answer = {}
# #             response_list = []
# #             side = 'BUY' if self.current_signal_val == 1 else 'SELL'
# #             if market_type == 'MARKET':
# #                 self.set_trade_nessasareses_templates()
# #             try:
# #                 order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
# #                 self.order_id = order_answer.get('orderId', None)
# #                 response_list.append(order_answer)
# #             except Exception as ex:
# #                 self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
# #             return response_list, self.response_order_logger(order_answer, side, market_type)

# #         self.last_direction = self.current_signal_val
# #         self.response_trading_list, self.create_order_success_flag = make_orders_template(self.qty, 'MARKET', None)

# #         if not self.create_order_success_flag:
# #             return False       

# #         return True

# #     def make_sl_tp_template(self, qty, market_type_list, target_price_list):
# #         order_answer = None
# #         sl_order_id = None
# #         tp_order_id = None
# #         response_success_list = []
# #         side = 'BUY' if self.current_signal_val == -1 else 'SELL'
# #         for market_type, target_price in zip(market_type_list, target_price_list):
# #             try:
# #                 order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
# #                 if market_type == 'STOP_MARKET':
# #                     sl_order_id = order_answer.get('orderId', None)

# #                 if market_type == 'TAKE_PROFIT_MARKET' or market_type == 'LIMIT':
# #                     tp_order_id = order_answer.get('orderId', None)

# #                 response_success_list.append(self.response_order_logger(order_answer, side, market_type))
# #                 time.sleep(0.1)
# #             except Exception as ex:
# #                 self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
# #         return all(response_success_list), sl_order_id, tp_order_id

# #     def for_set_open_position_temp(self):
# #         symbol_info = self.get_excangeInfo()
# #         self.qty, self.price_precession, self.price_precession_limit = self.usdt_to_qnt_converter(self.symbol, self.depo, symbol_info, self.cur_price)
# #         self.handle_messagee(f"qty, cur_price:\n{self.qty}, {self.cur_price}")

# #     def for_set_stops_orders_temp(self, response_trading_list, qty, cur_price):
# #         executed_qty = float(response_trading_list[0].get('executedQty', qty))
# #         self.last_enter_price = enter_price = float(response_trading_list[0].get('avgPrice', cur_price))
# #         self.handle_messagee(f"qty, enter_price:\n{executed_qty}, {enter_price}")
# #         return enter_price, executed_qty

# # from random import choice

# # long_trend = False
# # short_trend = False
# # long_count = 0
# # short_count = 0
# # # strategy_list = ['trande_shift_random']
# # # strategy_list = ['long_shift_random']
# # # strategy_list = ['short_shift_random']
# # strategy_list = ['simple_random']

# # for i in range(100):
# #     if 'simple_random' in strategy_list:
# #         random_list = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
# #         if choice(random_list) % 2 != 0:
# #             long_count += 1
# #         else:
# #             short_count += 1

# #     if {'trande_shift_random', 'long_shift_random', 'short_shift_random'} & set(strategy_list):
# #         if 'trande_shift_random' in strategy_list:
# #             if long_trend:
# #                 random_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2]

# #             elif short_trend:
# #                 random_list = [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1]

# #             if long_trend or short_trend:                         
# #                 if choice(random_list) % 2 != 0:
# #                     long_count += 1
# #                 else:
# #                     short_count += 1
# #         else:
# #             if 'long_shift_random' in strategy_list:
# #                 random_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2]
# #             if 'short_shift_random' in strategy_list:
# #                 random_list = [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1]
# #             if choice(random_list) % 2 != 0:
# #                 long_count += 1
# #             else:
# #                 short_count += 1

# # print(long_count)
# # print(short_count)
# # if short_count != 0 and long_count != 0:
# #     if 'long_shift_random' in strategy_list or long_trend or 'simple_random' in strategy_list:
# #         print(f"relation: {long_count/short_count}")
# #     elif 'short_shift_random' in strategy_list or short_trend:
# #         print(f"relation: {short_count/long_count}")

# import pandas_ta as ta
# from api_binance import BINANCE_API

# def calculate_ema_1(data):
#     close = data['Close']
#     ema1 = close.ewm(span=5, adjust=False).mean()
#     ema2 = close.ewm(span=20, adjust=False).mean()
#     ema3 = close.ewm(span=240, adjust=False).mean()
#     data[f"EMA{5}"] = ema1
#     data[f"EMA{20}"] = ema2
#     data[f"EMA{240}"] = ema3
#     data.dropna(inplace=True)
#     return data   

# def calculate_ema_2(data):
#     data[f"EMA{5}"] = ta.ema(data['Close'], length=5)
#     data[f"EMA{20}"] = ta.ema(data['Close'], length=20)
#     data[f"EMA{240}"] = ta.ema(data['Close'], length=240) 
#     data.dropna(inplace=True)
#     return data

# ba = BINANCE_API()

# data = ba.get_klines('BTCUSDT', '1m', 240)
# print(f"ema 1: {calculate_ema_1(data).get('EMA5', None)}")
# print(f"ema 2: {calculate_ema_2(data).get('EMA5', None)}")

# top_pairs_total = [1,2,3,4,5]
# coinsMarket_tickers = [3,4,5,6,7,8]

# print(set(top_pairs_total) & set(coinsMarket_tickers))

# a = [1,2,3,4]
# a.pop(2)
# print(a)

# import yfinance as yf
# import backtrader as bt
# import pandas as pd

# # Загрузка данных с помощью yfinance
# btc_usdt = yf.download('BTC-USD', start='2020-01-01', end='2023-12-31')

# # Убедитесь, что данные имеют правильный формат
# btc_usdt.index = pd.to_datetime(btc_usdt.index)

# # Определение индикатора Keltner Channel
# class KeltnerChannel(bt.Indicator):
#     lines = ('mid', 'top', 'bot')
#     params = (('period', 20), ('devfactor', 1.5),)

#     def __init__(self):
#         self.atr = bt.indicators.ATR(self.data, period=self.p.period)
#         print(self.atr)
#         self.mid = bt.indicators.SMA(self.data.close, period=self.p.period)
#         self.lines.top = self.mid + self.p.devfactor * self.atr
#         self.lines.bot = self.mid - self.p.devfactor * self.atr
#         self.lines.mid = self.mid

# class EMAStrategy(bt.Strategy):
#     params = (
#         ('ema_short', 5),
#         ('ema_long', 20),
#         ('atr_period', 14),
#         ('risk_reward_ratio', 1),
#         ('commission', 0.001),  # Комиссия Binance 0.1%
#     )

#     def __init__(self):
#         self.ema_short = bt.indicators.EMA(self.data.close, period=self.params.ema_short)
#         self.ema_long = bt.indicators.EMA(self.data.close, period=self.params.ema_long)
#         self.atr = bt.indicators.AverageTrueRange(self.data, period=self.params.atr_period)
#         self.bollinger = bt.indicators.BollingerBands(self.data, period=20, devfactor=2)
#         self.keltner = KeltnerChannel(self.data, period=20, devfactor=1.5)
#         self.order = None

#     def next(self):
#         if self.order:
#             return  # Если есть открытый ордер, не делаем ничего
#         # print(self.bollinger.top)
#         if self.data.close[0] < self.bollinger.top[0] and self.data.close[0] > self.bollinger.bot[0] and \
#            self.data.close[0] < self.keltner.top[0] and self.data.close[0] > self.keltner.bot[0]:
#             return

#         if self.ema_short > self.ema_long:
#             stop_loss = self.data.close[0] * (1 - 0.005)
#             print(stop_loss)
#             take_profit = self.data.close[0] * (1 + 0.005)
#             print(take_profit)
#             if not self.position:
#                 self.order = self.buy()
#                 self.sell(exectype=bt.Order.Stop, price=stop_loss)
#                 self.sell(exectype=bt.Order.Limit, price=take_profit)
#         elif self.ema_short < self.ema_long:
#             stop_loss = self.data.close[0] * (1 + 0.005)
#             take_profit = self.data.close[0] * (1 - 0.005)
#             if not self.position:
#                 self.order = self.sell()
#                 self.buy(exectype=bt.Order.Stop, price=stop_loss)
#                 self.buy(exectype=bt.Order.Limit, price=take_profit)

#     def notify_order(self, order):
#         if order.status in [order.Completed, order.Canceled, order.Margin]:
#             self.order = None

# class FixedSize(bt.Sizer):
#     params = (('stake', 100),)

#     def _getsizing(self, comminfo, cash, data, isbuy):
#         return self.params.stake

# if __name__ == '__main__':
#     cerebro = bt.Cerebro()
#     cerebro.addstrategy(EMAStrategy)
#     cerebro.addsizer(FixedSize)

#     # Преобразование данных для backtrader
#     data_feed = bt.feeds.PandasData(dataname=btc_usdt)
#     cerebro.adddata(data_feed)

#     cerebro.broker.setcommission(commission=0.001)
#     cerebro.broker.setcash(10000)

#     initial_cash = cerebro.broker.getvalue()
#     cerebro.run()
#     final_cash = cerebro.broker.getvalue()

#     print(f'Начальный капитал: {initial_cash}')
#     print(f'Конечный капитал: {final_cash}')
#     print(f'Прибыль: {final_cash - initial_cash}')

#     cerebro.plot()


# import pandas as pd
# import numpy as np

# # Точная функция для расчета ATR
# def calculate_atr(df, period=14):
#     high = df['High']
#     low = df['Low']
#     close = df['Close']
    
#     tr = pd.DataFrame(index=df.index)
#     tr['TR'] = np.maximum(high - low, np.maximum(abs(high - close.shift()), abs(low - close.shift())))
#     atr = tr['TR'].rolling(window=period, min_periods=1).mean()
#     return atr

# # Функция для расчета индикаторов
# def calculate_indicators(df):
#     df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
#     df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
#     df['ATR'] = calculate_atr(df, period=14)
#     df['BB_Middle'] = df['Close'].rolling(window=20).mean()
#     df['BB_Upper'] = df['BB_Middle'] + (df['Close'].rolling(window=20).std() * 2)
#     df['BB_Lower'] = df['BB_Middle'] - (df['Close'].rolling(window=20).std() * 2)
#     df['KC_Middle'] = df['Close'].rolling(window=20).mean()
#     df['KC_Upper'] = df['KC_Middle'] + (1.5 * df['ATR'])
#     df['KC_Lower'] = df['KC_Middle'] - (1.5 * df['ATR'])
#     return df

# # Функция для фильтрации монет по волатильности
# def filter_volatile_coins(df, atr_threshold):
#     return df[df['ATR'] > atr_threshold]

# # Функция для генерации сигналов
# def generate_signals(df):
#     df['Signal'] = np.where(df['EMA5'] > df['EMA20'], 1, -1)
#     df['ATR_Trend'] = df['ATR'] / df['ATR'].rolling(window=14).mean()
#     df['Filtered_Signal'] = np.where((df['Signal'] != 0) & (df['ATR_Trend'] < 1.5), df['Signal'], 0)
#     return df[df['Filtered_Signal'] != 0]

# # Функция для фильтрации сигналов во флете
# def filter_flat_signals(df):
#     return df[(df['Close'] < df['BB_Upper']) & (df['Close'] > df['BB_Lower']) & 
#               (df['Close'] < df['KC_Upper']) & (df['Close'] > df['KC_Lower'])]

# # Загрузка данных
# data = pd.read_csv('your_data.csv', parse_dates=True, index_col='Date')
# data = calculate_indicators(data)

# # Фильтрация волатильных монет
# volatile_data = filter_volatile_coins(data, atr_threshold=0.01)  # Замените значение порога на подходящее для вашего рынка

# # Генерация сигналов
# signals = generate_signals(volatile_data)

# # Фильтрация сигналов во флете
# filtered_signals = filter_flat_signals(signals)

# # Вывод сигналов
# print(filtered_signals[['Close', 'Signal', 'Filtered_Signal']])

        # return df[(df['Close'] < df['BB_Upper']) & (df['Close'] > df['BB_Lower']) & 
        #         (df['Close'] < df['KC_Upper']) & (df['Close'] > df['KC_Lower'])]


    
    # def calculate_BB(self, df):
    #     df['BB_Upper'] = df[f"EMA{self.ema2_period}"] + (df[f"EMA{self.ema2_period}"].std() * self.degree_of_BB_rigidity)
    #     df['BB_Lower'] = df[f"EMA{self.ema2_period}"] - (df[f"EMA{self.ema2_period}"].std() * self.degree_of_BB_rigidity)
    #     return df 
    # def calculate_KC(self, df, atr_period):
    #     df['KC_Upper'] = df[f"EMA{self.ema2_period}"] + (self.degree_of_KC_rigidity * df[f"ATR{atr_period}"])
    #     df['KC_Lower'] = df[f"EMA{self.ema2_period}"] - (self.degree_of_KC_rigidity * df[f"ATR{atr_period}"])

    # def in_flate(self, df):
    #     last_6_rows = df.iloc[-6:]
    #     return (last_6_rows['lower_band'] > last_6_rows['lower_keltner']).all() and \
    #         (last_6_rows['upper_band'] < last_6_rows['upper_keltner']).all()


    # def filter_flat_coins_by_BB_and_KC(self, data, atr_period):
    #     df = data.copy()
    #     df['sma'] = df['Close'].rolling(window=atr_period).mean()
    #     df['stddev'] = df['Close'].rolling(window=atr_period).std()
    #     df['lower_band'] = df['sma'] - (self.BB_stddev_MULTIPLITER * df['stddev'])
    #     df['upper_band'] = df['sma'] + (self.BB_stddev_MULTIPLITER * df['stddev'])

    #     # df['TR'] = abs(df['High'] - df['Low'])
    #     # df['ATR'] = df['TR'].rolling(window=60).mean()
    #     df, _ = self.calculate_atr(df, atr_period)
    #     df['lower_keltner'] = df['sma'] - ([f"ATR{atr_period}"] * self.KC_stddev_MULTIPLITER)
    #     df['upper_keltner'] = df['sma'] + ([f"ATR{atr_period}"] * self.KC_stddev_MULTIPLITER)
    #     # df = data.copy()
    #     # df['stddev'] = df[f"EMA{self.ema2_period}"].std()
    #     # df['lower_band'] = df[f"EMA{self.ema2_period}"] - (self.BB_stddev_MULTIPLITER * df['stddev'])
    #     # df['upper_band'] = df[f"EMA{self.ema2_period}"] + (self.BB_stddev_MULTIPLITER * df['stddev'])

    #     # df['lower_keltner'] = df[f"EMA{self.ema2_period}"] - (df[f"ATR{atr_period}"] * self.KC_stddev_MULTIPLITER)
    #     # df['upper_keltner'] = df[f"EMA{self.ema2_period}"] + (df[f"ATR{atr_period}"] * self.KC_stddev_MULTIPLITER)
        
    #     # Проверяем условие для последних шести строк
    #     last_6_rows = df.iloc[-6:]
    #     return (last_6_rows['lower_band'] > last_6_rows['lower_keltner']).all() & \
    #            (last_6_rows['upper_band'] < last_6_rows['upper_keltner']).all()

        # # Расчет ATR
        # # df, _ = self.calculate_atr(df, atr_period)
        # df['TR'] = abs(df['High'] - df['Low'])
        # df[f"ATR{atr_period}"] = df['TR'].rolling(window=atr_period).mean()
        # df.dropna(inplace=True)
        # # Проверка наличия колонки ATR
        # atr_column_name = f"ATR{atr_period}"
        # if atr_column_name not in df.columns:
        #     raise KeyError(f"Column '{atr_column_name}' not found in DataFrame after calculating ATR.")
        # print(df)
        # df = df.iloc[-self.ema2_period:]

        # print(last_6_rows[['lower_band', 'lower_keltner', 'upper_band', 'upper_keltner', atr_column_name]])





    # def change_volatility_indicator(self, df, atr_period):
    #     # Установка периодов для расчета скользящего среднего ATR
    #     atr_period1 = self.ema1_period
    #     atr_period2 = self.ema2_period

    #     # Получение текущих значений ATR для заданного периода
    #     atr_rolling_mean = df[f"ATR{atr_period}"]

    #     # Расчет скользящих средних ATR для двух различных периодов
    #     atr_rolling_mean_1 = atr_rolling_mean.rolling(window=atr_period1).mean()
    #     atr_rolling_mean_2 = atr_rolling_mean.rolling(window=atr_period2).mean()

    #     # Вычисление текущего отношения ATR к его более длинному скользящему среднему
    #     atr_cur_moving = atr_rolling_mean.iloc[-1] / atr_rolling_mean_2.iloc[-1]

    #     # Вычисление отношения более короткого скользящего среднего ATR к более длинному
    #     atr_mean_moving = atr_rolling_mean_1.iloc[-1] / atr_rolling_mean_2.iloc[-1]

    #     # Условия для оценки консистенции изменения скорости, флэта и средней консистенции
    #     speed_change_consistence = atr_cur_moving > self.degree_of_ATR_rigidity_upper
    #     flat_consistence = atr_mean_moving < self.degree_of_ATR_rigidity_lower
    #     average_consistence = self.degree_of_ATR_rigidity_lower <= atr_mean_moving <= self.degree_of_ATR_rigidity_upper

    #     # # Вывод значений для отладки
    #     # print(f"atr_cur_moving: {atr_cur_moving}")
    #     # print(f"atr_mean_moving: {atr_mean_moving}")
    #     # print(f"speed_change_consistence: {speed_change_consistence}")
    #     # print(f"flat_consistence: {flat_consistence}")
    #     # print(f"average_consistence: {average_consistence}")

    #     # Возвращаем три булевых значения, указывающих на состояние волатильности
    #     return speed_change_consistence, flat_consistence, average_consistence





    # def detect_anomalous_volume(self, df):
    #     # Расчет среднего и стандартного отклонения объема
    #     df['AverageVolume'] = df['Volume'].rolling(window=self.average_window).mean()
    #     df['StdVolume'] = df['Volume'].rolling(window=self.average_window).std()

    #     # Расчет верхней границы для аномального объема
    #     df['UpperVolumeLimit'] = df['AverageVolume'] + self.std_multiplier * df['StdVolume']

    #     # Определение, является ли текущий объем аномальным
    #     df['AnomalousVolume'] = df['Volume'] > df['UpperVolumeLimit']

    #     return df['AnomalousVolume']


# import pandas as pd

# class VolumeAnomalyDetector:
#     def __init__(self, average_window=20, std_multiplier=2.0):
#         self.average_window = average_window  # окно для расчета среднего объема
#         self.std_multiplier = std_multiplier  # множитель для стандартного отклонения
#         self.std_multiplier_flag = False

#     def detect_anomalous_volume(self, df):
#         # Расчет среднего и стандартного отклонения объема
#         df['AverageVolume'] = df['Volume'].rolling(window=self.average_window).mean()
#         if self.std_multiplier_flag:
#             df['StdVolume'] = df['Volume'].rolling(window=self.average_window).std()

#             # Расчет верхней границы для аномального объема
#             df['UpperVolumeLimit'] = df['AverageVolume'] + self.std_multiplier * df['StdVolume']
#         else:
#             pass

#         # Определение, является ли текущий объем аномальным
#         df['AnomalousVolume'] = df['Volume'] > df['UpperVolumeLimit']

#         # Определение направления последней свечи (зеленый или красный)
#         last_close = df['Close'].iloc[-1]
#         last_open = df['Open'].iloc[-1]
#         last_volume = df['Volume'].iloc[-1]

#         if last_close > last_open:
#             candle_direction = 'green'
#         elif last_close < last_open:
#             candle_direction = 'red'
#         else:
#             candle_direction = 'neutral'  # если цены открытия и закрытия равны

#         return df['AnomalousVolume'].iloc[-1], candle_direction

# import pandas as pd
# import numpy as np

# class VolumeIndicator:
#     def __init__(self):
#         self.average_window = 20
#         self.percentile = 0.95
    
#     def detect_anomalous_volume(self, df):
#         is_anomalousVolume_true = False
#         # 1. Вычисляем скользящее среднее по объему
#         df['AverageVolume'] = df['Volume'].rolling(window=self.average_window).mean()

#         # df['StdVolume'] = df['Volume'].rolling(window=self.average_window).std()

#         # # Расчет средней верхней границы объема
#         # df['UpperVolumeLimit'] = df['AverageVolume'] + df['StdVolume']
#         # print(df['UpperVolumeLimit'].iloc[-1])
        
#         # 2. Рассчитываем перцентиль 95-го процентиля без последнего значения
#         percentile_value = df['Volume'].iloc[:-1].rolling(window=self.average_window).quantile(q=self.percentile)

#         # Выводим значение перцентиля
#         print(percentile_value.iloc[-1])

#         # # 3. Проверяем условия аномального объема
#         # conditions = []
#         # for i in range(-6, -1):
#         #     if df['Volume'].iloc[i] <= df['UpperVolumeLimit'].iloc[i]:
#         #         conditions.append(True)
#         #     else:
#         #         conditions.append(False)
        
#         # 3. Проверяем условия аномального объема
#         conditions = []
#         for i in range(-6, -1):
#             if df['Volume'].iloc[i] < percentile_value.iloc[-1]:
#                 conditions.append(True)
#             else:
#                 conditions.append(False)              
        
#         # 4. Последняя свеча выше значения перцентиля
#         last_candle_condition = df['Volume'].iloc[-1] > percentile_value.iloc[-1]
        
#         # 5. Проверяем все условия
#         is_anomalousVolume_true = np.all(conditions) and last_candle_condition
        
#         # 6. Определение направления объема (зеленый или красный)
#         df['VolumeDirection'] = np.where(df['Close'] > df['Open'], 'Green', 'Red')

#         return is_anomalousVolume_true, df['VolumeDirection']

# # Пример использования
# if __name__ == "__main__":
#     # Пример данных
#     data = {
#         'Open': [100, 105, 102, 98, 105, 110, 112, 100, 105, 102, 98, 105, 110, 112, 100, 105, 102, 98, 105, 110, 112],
#         'Close': [102, 100, 99, 97, 106, 108, 115, 102, 100, 99, 97, 106, 108, 115, 102, 100, 99, 97, 106, 108, 115],
#         'Volume': [1000, 1200, 800, 3500, 2000, 1800, 1500, 1000, 1200, 800, 1500, 2000, 1800, 1500, 1000, 1200, 800, 1500, 2000, 1800, 22500]
#     }
#     df = pd.DataFrame(data)
    
#     # Создание экземпляра индикатора с параметрами
#     indicator = VolumeIndicator()
    
#     # Вызов функции для обнаружения аномального объема
#     anomalous_volume, volume_direction = indicator.detect_anomalous_volume(df)
    
#     # Вывод результатов
#     print("Аномальный объем:")
#     print(anomalous_volume)
#     print("\nНаправление объема (зеленый или красный):")
#     print(volume_direction.iloc[-1])

# import pandas_ta as ta
    # def calculate_ema(self, data):
    #     data[f"EMA{self.ema1_period}"] = ta.ema(data['Close'], length=self.ema1_period)
    #     data[f"EMA{self.ema2_period}"] = ta.ema(data['Close'], length=self.ema2_period)
    #     data[f"EMA{self.ema_trend_line}"] = ta.ema(data['Close'], length=self.ema_trend_line) 
    #     data.dropna(inplace=True)
    #     return data
    
    # def calculate_stoch_rsi(self, data):
    #     stoch_rsi = ta.stochrsi(data['Close'], length=14, rsi_length=14, k=3, d=3)
    #     data['StochRSI_%K'] = stoch_rsi['STOCHRSIk_14_14_3_3']
    #     data['StochRSI_%D'] = stoch_rsi['STOCHRSId_14_14_3_3']
    #     data.dropna(inplace=True)
    #     return data 
    
    # def calculate_atr(self, data, atr_period):
    #     data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
    #     data.dropna(inplace=True)
    #     return data, data[f"ATR{atr_period}"].iloc[-1]
        # print(ema1_period, self.ema2_period, ema3_period)
        # total_flat_list_BB_KC = []
        # total_flat_list_ATR = []
        # total_flat_list_EMA_DEGREE = []
        # total_flat_list_NONE_FILTERED = []

        # print(f"len_total_flat_list_BB_KC: {len(total_flat_list_BB_KC)}")
        # # print(f"total_flat_list_BB_KC: {total_flat_list_BB_KC}")
        # print(f"len_total_flat_list_ATR: {len(total_flat_list_ATR)}")
        # # print(f"total_flat_list_ATR: {total_flat_list_ATR}")

        # print(f"len_total_flat_list_EMA_DEGREE: {len(total_flat_list_EMA_DEGREE)}")
        # # print(f"total_flat_list_EMA_DEGREE: {total_flat_list_EMA_DEGREE}")
        # print(f"len_total_flat_list_NONE_FILTERED: {len(total_flat_list_NONE_FILTERED)}")
        # # print(f"total_flat_list_NONE_FILTERED: {total_flat_list_NONE_FILTERED}")



        # # Вывод значений для отладки
        # print(f"atr_cur_moving: {atr_cur_moving}")
        # print(f"atr_mean_moving: {atr_mean_moving}")
        # print(f"speed_change_consistence: {speed_change_consistence}")
        # print(f"flat_consistence: {flat_consistence}")
        # print(f"average_consistence: {average_consistence}")

        # Возвращаем три булевых значения, указывающих на состояние волатильности



    # def has_open_position(self, symbol):
    #     params = {
    #         "symbol": symbol,
    #         'recvWindow': 20000
    #     }
    #     params = self.get_signature(params)

    #     try:
    #         positions = self.session.get(
    #             self.positions_url, 
    #             headers=self.headers, 
    #             params=params, 
    #             proxies=self.proxiess if self.is_proxies_true else None
    #         )

    #         if positions.status_code == 200:
    #             positions = positions.json()
    #             for position in positions:
    #                 if position['symbol'] == symbol and float(position['positionAmt']) != 0:
    #                     return True
    #             return False
    #         else:
    #             print(f"Error fetching positions: {positions.status_code} - {positions.text}")
    #             return None
    #     except requests.exceptions.RequestException as e:
    #         print(f"Request exception: {e}")
    #     return None


    # def calculate_ema(self, data):
    #     data[f"EMA{self.ema1_period}"] = ta.ema(data['Close'], length=self.ema1_period)
    #     data[f"EMA{self.ema2_period}"] = ta.ema(data['Close'], length=self.ema2_period)
    #     data[f"EMA{self.ema_trend_line}"] = ta.ema(data['Close'], length=self.ema_trend_line) 
    #     data.dropna(inplace=True)
    #     return data
    
    # def calculate_wma(self, data):
    #     data[f"WMA{self.ema1_period}"] = ta.wma(data['Close'], length=self.ema1_period)
    #     data[f"WMA{self.ema2_period}"] = ta.wma(data['Close'], length=self.ema2_period)
    #     data[f"WMA{self.ema_trend_line}"] = ta.wma(data['Close'], length=self.ema_trend_line) 
    #     data.dropna(inplace=True)
    #     return data
