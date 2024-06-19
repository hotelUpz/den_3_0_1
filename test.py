# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from api_binance import BINANCE_API


# # # def calculate_vpvr(data, min_bins=10, max_bins=50):
# # #     # Вычисляем динамическое количество корзин (bins) на основе количества свечей
# # #     num_candles = 240
# # #     bins = min(max(min_bins, num_candles // 10), max_bins)
# # #     data = data.tail(240)
# # #     # print(data)        
# # #     # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
# # #     price_range = pd.cut(data['Close'], bins=bins)
# # #     vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
# # #     return vpvr

# # # def find_vpvr_levels(vpvr, num_levels=2):
# # #     # Поиск наиболее объемных зон VPVR
# # #     top_vpvr_indexes = vpvr.nlargest(num_levels).index
# # #     vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
# # #     return vpvr_levels

# # # def immediate_vpvr_level_defender(cur_price, vpvr_levels):
# # #     disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
# # #                 (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
# # #     if not disposition:
# # #         immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
# # #         strongest_volum_level = [0, 0]

# # #         for _, _, m, v in vpvr_levels:
# # #             cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
# # #             if cur_volum_level > strongest_volum_level[0]:
# # #                 strongest_volum_level = [cur_volum_level, m]                                

# # #         if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
# # #             return "L", immediate_level
# # #         elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
# # #             return "S", immediate_level
# # #         elif strongest_volum_level[1] > cur_price:
# # #             return "L", strongest_volum_level[1]
# # #         elif strongest_volum_level[1] < cur_price:
# # #             return "L", strongest_volum_level[1]

# # #     return

# # # def plot_vpvr(vpvr):
# # #     plt.barh(vpvr.index.astype(str), vpvr.values, height=0.5)
# # #     plt.ylabel('Price Range')
# # #     plt.xlabel('Volume')
# # #     plt.title('Volume Profile Visible Range (VPVR)')
# # #     plt.show()

# # # df = BINANCE_API().get_klines('BTCUSDT', '5m', 20)
# # # vpvr = calculate_vpvr(df)
# # # cur_price = df["Close"].iloc[-1]
# # # print(f"cur_price: {cur_price}")

# # # immediate_vpvr_level_defender_val = None
# # # vpvr = calculate_vpvr(df)                       
# # # vpvr_levels = find_vpvr_levels(vpvr)
# # # immediate_vpvr_level_defender_val = immediate_vpvr_level_defender(cur_price, vpvr_levels)

# # # if immediate_vpvr_level_defender_val:
# # #     if immediate_vpvr_level_defender_val[0] == 'L':
# # #         print("vpr indicator: Long")
# # #     elif immediate_vpvr_level_defender_val[0] == 'S':
# # #         print("vpr indicator: Short")
# # #     print(f"level: {immediate_vpvr_level_defender_val[1]}")

# # # plot_vpvr(vpvr)

    
# # #     # def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
# # #     #     symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
# # #     #     # print(symbol_data)
# # #     #     # //////////////////////
# # #     #     quantity_precision = int(float(symbol_data['quantityPrecision']))
# # #     #     price_precision = int(float(symbol_data['pricePrecision']))
# # #     #     # print(f"quantity_precision: {quantity_precision}")
# # #     #     min_notional = int(float(next((f['notional'] for f in symbol_data['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 0)))
# # #     #     if depo <= min_notional:
# # #     #         depo = min_notional
# # #     #     if (quantity_precision == 0 and (depo / cur_price) < 1) or depo < 5:
# # #     #         return "Too_litle_size", None            
# # #     #     return round(depo / cur_price, quantity_precision), price_precision 


# # # def count_decimal_places(number):
# # #     if isinstance(number, (int, float)):
# # #         # Преобразуем число в строку
# # #         number_str = f'{number:.10f}'.rstrip('0')
# # #         # Проверяем наличие десятичной точки
# # #         if '.' in number_str:
# # #             # Возвращаем количество знаков после запятой
# # #             return len(number_str.split('.')[1])
# # #     return 0

# # # import math
# # # str_number = '1.00105'
# # # float_number = float(str_number)
# # # price_precision_limit = count_decimal_places(float_number)
# # # print(price_precision_limit)

# # import aiohttp
# # import asyncio
# # import random
# # import json
# # from aiohttp_socks import ProxyConnector
# # from api_binance import BINANCE_API

# # class WEbss(BINANCE_API):
# #     def __init__(self):  
# #         super().__init__()

