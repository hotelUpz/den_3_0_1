# from api_binance import BINANCE_API
# import pandas as pd

# def calculate_vpvr(data, min_bins=10, max_bins=50):
#     # Вычисляем динамическое количество корзин (bins) на основе количества свечей
#     num_candles = 240
#     bins = min(max(min_bins, num_candles // 10), max_bins)
#     data = data.tail(240)
#     # print(data)        
#     # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
#     price_range = pd.cut(data['Close'], bins=bins)
#     vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
#     return vpvr

# def find_vpvr_levels(vpvr, num_levels=2):
#     # Поиск наиболее объемных зон VPVR
#     top_vpvr_indexes = vpvr.nlargest(num_levels).index
#     vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
#     return vpvr_levels

# def immediate_vpvr_level_defender(cur_price, vpvr_levels):
#     disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
#                 (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
#     if not disposition:
#         immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
#         strongest_volum_level = [0, 0]

#         for _, _, m, v in vpvr_levels:
#             cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
#             if cur_volum_level > strongest_volum_level[0]:
#                 strongest_volum_level = [cur_volum_level, m]                                

#         if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
#             return "L", immediate_level
#         elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
#             return "S", immediate_level
#         elif strongest_volum_level[1] > cur_price:
#             return "L", strongest_volum_level[1]
#         elif strongest_volum_level[1] < cur_price:
#             return "S", strongest_volum_level[1]

#     return

# ba = BINANCE_API()
# klines = ba.get_klines("BTCUSDT", '4h', 240)
# cur_price = klines["Close"].iloc[-1]
# vpvr = calculate_vpvr(klines)
# print(cur_price)
# # print(vpvr)
# vpvr_levels = find_vpvr_levels(vpvr)
# # print(levels)
# desigion = immediate_vpvr_level_defender(cur_price, vpvr_levels)
# print(desigion)

# # vpvr_levels = [(7, 50000), (2, 50000)]
# # cur_price  = 5
# # strongest_volum_level = [0, 0]

# # for i, (m, v) in enumerate(vpvr_levels):
# #     cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
# #     if cur_volum_level > strongest_volum_level[0]:
# #         strongest_volum_level = [cur_volum_level, m]

# # print(strongest_volum_level)