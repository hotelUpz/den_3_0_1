import pandas_ta as ta
from tradingview_ta import TA_Handler, Interval, Exchange
from random import choice
from api_binance import BINANCE_API

class INDICATORS(BINANCE_API):
    def __init__(self) -> None:
        super().__init__()  
        # устанавливаем функциии декораторы
        self.calculate_ema = self.log_exceptions_decorator(self.calculate_ema)
        self.calculate_stoch_rsi = self.log_exceptions_decorator(self.calculate_stoch_rsi)
        self.calculate_atr = self.log_exceptions_decorator(self.calculate_atr)

    def indicators_documentation(self):
        """
            # номера стратегии индикаторов:
            # 1 -- 'ema_crossover': классическая стратегия прересечения двух ema (кроссовер)
            # 2 -- 'ema_crossover + trend_line': кроссовер ema плюс ориентироваться на линию тренда ema. Период равен ema_trend_line (сейчас 240). (Смотри в настройках программы)
            # 3 -- 'ema_crossover + stoch_rsi_crossover': ema кроссовер плюс кроссовер стохастик-рси
            # 4 -- 'ema_crossover + stoch_rsi_overTrade': ema кроссовер плюс овертрейд стохастик-рси
            # 5 -- 'ema_crossover + stoch_rsi_overTrade + trend_line': то же что и предыдущий, но плюс ориентрироваться на линию тренда
            # 6 - 'smart_random + trend_line' # рандомный выбор сигнала c ориентацией на тренд. Рекомендуется использовать только для тестов
        """
    # pandas_ta library: .......................................  
     
    def calculate_ema(self, data, ema1_period, ema2_period, ema3_period):
        data[f"EMA{ema1_period}"] = ta.ema(data['Close'], length=ema1_period)
        data[f"EMA{ema2_period}"] = ta.ema(data['Close'], length=ema2_period)
        data[f"EMA{ema3_period}"] = ta.ema(data['Close'], length=ema3_period) 
        data.dropna(inplace=True)
        return data
    
    def calculate_stoch_rsi(self, data):
        stoch_rsi = ta.stochrsi(data['Close'], length=14, rsi_length=14, k=3, d=3)
        data['StochRSI_%K'] = stoch_rsi['STOCHRSIk_14_14_3_3']
        data['StochRSI_%D'] = stoch_rsi['STOCHRSId_14_14_3_3']
        data.dropna(inplace=True)
        return data    
    
    def calculate_atr(self, data, atr_period):
        data[f"ATR{atr_period}"] = ta.atr(data['High'], data['Low'], data['Close'], length=atr_period)
        data.dropna(inplace=True)
        return data, data[f"ATR{atr_period}"].iloc[-1]
    
    # /////// trading view indicator:
    def get_trading_view_signal(self):     
        coin_data = TA_Handler(
            symbol=self.symbol.upper(),
            screener='crypto',
            exchange="BINANCE",
            interval=self.interval
        )
        tv_answer = coin_data.get_analysis().summary
        recommendation = None
        try:
            recommendation = tv_answer.get("RECOMMENDATION", None)
            print(f"trading view recommendation: {recommendation}")
        except Exception as ex:
            pass
        
        if recommendation == 'STRONG_BUY':
            return 1
        elif recommendation == 'STRONG_SELL':
            return -1             

        return 0    

class INDICATORS_STRATEGYY(INDICATORS):
    def __init__(self) -> None:
        super().__init__()
        # устанавливаем функциии декораторы
        self.get_signals = self.log_exceptions_decorator(self.get_signals)
     
    def get_signals(self, strategy_list, df, ema1_period, ema2_period, ema3_period, stoch_rsi_over_sell, stoch_rsi_over_buy): 
  
        df = self.calculate_ema(df, ema1_period, ema2_period, ema3_period)
        df = self.calculate_stoch_rsi(df)
        signals_assum = 0
        long_trend = False
        short_trend = False

        if 'ema_crossover' in strategy_list:
            if (df[f"EMA{ema1_period}"].iloc[-1] > df[f"EMA{ema2_period}"].iloc[-1]) and (df[f"EMA{ema1_period}"].iloc[-2] < df[f"EMA{ema2_period}"].iloc[-2]):
                signals_assum += 1         
                 
            if (df[f"EMA{ema1_period}"].iloc[-1] < df[f"EMA{ema2_period}"].iloc[-1]) and (df[f"EMA{ema1_period}"].iloc[-2] > df[f"EMA{ema2_period}"].iloc[-2]):
                signals_assum -= 1

        if 'trend_line' in strategy_list:
            if df[f"EMA{ema2_period}"].iloc[-1] > df[f"EMA{ema3_period}"].iloc[-1]:
                long_trend = True
                signals_assum += 1         
                
            if df[f"EMA{ema2_period}"].iloc[-1] < df[f"EMA{ema3_period}"].iloc[-1]:
                short_trend = True
                signals_assum -= 1

        if 'smart_random' in strategy_list:
            if long_trend:
                random_list = [1,2,3,4,5,6,1,3,5,7,8,9,10]
            elif short_trend:
                random_list = [1,2,3,4,5,2,4,6,6,7,8,9,10]
            if long_trend or short_trend:
                if choice(random_list) % 2 != 0:
                    return "LONG_SIGNAL"
                else:
                    return "SHORT_SIGNAL"
            return
            
        if 'stoch_rsi_crossover' in strategy_list:
            for i in range(1, 4):
                if (df['StochRSI_%K'].iloc[-1] > df['StochRSI_%D'].iloc[-1] and 
                    df['StochRSI_%K'].iloc[-(i+1)] < df['StochRSI_%D'].iloc[-(i+1)]):
                    signals_assum += 1
                    break
                if (df['StochRSI_%K'].iloc[-1] < df['StochRSI_%D'].iloc[-1] and 
                    df['StochRSI_%K'].iloc[-(i+1)] > df['StochRSI_%D'].iloc[-(i+1)]):
                    signals_assum -= 1
                    break

        if 'stoch_rsi_overTrade' in strategy_list:
            if df['StochRSI_%K'].iloc[-1] < stoch_rsi_over_sell and df['StochRSI_%D'].iloc[-1] < stoch_rsi_over_sell:
                signals_assum += 1
            if df['StochRSI_%K'].iloc[-1] > stoch_rsi_over_buy and (df['StochRSI_%D'].iloc[-1] > stoch_rsi_over_buy):
                signals_assum -= 1

        if 'trading_view_ind':
            if self.get_trading_view_signal == 1:
                signals_assum += 1
            elif self.get_trading_view_signal == -1:
                signals_assum -= 1
            
        if signals_assum > 0 and signals_assum == len(strategy_list):
            return "LONG_SIGNAL"
        elif signals_assum < 0 and abs(signals_assum) == len(strategy_list):
            return "SHORT_SIGNAL"               

        return