# #     def trailing_tp_sl_shell(self):
# #         async def stop_logic_price_monitoring():
# #             # print(qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id)
# #             symbol = 'BTCUSDT'
# #             # /////////////////////////////////////  
# #             url = 'wss://stream.binance.com:9443/ws/'
# #             # /////////////////////////////////////
# #             max_retries = 10
# #             retry_delay = 1  # seconds
# #             retries = 0
# #             # /////////////////////////////////////

# #             while retries < max_retries:            
# #                 try:
# #                     if self.is_proxies_true:
# #                         connector = ProxyConnector.from_url(f'socks5://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_socks5_port}')
# #                     async with aiohttp.ClientSession(connector=connector if self.is_proxies_true else None) as session:

# #                         async with session.ws_connect(url + f"{symbol}@kline_1s") as ws:
# #                             subscribe_request = {
# #                                 "method": "SUBSCRIBE",
# #                                 "params": [f"{symbol.lower()}@kline_1s"],
# #                                 "id": random.randrange(11,111111)
# #                             }
# #                             # print('Stop_logic_price_monitoring start processing!')                       
# #                             try:
# #                                 await ws.send_json(subscribe_request)
# #                             except:
# #                                 pass

# #                             async for msg in ws:
# #                                 if msg.type == aiohttp.WSMsgType.TEXT:
# #                                     try:
# #                                         data = json.loads(msg.data)
# #                                         kline_websocket_data = data.get('k', {})
# #                                         if kline_websocket_data:
# #                                             try:
# #                                                 cur_price = float(kline_websocket_data.get('c'))
# #                                                 print(f"last_close_price: {cur_price}")                              
                                
# #                                             except Exception as ex:
# #                                                 # print(ex)
# #                                                 pass
                                            
# #                                     except Exception as ex:
# #                                         continue

# #                 except Exception as ex:
# #                     print(f"An error occurred: {ex}")
# #                     retries += 1
# #                     await asyncio.sleep(retry_delay * (2 ** retries))  # Exponential backoff
# #             return
        
# #         asyncio.run(stop_logic_price_monitoring())

# # WEbss().trailing_tp_sl_shell()



#     # def cancel_order_by_id(self, symbol, orderId, retries=3):
#     #     attempt = 0
#     #     while attempt < retries:
#     #         try:
#     #             params = {
#     #                 'symbol': symbol,
#     #                 'orderId': orderId,
#     #                 'timestamp': int(time.time() * 1000)
#     #             }
#     #             params = self.get_signature(params)
#     #             resp = self.HTTP_request('other', self.cancel_order_url, method='DELETE',
#     #                                     headers=self.headers, params=params, proxies=self.proxiess)
#     #             if resp.status_code == 200:
#     #                 return resp
#     #         except Exception as ex:
#     #             print(f"Ошибка при отмене ордера {orderId}: {ex}")
#     #         attempt += 1
#     #         sleep(1)
#     #     return None

#     # def cancel_secondary_open_orders(self, symbol):
#     #     id_list = [self.sl_order_id, self.tp_order_id]
#     #     for orderId in id_list:
#     #         if orderId is not None:
#     #             resp = self.cancel_order_by_id(symbol, orderId)
#     #             if resp is not None:
#     #                 print(f"Ордер {orderId} успешно отменен.")
#     #             else:
#     #                 print(f"Не удалось отменить ордер {orderId}")
#     #     return

# # import ta

# #     def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
# #         data[f"EMA{ema1_period}"] = ta.trend.ema_indicator(data['Close'], window=ema1_period)
# #         data[f"EMA{ema2_period}"] = ta.trend.ema_indicator(data['Close'], window=ema2_period)
# #         data[f"EMA{ema3_period}"] = ta.trend.ema_indicator(data['Close'], window=ema3_period) 
# #         data.dropna(inplace=True)
# #         return data
# import pandas as pd
# import pandas_ta as ta
# from tradingview_ta import get_multiple_analysis
# from random import choice
# from api_binance import BINANCE_API
# import time

# class INDICATORS(BINANCE_API):
#     def __init__(self) -> None:
#         super().__init__()  
#         # устанавливаем функциии декораторы
#         self.calculate_ema = self.log_exceptions_decorator(self.calculate_ema)
#         self.calculate_atr = self.log_exceptions_decorator(self.calculate_atr)

