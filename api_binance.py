from log import Total_Logger
import time
from time import sleep
import pandas as pd
import hmac
import hashlib
import requests

class BINANCE_API(Total_Logger):
    def __init__(self) -> None:
        super().__init__() 
        self.market_place = 'binance' # ...
        self.market_type = 'futures' # ...
        # /////////////////////////////////////////
        # //////////урлы api бинанс: ///////////////////////
        self.create_order_url = self.cancel_order_url = 'https://fapi.binance.com/fapi/v1/order'
        self.exchangeInfo_url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        self.klines_url = 'https://fapi.binance.com/fapi/v1/klines' 
        self.set_margin_type_url = 'https://fapi.binance.com/fapi/v1/marginType'
        self.set_leverage_url = 'https://fapi.binance.com/fapi/v1/leverage'
        self.positions_url = 'https://fapi.binance.com/fapi/v2/positionRisk'
        self.all_tikers_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        self.get_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOrders'
        self.cancel_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOpenOrders'                
        self.balance_url = 'https://fapi.binance.com/fapi/v2/balance'
        # self.current_price_url = "https://fapi.binance.com/fapi/v1/ticker/price"
        # self.get_all_open_orders_url = 'https://fapi.binance.com/fapi/v1/openOrders'
        # self.account_url = 'https://fapi.binance.com/fapi/v2/account'
        # print(BINANCE_API_PUBLIC_KEY)
        self.headers = {
            'X-MBX-APIKEY': self.api_key
        }

        # proxy_soks5_url = f'soks5://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_socks5_port}'
        # self.proxiess = {
        #     "socks5": proxy_soks5_url
        # }

        self.proxy_url = f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
        self.proxiess = {
            'http': self.proxy_url,
            # 'https': self.proxy_url
        }
        # устанавливаем функциии декораторы
        self.get_signature = self.log_exceptions_decorator(self.get_signature)
        self.HTTP_request = self.log_exceptions_decorator(self.HTTP_request)
        self.get_excangeInfo = self.log_exceptions_decorator(self.get_excangeInfo)
        self.get_all_tickers = self.log_exceptions_decorator(self.get_all_tickers)
        self.get_total_balance = self.log_exceptions_decorator(self.get_total_balance)
        self.get_all_orders = self.log_exceptions_decorator(self.get_all_orders)
        self.get_klines = self.log_exceptions_decorator(self.get_klines)
        self.is_closing_position_true = self.log_exceptions_decorator(self.is_closing_position_true)
        self.set_margin_type = self.log_exceptions_decorator(self.set_margin_type)
        self.set_leverage = self.log_exceptions_decorator(self.set_leverage)
        self.make_order = self.log_exceptions_decorator(self.make_order)
        # self.tralling_stop_order = self.log_exceptions_decorator(self.tralling_stop_order)
        self.cancel_secondary_open_orders = self.log_exceptions_decorator(self.cancel_secondary_open_orders)
        self.cancel_order_by_id = self.log_exceptions_decorator(self.cancel_order_by_id)

    def get_signature(self, params):
        params['timestamp'] = int(time.time() *1000)
        params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
        hash = hmac.new(bytes(self.api_secret, 'utf-8'), params_str.encode('utf-8'), hashlib.sha256)        
        params['signature'] = hash.hexdigest()
        return params
    
    def HTTP_request(self, target, url, **kwargs):
        response = None
        multiplier = 2

        for i in range(2):
            try:
                if not self.is_proxies_true:
                    kwargs.pop('proxies', None)

                response = requests.request(url=url, **kwargs)
                # print(f"binance: {response}")
                # print(response.json())
                if response is not None:
                    if target == 'place_order':
                        if response.status_code != 200:
                            self.handle_exception(f"Ошибка запроса при попытке создания ордера. Файл api_binance.py: {response.status_code}\nТекст ошибки:\n{response.json()}")                      
                            sleep((i+1) * multiplier)
                            continue
                    return response.json()
                continue
            except Exception as ex:
                self.handle_exception(f"Файл api_binance.py: {ex}") 
                sleep((i+1) * multiplier)

        return None    

