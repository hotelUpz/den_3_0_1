# # class Interval:
# #     INTERVAL_1_MINUTE = "1m"
# #     INTERVAL_5_MINUTES = "5m"
# #     INTERVAL_15_MINUTES = "15m"
# #     INTERVAL_30_MINUTES = "30m"
# #     INTERVAL_1_HOUR = "1h"
# #     INTERVAL_2_HOURS = "2h"
# #     INTERVAL_4_HOURS = "4h"
# #     INTERVAL_1_DAY = "1d"
# #     INTERVAL_1_WEEK = "1W"
# #     INTERVAL_1_MONTH = "1M"
# # from tradingview_ta import TA_Handler, Interval, Exchange
# from tradingview_ta import get_multiple_analysis
# from utils import COInN_FILTERR
# from api_binance import BINANCE_API
# from random import choice

# # def get_trading_view_signal(intervall='5m'):     
# #     coin_data = TA_Handler(
# #         symbol='fjkv',
# #         screener='crypto',
# #         exchange="BINANCE",
# #         interval=intervall
# #     )
# #     tv_answer = coin_data.get_analysis().summary
# #     recommendation = None
# #     try:
# #         recommendation = tv_answer.get("RECOMMENDATION", None)
# #         print(f"trading view recommendation: {recommendation}")
# #     except Exception as ex:
# #         pass
    
# #     if recommendation == 'STRONG_BUY':
# #         return 1
# #     elif recommendation == 'STRONG_SELL':
# #         return -1             

# #     return 0  


# def get_tv_signals(coins_list):

#     all_coins_indicators = None
#     signals_list = []      
#     symbols = [f"BINANCE:{x}" for x in coins_list if x]

#     all_coins_indicators = get_multiple_analysis(symbols=symbols,
#                         screener='crypto',                    
#                         interval="1h")

#     for _, item in all_coins_indicators.items():
#         recommendation = None
#         symbol = None
#         try:
#             symbol = item.symbol
#             recommendation = item.summary["RECOMMENDATION"]
#         except:
#             continue
#         if (recommendation == 'STRONG_BUY'):
#             signals_list.append({f"{symbol}": 1})          

#         elif (recommendation == 'STRONG_SELL'):
#             signals_list.append({f"{symbol}": -1})             

#     return signals_list 

# coin_filter = COInN_FILTERR()
# bin_api = BINANCE_API()

# random_tv_signal = choice(get_tv_signals(coin_filter.go_filter(bin_api.get_all_tickers(), coin_filter.coin_market_cup_top(100))))
# print(next(iter(random_tv_signal)))
# print(next(iter(random_tv_signal.values())))


# wait_candle_flag = True

# if wait_candle_flag:
#     wait_candle_flag = False
#     print(1)
# else:
#     print(2) 


  