#     def indicators_documentation(self):
#         """
#             # номера стратегии индикаторов:
#             1 -- 'ema_crossover': классическая стратегия прересечения двух ema (кроссовер)
#             2 -- 'ema_crossover + trend_line': кроссовер ema плюс ориентироваться на линию тренда ema. Период равен ema_trend_line (сейчас 240). (Смотри в настройках программы)
#             3 -- 'ema_crossover + stoch_rsi_crossover': ema кроссовер плюс кроссовер стохастик-рси
#             4 -- 'ema_crossover + stoch_rsi_crossover + trend_line': ema кроссовер плюс кроссовер стохастик-рси плюс линия тренда
#             5 -- 'ema_crossover + stoch_rsi_overTrade': ema кроссовер плюс овертрейд стохастик-рси
#             6 -- 'ema_crossover + stoch_rsi_overTrade + trend_line': то же что и предыдущий, но плюс ориентрироваться на линию тренда
#             7 - 'smart_random + trend_line' # рандомный выбор сигнала c ориентацией на тренд. Рекомендуется использовать только для тестов
#             8 -- 'trading_view_ind' -- индикатор библиотеки трейдинг вью
#             9 -- 'trading_view_ind + trend_line' -- индикатор библиотеки трейдинг вью + трендовая линия
#             10 -- 'ema_crossover + vpvr_level' # кроссовер ema плюс + vpvr индикатор
#         """
   
#     def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
#         close = data['Close']
#         ema1 = close.ewm(span=ema1_period, adjust=False).mean()
#         ema2 = close.ewm(span=ema2_period, adjust=False).mean()
#         ema3 = close.ewm(span=ema3_period, adjust=False).mean()
#         data[f"EMA{ema1_period}"] = ema1
#         data[f"EMA{ema2_period}"] = ema2
#         data[f"EMA{ema3_period}"] = ema3
#         data.dropna(inplace=True)

#         return data    

#     def calculate_stoch_rsi(self, data):
#         close = data['Close']
#         window = 14
#         smooth1 = 3
#         smooth2 = 3

#         # Рассчитываем RSI
#         delta = close.diff()
#         gain = delta.where(delta > 0, 0)
#         loss = -delta.where(delta < 0, 0)

#         avg_gain = gain.rolling(window=window, min_periods=1).mean()
#         avg_loss = loss.rolling(window=window, min_periods=1).mean()

#         rs = avg_gain / avg_loss
#         rsi = 100 - (100 / (1 + rs))

#         # Рассчитываем стохастический RSI
#         min_rsi = rsi.rolling(window=window, min_periods=1).min()
#         max_rsi = rsi.rolling(window=window, min_periods=1).max()

#         stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)
#         stoch_rsi_k = stoch_rsi.rolling(window=smooth1, min_periods=1).mean()
#         stoch_rsi_d = stoch_rsi_k.rolling(window=smooth2, min_periods=1).mean()

#         data['StochRSI_%K'] = stoch_rsi_k * 100  # Приводим к диапазону 0-100
#         data['StochRSI_%D'] = stoch_rsi_d * 100  # Приводим к диапазону 0-100
#         data.dropna(inplace=True)

#         return data

#     def calculate_atr(self, data, atr_period):
#         high = data['High']
#         low = data['Low']
#         close = data['Close']

#         # Рассчитываем True Range
#         tr = []
#         for i in range(1, len(data)):
#             tr_high_low = high.iloc[i] - low.iloc[i]
#             tr_high_close_prev = abs(high.iloc[i] - close.iloc[i - 1])
#             tr_low_close_prev = abs(low.iloc[i] - close.iloc[i - 1])
#             true_range = max(tr_high_low, tr_high_close_prev, tr_low_close_prev)
#             tr.append(true_range)

#         # Рассчитываем ATR
#         atr = [None] * len(data)
#         atr[atr_period - 1] = sum(tr[:atr_period]) / atr_period  # Первое значение ATR

#         for i in range(atr_period, len(data)):
#             atr[i] = (atr[i - 1] * (atr_period - 1) + tr[i]) / atr_period
        
#         data[f"ATR{atr_period}"] = atr
#         data.dropna(inplace=True)

#         return data, atr[-1]


#     # def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
#     #     data[f"EMA{ema1_period}"] = ta.ema(data['Close'], length=ema1_period)
#     #     data[f"EMA{ema2_period}"] = ta.ema(data['Close'], length=ema2_period)
#     #     data[f"EMA{ema3_period}"] = ta.ema(data['Close'], length=ema3_period) 
#     #     data.dropna(inplace=True)
#     #     return data
    
#     # def calculate_stoch_rsi(self, data):
#     #     stoch_rsi = ta.stochrsi(data['Close'], length=14, rsi_length=14, k=3, d=3)
#     #     data['StochRSI_%K'] = stoch_rsi['STOCHRSIk_14_14_3_3']
#     #     data['StochRSI_%D'] = stoch_rsi['STOCHRSId_14_14_3_3']
#     #     data.dropna(inplace=True)
#     #     return data 
    
