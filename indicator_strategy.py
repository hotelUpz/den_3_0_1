import pandas_ta as ta
from tradingview_ta import get_multiple_analysis
from random import choice
from api_binance import BINANCE_API
import time

class INDICATORS(BINANCE_API):
    def __init__(self) -> None:
        super().__init__()  
        # устанавливаем функциии декораторы
        self.calculate_ema = self.log_exceptions_decorator(self.calculate_ema)
        self.calculate_atr = self.log_exceptions_decorator(self.calculate_atr)

    def indicators_documentation(self):
        """
            # номера стратегии индикаторов:
            '1': 'trading_view_ind' -- индикатор библиотеки трейдинг вью
            '2': 'trading_view_ind + trend_line' -- индикатор библиотеки трейдинг вью + трендовая линия
        """
    # pandas_ta library: .......................................  
     
    def calculate_ema(self, data, ema1_period, ema2_period):
        data[f"EMA{ema1_period}"] = ta.ema(data['Close'], length=ema1_period)
        data[f"EMA{ema2_period}"] = ta.ema(data['Close'], length=ema2_period) 
        data.dropna(inplace=True)
        return data
    
    def calculate_atr(self, data, atr_period):
        data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
        data.dropna(inplace=True)
        return data, data[f"ATR{atr_period}"].iloc[-1]
    
    # /////// trading view indicator:
    def get_tv_signals(self, coins_list):

        all_coins_indicators = None
        signals_list = []      
        symbols = [f"BINANCE:{x}" for x in coins_list if x]

        all_coins_indicators = get_multiple_analysis(symbols=symbols,
                            screener='crypto',                    
                            interval=self.interval)

        for _, item in all_coins_indicators.items():
            recommendation = None
            symbol = None
            try:
                symbol = item.symbol
                recommendation = item.summary["RECOMMENDATION"]
            except:
                continue
            if (recommendation == 'STRONG_BUY'):
                signals_list.append((symbol, "LONG_SIGNAL"))          

            elif (recommendation == 'STRONG_SELL'):
                signals_list.append((symbol, "SHORT_SIGNAL"))             

        return signals_list    

class INDICATORS_STRATEGYY(INDICATORS):
    def __init__(self) -> None:
        super().__init__()
        # устанавливаем функциии декораторы
        self.get_signals = self.log_exceptions_decorator(self.get_signals)
     
    def get_signals(self, strategy_list, coins_list, ema1_period, ema2_period):
            symbol = None
            cur_price = None
                    
            get_tv_signals_list = self.get_tv_signals(coins_list)
            if get_tv_signals_list:             

                if not 'trend_line' in strategy_list:
                    random_tv_signal = choice(get_tv_signals_list)
                    symbol = random_tv_signal[0]
                    cur_signal = random_tv_signal[1]
                    df = self.get_klines(symbol, self.interval, ema2_period)
                    cur_price = df['Close'].iloc[-1]
                    return symbol, cur_signal, cur_price, df
                           
                for symbol, cur_signal in get_tv_signals_list:
                    df = self.get_klines(symbol, self.interval, ema2_period)
                    df = self.calculate_ema(df, ema1_period, ema2_period)
                    if cur_signal == "LONG_SIGNAL":
                        if df[f"EMA{ema1_period}"].iloc[-1] > df[f"EMA{ema2_period}"].iloc[-1]:
                            cur_price = df['Close'].iloc[-1]
                            return symbol, "LONG_SIGNAL", cur_price, df 
                    elif cur_signal == "SHORT_SIGNAL":   
                        if df[f"EMA{ema1_period}"].iloc[-1] < df[f"EMA{ema2_period}"].iloc[-1]:
                            cur_price = df['Close'].iloc[-1]
                            return symbol, "SHORT_SIGNAL", cur_price, df
                    time.sleep(0.1)
            return None, None, None, None