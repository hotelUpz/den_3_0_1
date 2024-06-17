# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from api_binance import BINANCE_API


# # def calculate_vpvr(data, min_bins=10, max_bins=50):
# #     # Вычисляем динамическое количество корзин (bins) на основе количества свечей
# #     num_candles = 240
# #     bins = min(max(min_bins, num_candles // 10), max_bins)
# #     data = data.tail(240)
# #     # print(data)        
# #     # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
# #     price_range = pd.cut(data['Close'], bins=bins)
# #     vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
# #     return vpvr

# # def find_vpvr_levels(vpvr, num_levels=2):
# #     # Поиск наиболее объемных зон VPVR
# #     top_vpvr_indexes = vpvr.nlargest(num_levels).index
# #     vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
# #     return vpvr_levels

# # def immediate_vpvr_level_defender(cur_price, vpvr_levels):
# #     disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
# #                 (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
# #     if not disposition:
# #         immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
# #         strongest_volum_level = [0, 0]

# #         for _, _, m, v in vpvr_levels:
# #             cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
# #             if cur_volum_level > strongest_volum_level[0]:
# #                 strongest_volum_level = [cur_volum_level, m]                                

# #         if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
# #             return "L", immediate_level
# #         elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
# #             return "S", immediate_level
# #         elif strongest_volum_level[1] > cur_price:
# #             return "L", strongest_volum_level[1]
# #         elif strongest_volum_level[1] < cur_price:
# #             return "L", strongest_volum_level[1]

# #     return

# # def plot_vpvr(vpvr):
# #     plt.barh(vpvr.index.astype(str), vpvr.values, height=0.5)
# #     plt.ylabel('Price Range')
# #     plt.xlabel('Volume')
# #     plt.title('Volume Profile Visible Range (VPVR)')
# #     plt.show()

# # df = BINANCE_API().get_klines('BTCUSDT', '5m', 20)
# # vpvr = calculate_vpvr(df)
# # cur_price = df["Close"].iloc[-1]
# # print(f"cur_price: {cur_price}")

# # immediate_vpvr_level_defender_val = None
# # vpvr = calculate_vpvr(df)                       
# # vpvr_levels = find_vpvr_levels(vpvr)
# # immediate_vpvr_level_defender_val = immediate_vpvr_level_defender(cur_price, vpvr_levels)

# # if immediate_vpvr_level_defender_val:
# #     if immediate_vpvr_level_defender_val[0] == 'L':
# #         print("vpr indicator: Long")
# #     elif immediate_vpvr_level_defender_val[0] == 'S':
# #         print("vpr indicator: Short")
# #     print(f"level: {immediate_vpvr_level_defender_val[1]}")

# # plot_vpvr(vpvr)

    
# #     # def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
# #     #     symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
# #     #     # print(symbol_data)
# #     #     # //////////////////////
# #     #     quantity_precision = int(float(symbol_data['quantityPrecision']))
# #     #     price_precision = int(float(symbol_data['pricePrecision']))
# #     #     # print(f"quantity_precision: {quantity_precision}")
# #     #     min_notional = int(float(next((f['notional'] for f in symbol_data['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 0)))
# #     #     if depo <= min_notional:
# #     #         depo = min_notional
# #     #     if (quantity_precision == 0 and (depo / cur_price) < 1) or depo < 5:
# #     #         return "Too_litle_size", None            
# #     #     return round(depo / cur_price, quantity_precision), price_precision 


# # def count_decimal_places(number):
# #     if isinstance(number, (int, float)):
# #         # Преобразуем число в строку
# #         number_str = f'{number:.10f}'.rstrip('0')
# #         # Проверяем наличие десятичной точки
# #         if '.' in number_str:
# #             # Возвращаем количество знаков после запятой
# #             return len(number_str.split('.')[1])
# #     return 0

# # import math
# # str_number = '1.00105'
# # float_number = float(str_number)
# # price_precision_limit = count_decimal_places(float_number)
# # print(price_precision_limit)

# import aiohttp
# import asyncio
# import random
# import json
# from aiohttp_socks import ProxyConnector
# from api_binance import BINANCE_API

# class WEbss(BINANCE_API):
#     def __init__(self):  
#         super().__init__()

#     def trailing_tp_sl_shell(self):
#         async def stop_logic_price_monitoring():
#             # print(qty, enter_price, stop_loss_ratio, price_precession, last_signal_val, sl_risk_reward_multiplier, sl_order_id)
#             symbol = 'BTCUSDT'
#             # /////////////////////////////////////  
#             url = 'wss://stream.binance.com:9443/ws/'
#             # /////////////////////////////////////
#             max_retries = 10
#             retry_delay = 1  # seconds
#             retries = 0
#             # /////////////////////////////////////

#             while retries < max_retries:            
#                 try:
#                     if self.is_proxies_true:
#                         connector = ProxyConnector.from_url(f'socks5://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_socks5_port}')
#                     async with aiohttp.ClientSession(connector=connector if self.is_proxies_true else None) as session:

#                         async with session.ws_connect(url + f"{symbol}@kline_1s") as ws:
#                             subscribe_request = {
#                                 "method": "SUBSCRIBE",
#                                 "params": [f"{symbol.lower()}@kline_1s"],
#                                 "id": random.randrange(11,111111)
#                             }
#                             # print('Stop_logic_price_monitoring start processing!')                       
#                             try:
#                                 await ws.send_json(subscribe_request)
#                             except:
#                                 pass

#                             async for msg in ws:
#                                 if msg.type == aiohttp.WSMsgType.TEXT:
#                                     try:
#                                         data = json.loads(msg.data)
#                                         kline_websocket_data = data.get('k', {})
#                                         if kline_websocket_data:
#                                             try:
#                                                 cur_price = float(kline_websocket_data.get('c'))
#                                                 print(f"last_close_price: {cur_price}")                              
                                
#                                             except Exception as ex:
#                                                 # print(ex)
#                                                 pass
                                            
#                                     except Exception as ex:
#                                         continue

#                 except Exception as ex:
#                     print(f"An error occurred: {ex}")
#                     retries += 1
#                     await asyncio.sleep(retry_delay * (2 ** retries))  # Exponential backoff
#             return
        
#         asyncio.run(stop_logic_price_monitoring())

# WEbss().trailing_tp_sl_shell()
