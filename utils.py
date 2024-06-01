import requests
import time
from datetime import datetime as dttm, time as timm
# from random import choice
import math
import decimal
from indicator_strategy import INDICATORS_STRATEGYY

def server_to_utc_difference_counter():
    server_time_naive = dttm.now()
    # print(f"server_time_naive: {server_time_naive}")
    utc_time = dttm.utcnow()
    # print(f"utc_time: {utc_time}")
    time_difference = server_time_naive - utc_time
    total_seconds = abs(time_difference.total_seconds()) * 1000
    total_seconds = math.ceil(total_seconds)
    if total_seconds < 10:
        return 0
    return total_seconds

time_correction_val = server_to_utc_difference_counter()
# print("Разница между серверным временем в милисекундах:", time_correction_val)

class COInN_FILTERR(INDICATORS_STRATEGYY):
    def __init__(self) -> None:
        super().__init__()
        # устанавливаем функциии декораторы
        self.top_coins_engin = self.log_exceptions_decorator(self.top_coins_engin)
        self.coin_market_cup_top = self.log_exceptions_decorator(self.coin_market_cup_top)
        self.go_filter = self.log_exceptions_decorator(self.go_filter)
    
    def top_coins_engin(self, limit):
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.coinMarketCup_api_token,
        }
        params = {
            'start': '1',
            'limit': limit,
            'convert': 'USD',  
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            top_coins = data['data']
            return top_coins
        return None
    
    def coin_market_cup_top(self, limit):
        top_coins_total_list = []
        top_coins = self.top_coins_engin(limit)
        if top_coins:
            for coin in top_coins:
                try:
                    top_coins_total_list.append(f"{coin['symbol']}USDT")
                except:
                    pass
            return top_coins_total_list
        return       

    def go_filter(self, all_binance_tickers, coinsMarket_tickers):
        top_pairs = []            
        exclusion_contains_list = ['UP', 'DOWN', 'RUB', 'EUR']

        if all_binance_tickers:
            if not self.price_filter_flag:
                self.MIN_FILTER_PRICE = 0
                self.MAX_FILTER_PRICE = math.inf                   

            top_pairs = [ticker for ticker in all_binance_tickers if
                            ticker['symbol'].upper().endswith('USDT') and
                            not any(exclusion in ticker['symbol'].upper() for exclusion in exclusion_contains_list) and
                            (float(ticker['lastPrice']) >= self.MIN_FILTER_PRICE) and (
                                    float(ticker['lastPrice']) <= self.MAX_FILTER_PRICE)]
            if self.slice_volum_flag:
                top_pairs = sorted(top_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
                top_pairs = top_pairs[:self.SLICE_VOLUME_BINANCE_PAIRS]

            if self.min_volume_usdtFilter_flag:
                top_pairs = [x for x in top_pairs if float(x['quoteVolume']) >= self.MIN_VOLUM_USDT]

            if self.slice_volatilyty_flag:
                top_pairs = sorted(top_pairs, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
                top_pairs = top_pairs[:self.SLICE_VOLATILITY]
            if self.daily_filter_direction == 1:
                top_pairs = [x for x in top_pairs if float(x['priceChange']) > 0]
            elif self.daily_filter_direction == -1:
                top_pairs = [x for x in top_pairs if float(x['priceChange']) < 0]
            if self.volume_range_true:
                top_pairs = sorted(top_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
            if self.volatility_range_true:
                top_pairs = sorted(top_pairs, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
            if self.in_coinMarketCup_is:
                return [x['symbol'] for x in top_pairs if x['symbol'] not in self.black_coins_list and x['symbol'] in coinsMarket_tickers]
            return [x['symbol'] for x in top_pairs if x['symbol'] not in self.black_coins_list]

class UTILS(COInN_FILTERR):
    def __init__(self):  
        super().__init__()
        # устанавливаем функциии декораторы
        self.date_of_the_month = self.log_exceptions_decorator(self.date_of_the_month)
        self.milliseconds_to_datetime = self.log_exceptions_decorator(self.milliseconds_to_datetime)
        self.is_time_to_show_statistik = self.log_exceptions_decorator(self.is_time_to_show_statistik)
        self.time_calibrator = self.log_exceptions_decorator(self.time_calibrator)
        self.usdt_to_qnt_converter = self.log_exceptions_decorator(self.usdt_to_qnt_converter)
        self.from_anomal_view_to_normal = self.log_exceptions_decorator(self.from_anomal_view_to_normal)
    
    def date_of_the_month(self):        
        current_time = time.time()        
        datetime_object = dttm.fromtimestamp(current_time)       
        formatted_time = datetime_object.strftime('%d')
        return int(formatted_time) 
        
    def milliseconds_to_datetime(self, milliseconds):
        seconds, milliseconds = divmod(milliseconds, 1000)
        time = dttm.utcfromtimestamp(seconds)
        # milliseconds_str = str(milliseconds).zfill(3)
        # return time.strftime('%Y-%m-%d %H:%M:%S') + '.' + milliseconds_str
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def is_time_to_show_statistik(self, show_statistic_hour):
        now = dttm.now().time()    
        nine_pm = timm(show_statistic_hour, 0)
        return now >= nine_pm  
    
    def time_calibrator(self, kline_time, time_frame):
        current_time = time.time()
        time_in_seconds = 0

        if time_frame == 'm':
            time_in_seconds = kline_time * 60
        elif time_frame == 'h':
            time_in_seconds = kline_time * 3600
        elif time_frame == 'd':
            time_in_seconds = kline_time * 86400

        next_interval = math.ceil(current_time / time_in_seconds) * time_in_seconds
        wait_time = next_interval - current_time
        return int(wait_time)    
    
    def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
        # print(symbol_data)
        # //////////////////////
        quantity_precision = int(float(symbol_data['quantityPrecision']))
        price_precision = int(float(symbol_data['pricePrecision']))
        # print(f"quantity_precision: {quantity_precision}")
        min_notional = int(float(next((f['notional'] for f in symbol_data['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 0)))
        if depo <= min_notional:
            depo = min_notional
        if (quantity_precision == 0 and (depo / cur_price) < 1) or depo < 5:
            return "Too_litle_size", None            
        return round(depo / cur_price, quantity_precision), price_precision    
    
    def from_anomal_view_to_normal(self, strange_list):
        normal_list = [] 
        # /////////////////////////////////////////////////////
        for x in strange_list:
            x_f = decimal.Decimal(str(x))
            normal_list.append(format(x_f, 'f'))        
        normal_view = ', '.join(normal_list)
        self.handle_messagee(normal_view)