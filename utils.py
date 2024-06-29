import requests
import time
from datetime import datetime as dttm, time as timm, timedelta as tmdl
# import pytz
# from random import choice
import math
import decimal
from indicator_strategy import INDICATORS_STRATEGYY

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
        # print(self.proxiess)
        response = requests.get(url, headers=headers, params=params, proxies=self.proxiess if self.is_proxies_true else None)
        # response = self.session.get(url, headers=headers, params=params)
        # print(f"coin_market_cup: {response}")
        # print(response.json())
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
        top_pairs_total = []  
        top_pairs_by_volum = []
        top_pairs_by_positive_price = []  
        top_pairs_by_negative_price = []       
        exclusion_contains_list = ['UP', 'DOWN', 'RUB', 'EUR']
        exclusion_contains_list += self.black_coins_list

        if all_binance_tickers:
            if not self.price_filter_flag:
                self.MIN_FILTER_PRICE = 0
                self.MAX_FILTER_PRICE = math.inf                   

            def is_valid_ticker(ticker, exclusion_contains_list, min_price, max_price, black_coins_list, coinsMarket_tickers, in_coinMarketCup_is):
                symbol = ticker['symbol'].upper()
                last_price = float(ticker['lastPrice'])
                
                common_conditions = (
                    symbol.endswith('USDT') and
                    all(exclusion not in symbol for exclusion in exclusion_contains_list) and
                    min_price <= last_price <= max_price
                )
                
                if in_coinMarketCup_is:
                    return common_conditions and symbol in coinsMarket_tickers
                else:
                    return common_conditions

            top_pairs_total = [
                ticker for ticker in all_binance_tickers
                if is_valid_ticker(
                    ticker, 
                    exclusion_contains_list, 
                    self.MIN_FILTER_PRICE, 
                    self.MAX_FILTER_PRICE, 
                    self.black_coins_list, 
                    coinsMarket_tickers, 
                    self.in_coinMarketCup_is
                )
            ]

            if self.slice_volum_flag:
                top_pairs_total = top_pairs_by_volum = sorted(top_pairs_total, key=lambda x: float(x['quoteVolume']), reverse=True)
                top_pairs_total = top_pairs_by_volum = top_pairs_total[:self.SLICE_VOLUME_BINANCE_PAIRS]

            if self.min_volume_usdtFilter_flag:
                top_pairs_total = top_pairs_by_volum = [x for x in top_pairs_total if float(x['quoteVolume']) >= self.MIN_VOLUM_USDT]

            if self.slice_volatilyty_flag:
                top_pairs_total = sorted(top_pairs_total, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
                top_pairs_total = top_pairs_total[:self.SLICE_VOLATILITY]

            top_pairs_by_positive_price = [x for x in top_pairs_total if float(x['priceChange']) > 0]
            top_pairs_by_negative_price = [x for x in top_pairs_total if float(x['priceChange']) < 0]

            if self.daily_filter_direction == 1 and not self.defend_total_market_trend_flag:
                top_pairs_total = top_pairs_by_positive_price
            elif self.daily_filter_direction == -1 and not self.defend_total_market_trend_flag:
                top_pairs_total = top_pairs_by_negative_price 
            else:
                top_pairs_total = top_pairs_by_positive_price + top_pairs_by_negative_price

            if self.volume_range_true:
                top_pairs_total = sorted(top_pairs_total, key=lambda x: float(x['quoteVolume']), reverse=True)
            if self.volatility_range_true:
                top_pairs_total = sorted(top_pairs_total, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
            top_pairs_total = [x['symbol'] for x in top_pairs_total]
            top_pairs_by_volum = [x['symbol'] for x in top_pairs_by_volum]
            top_pairs_by_positive_price = [x['symbol'] for x in top_pairs_by_positive_price]
            top_pairs_by_negative_price = [x['symbol'] for x in top_pairs_by_negative_price]
            return top_pairs_total, top_pairs_by_volum, top_pairs_by_positive_price, top_pairs_by_negative_price

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

    def count_decimal_places(self, number):
        if isinstance(number, (int, float)):
            # Преобразуем число в строку
            number_str = f'{number:.10f}'.rstrip('0')
            # Проверяем наличие десятичной точки
            if '.' in number_str:
                # Возвращаем количество знаков после запятой
                return len(number_str.split('.')[1])
        return 0  

    def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
        if not symbol_data:
            return "Symbol not found", None, None

        quantity_precision = int(float(symbol_data['quantityPrecision']))
        price_precision_market = int(float(symbol_data['pricePrecision']))

        price_precision_limit = price_precision_market 
        for filter_data in symbol_data['filters']:
            if filter_data['filterType'] == 'PRICE_FILTER':
                price_precision_limit = float(filter_data.get('tickSize', 1.0))
                price_precision_limit = self.count_decimal_places(price_precision_limit)

        min_notional = float(next((f['notional'] for f in symbol_data['filters'] if f['filterType'] == 'MIN_NOTIONAL'), 0))
        if depo <= min_notional:
            depo = min_notional

        if (quantity_precision == 0 and (depo / cur_price) < 1) or depo < 5:
            return "Too_little_size", None, None

        quantity = round(depo / cur_price, quantity_precision)
        return quantity, price_precision_market, price_precision_limit
    
    def from_anomal_view_to_normal(self, strange_list):
        normal_list = [] 
        # /////////////////////////////////////////////////////
        for x in strange_list:
            x_f = decimal.Decimal(str(x))
            normal_list.append(format(x_f, 'f'))        
        normal_view = ', '.join(normal_list)
        self.handle_messagee(normal_view)

    # # /////////////////////////////////////////////////////////////
    def get_next_show_statistic_time(self):
        current_time = dttm.now(self.local_tz)
        target_time = current_time.replace(hour=self.show_statistic_hour, minute=0, second=0)
        if current_time >= target_time:            
            target_time += tmdl(days=1)        
        return target_time
    
    def show_statistic_signal(self, target_time): 
        now_time = dttm.now(self.local_tz)
        if now_time >= target_time:
            target_time = self.get_next_show_statistic_time()             
            return True, target_time          
        return False, target_time
    
# u = UTILS()
# symbol_info = u.get_excangeInfo()
# cur_price = u.get_klines('LDOUSDT', u.interval, 2).get("Close", None).iloc[-1]
# print(cur_price)
# symbol, depo = 'LDOUSDT', 10, 
# print(u.usdt_to_qnt_converter(symbol, depo, symbol_info, cur_price))