# ////////////////////////////////////////get api:   
    def get_excangeInfo(self):   
        params = {
            'recvWindow': 20000
        }  
        return self.HTTP_request('other', self.exchangeInfo_url, method='GET', headers=self.headers, params=params, proxies=self.proxiess)    
   
    def get_all_tickers(self): 
        params = {
            'recvWindow': 20000
        }       
        return self.HTTP_request('other', self.all_tikers_url, method='GET', headers=self.headers, params=params, proxies=self.proxiess)
   
    def get_total_balance(self, ticker):
        params = {}
        params['recvWindow'] = 20000
        params = self.get_signature(params)
        current_balance = self.HTTP_request('other', self.balance_url, method='GET', headers=self.headers, params=params, proxies=self.proxiess)
        return float([x['balance'] for x in current_balance if x['asset'] == ticker][0])
   
    def get_all_orders(self, symbol):
        params = {
            'symbol': symbol,
            'recvWindow': 20000
            # 'limit': limit
        }
        params = self.get_signature(params)
        resp = self.HTTP_request('other', self.get_all_orders_url, method='GET', headers=self.headers, params=params, proxies=self.proxiess)
        # print(resp)
        return resp
       
    def get_klines(self, symbol, interval, periodd):
        klines = None       
        params = {}
        params["symbol"] = symbol
        params['recvWindow'] = 20000
        params["interval"] = interval
        params["limit"] = int(periodd*2.1)
        params = self.get_signature(params)
        klines = self.HTTP_request('other', self.klines_url, method='GET', headers=self.headers, params=params, proxies=self.proxiess)
        if klines:
            data = pd.DataFrame(klines).iloc[:, :6]
            data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
            data = data.set_index('Time')
            data.index = pd.to_datetime(data.index, unit='ms')
            return data.astype(float)        
        return
       
    def is_closing_position_true(self, symbol):
        positions = None
        params = {
            "symbol": symbol,
            'recvWindow': 20000
        }
        params = self.get_signature(params)
        positions = requests.get(
            self.positions_url, 
            headers=self.headers, 
            params=params, 
            proxies=self.proxiess if self.is_proxies_true else None
        )
        if positions.status_code == 200:
            positions = positions.json()                        
            for position in positions:
                if position['symbol'] == symbol and float(position['positionAmt']) != 0:
                    #  and position['orderId'] == self.order_id:
                    return   
            return True        
        return
    
# ///////////////////////////////////////////// post api:   
    def set_margin_type(self, symbol, margin_type):                
        params = {}
        params['symbol'] = symbol
        params['margintype'] =  margin_type
        params['recvWindow'] = 20000
        params['newClientOrderId'] = 'CHANGE_MARGIN_TYPE'       
        params = self.get_signature(params)
        return self.HTTP_request('other', self.set_margin_type_url, method='POST', headers=self.headers, params=params, proxies=self.proxiess)        
   
    def set_leverage(self, symbol, lev_size):                     
        params = {}
        params['symbol'] = symbol
        params['recvWindow'] = 20000
        params['leverage'] = lev_size
        params = self.get_signature(params)
        # print(params)
        return self.HTTP_request('other', self.set_leverage_url, method='POST', headers=self.headers, params=params, proxies=self.proxiess)
   
    def make_order(self, symbol, qty, side, market_type, target_price): 
        # print(symbol, qty, side, market_type, target_price)
        params = {}        
        params["symbol"] = symbol        
        params["type"] = market_type
        params["quantity"] = qty
        params['recvWindow'] = 20000
        if market_type == 'STOP_MARKET' or market_type == 'TAKE_PROFIT_MARKET':
            params['stopPrice'] = target_price
            params['closePosition'] = True
        if market_type == 'LIMIT':            
            params["price"] = target_price
            params["timeinForce"] = 'GTC' 
        params["side"] = side
        params['newOrderRespType'] = 'RESULT' # default 'ASK'
        params = self.get_signature(params)
        resp = self.HTTP_request('place_order', self.create_order_url, method='POST', headers=self.headers, params=params, proxies=self.proxiess)
        # print(resp)
        return resp

# //////////////////////////////////// delete api:
    def cancel_order_by_id(self, symbol, orderId):
        # print(symbol, orderId)
        params = {
            'symbol': symbol,
            'orderId': orderId,
            'recvWindow': 20000,
            'timestamp': int(time.time() * 1000)
        }

        params = self.get_signature(params)
        resp = self.HTTP_request('other', self.cancel_order_url, method='DELETE', headers=self.headers, params=params, proxies=self.proxiess)
        return resp 
    
    def cancel_secondary_open_orders(self, symbol):
        id_list = [self.sl_order_id, self.tp_order_id]
        # print(f"id_list: {id_list}")
        for orderId in id_list:
            if orderId is not None:
                try:
                    resp = self.cancel_order_by_id(symbol, orderId)
                except Exception as ex:
                    pass
                # print(resp)
        return
    
# ba = BINANCE_API()
# kl = ba.get_klines('BTCUSDT', '1m', 240)
# print(kl)