#     # def calculate_atr(self, data, atr_period):
#     #     data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
#     #     data.dropna(inplace=True)
#     #     return data, data[f"ATR{atr_period}"].iloc[-1]
    
#     def calculate_vpvr(self, data, min_bins=10, max_bins=50):
#         # Вычисляем динамическое количество корзин (bins) на основе количества свечей
#         num_candles = self.ema_trend_line
#         bins = min(max(min_bins, num_candles // 10), max_bins)
#         data = data.tail(self.ema_trend_line)
#         # print(data)        
#         # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
#         price_range = pd.cut(data['Close'], bins=bins)
#         vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
#         return vpvr

#     def find_vpvr_levels(self, vpvr, num_levels=2):
#         # Поиск наиболее объемных зон VPVR
#         top_vpvr_indexes = vpvr.nlargest(num_levels).index
#         vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
#         return vpvr_levels
    
#     def immediate_vpvr_level_defender(self, cur_price, vpvr_levels):
#         disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
#                     (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
#         if not disposition:
#             immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
#             strongest_volum_level = [0, 0]

#             for _, _, m, v in vpvr_levels:
#                 cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
#                 if cur_volum_level > strongest_volum_level[0]:
#                     strongest_volum_level = [cur_volum_level, m]                                

#             if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
#                 return "L", immediate_level
#             elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
#                 return "S", immediate_level
#             elif strongest_volum_level[1] > cur_price:
#                 return "L", strongest_volum_level[1]
#             elif strongest_volum_level[1] < cur_price:
#                 return "L", strongest_volum_level[1]

#         return
    
#     # /////// trading view indicator:
#     def get_tv_signals(self, coins_list):

#         all_coins_indicators = None
#         signals_list = []      
#         symbols = [f"BINANCE:{x}" for x in coins_list if x]

#         all_coins_indicators = get_multiple_analysis(symbols=symbols,
#                             screener='crypto',                    
#                             interval=self.interval)

#         for _, item in all_coins_indicators.items():
#             recommendation = None
#             symbol = None
#             try:
#                 symbol = item.symbol
#                 recommendation = item.summary["RECOMMENDATION"]
#             except:
#                 continue
#             if (recommendation == 'STRONG_BUY'):
#                 signals_list.append((symbol, 1))          

#             elif (recommendation == 'STRONG_SELL'):
#                 signals_list.append((symbol, -1))             

#         return signals_list  



# def calculate_atr1(data, atr_period=14):
#     data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
#     data.dropna(inplace=True)
#     return data, data[f"ATR{atr_period}"].iloc[-1]
# def calculate_atr2(data, atr_period=14):
#     high = data['High'].values
#     low = data['Low'].values
#     close = data['Close'].values

#     tr = [0] * len(data)
#     atr = [0] * len(data)

#     tr[0] = high[0] - low[0]

#     # Calculate True Range (TR)
#     for i in range(1, len(data)):
#         tr_high_low = high[i] - low[i]
#         tr_high_close_prev = abs(high[i] - close[i - 1])
#         tr_low_close_prev = abs(low[i] - close[i - 1])
#         tr[i] = max(tr_high_low, tr_high_close_prev, tr_low_close_prev)

#     # Calculate ATR
#     atr[atr_period - 1] = sum(tr[:atr_period]) / atr_period

#     for i in range(atr_period, len(data)):
#         atr[i] = (atr[i - 1] * (atr_period - 1) + tr[i]) / atr_period

#     data_copy = data.copy()
#     data_copy[f"ATR{atr_period}"] = atr
#     data_copy.dropna(inplace=True)

#     return data_copy, atr[-1]

# # Пример использования
# indnd = INDICATORS()
# data = indnd.get_klines('BTCUSDT', '1m', 240)

# # Вызов функции calculate_atr2
# new_data1, atr_value1 = calculate_atr1(data)
# new_data2, atr_value = calculate_atr2(data)

# # Вывод результата
# # print(new_data2)
# print(f"Последнее значение ATR{14}: {atr_value1}")
# print(f"Последнее значение ATR{14}: {atr_value}")



# # indnd = INDICATORS()

# # data = indnd.get_klines('BTCUSDT', '1m', 240)
# # # new_data1 = calculate_atr1(data)
# # new_data2 = calculate_atr2(data)
# # # new_data1 = calculate_stoch_rsi_pandas_ta(data)
# # # new_data2 = calculate_stoch_rsi(data)
# # # print(new_data1)
# # print(new_data2)
