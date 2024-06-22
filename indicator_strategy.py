import pandas as pd
# import pandas_ta as ta
from tradingview_ta import get_multiple_analysis
from random import choice
from api_binance import BINANCE_API
import time
import os
import inspect
current_file = os.path.basename(__file__)

class INDICATORS(BINANCE_API):
    def __init__(self) -> None:
        super().__init__()  
        # устанавливаем функциии декораторы
        self.calculate_ema = self.log_exceptions_decorator(self.calculate_ema)
        self.calculate_atr = self.log_exceptions_decorator(self.calculate_atr)

    def indicators_documentation(self):
        """
            # номера стратегии индикаторов:
            #////////// СТРАТЕГИИ EMA:
                            # (классические)
            # 1 -- 'ema_crossover': классическая стратегия прересечения двух ema (кроссовер)
            # 2 -- 'ema_crossover + trend_line': кроссовер ema плюс ориентироваться на линию тренда ema. Период равен ema_trend_line
            # 3 -- 'ema_crossover + anty_trend_line': кроссовер ema плюс ориентироваться на анти трендовую линию
            # 4 -- 'ema_crossover + stoch_rsi_crossover': ema кроссовер плюс кроссовер стохастик_рси
            # 5 -- 'ema_crossover + stoch_rsi_crossover + trend_line': ema кроссовер плюс кроссовер стохастик_рси плюс линия тренда
            # 6 -- 'ema_crossover + stoch_rsi_overTrade':  ema кроссовер плюс кроссовер стохастик_рси
            # 7 -- 'ema_crossover + stoch_rsi_overTrade + trend_line': то же что и предыдущий, плюс ориентрироваться на линию тренда

                            # (эксперементальные)
            # 8 -- 'ema_crossover + simple_random': : кроссовер ema как тригер но выбор сигнала рандомный. Вероятность выбора 1:1
            # 9 -- 'ema_crossover + trande_shift_random': кроссовер ema как тригер но выбор сигнала рандомный со смещением вероятности в сторону тренда. Вероятность выбора 1:1.6
            # 10 -- 'ema_crossover + long_shift_random': кроссовер ema как тригер но выбор сигнала рандомный со смещением вероятности в лонговую сторону. Вероятность выбора 1:1.6. Можно попробовать с настройкой фильтра self.daily_filter_direction = 1, то есть на бычьем рынке
            # 11 -- 'ema_crossover + short_shift_random': кроссовер ema как тригер но выбор сигнала рандомный со смещением вероятности в шортовую сторону. Вероятность выбора 1:1.6. Можно попробовать с настройкой фильтра self.daily_filter_direction = -1, то есть на медвежьем рынке

                            # (инновационные)
            # 12 - 'ema_crossover + vpvr_level' # кроссовер ema плюс + vpvr индикатор

            # //////// СТРАТЕГИИ ТРЕЙДИНГ-ВЬЮ индикатора:
            # 13 - 'trading_view_ind' # индикатор трейдинг вью
            # 14 - 'trading_view_ind + trend_line' # индикатор трейдинг вью + ориентироваться на линию тренда
            # 15 - 'trading_view_ind + anti_trend_line' # индикатор трейдинг вью + ориентироваться на анти трендовую линию
            # 16 -- 'trading_view_ind + simple_random': : индикатор трейдинг вью как тригер но выбор сигнала рандомный. Вероятность выбора 1:1
            # 17 -- 'trading_view_ind + trande_shift_random': индикатор трейдинг вью как тригер но выбор сигнала рандомный со смещением вероятности в сторону тренда. Вероятность выбора 1:1.6
            # 18 -- 'trading_view_ind + long_shift_random': индикатор трейдинг вью как тригер но выбор сигнала рандомный со смещением вероятности в лонговую сторону. Вероятность выбора 1:1.6. Можно попробовать с настройкой фильтра self.daily_filter_direction = 1, то есть на бычьем рынке
            # 19 -- 'trading_view_ind + short_shift_random': индикатор трейдинг вью как тригер но выбор сигнала рандомный со смещением вероятности в шортовую сторону. Вероятность выбора 1:1.6. Можно попробовать с настройкой фильтра self.daily_filter_direction = -1, то есть на медвежьем рынке   
        """
   
    def calculate_ema(self, data):
        close = data['Close']
        ema1 = close.ewm(span=self.ema1_period, adjust=False).mean()
        ema2 = close.ewm(span=self.ema2_period, adjust=False).mean()
        ema3 = close.ewm(span=self.ema_trend_line, adjust=False).mean()
        data[f"EMA{self.ema1_period}"] = ema1
        data[f"EMA{self.ema2_period}"] = ema2
        data[f"EMA{self.ema_trend_line}"] = ema3
        data.dropna(inplace=True)
        return data    

    def calculate_stoch_rsi(self, data):
        close = data['Close']
        window = 14
        smooth1 = 3
        smooth2 = 3

        # Рассчитываем RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Рассчитываем стохастический RSI
        min_rsi = rsi.rolling(window=window, min_periods=1).min()
        max_rsi = rsi.rolling(window=window, min_periods=1).max()

        stoch_rsi = (rsi - min_rsi) / (max_rsi - min_rsi)
        stoch_rsi_k = stoch_rsi.rolling(window=smooth1, min_periods=1).mean()
        stoch_rsi_d = stoch_rsi_k.rolling(window=smooth2, min_periods=1).mean()

        data['StochRSI_%K'] = stoch_rsi_k * 100  # Приводим к диапазону 0-100
        data['StochRSI_%D'] = stoch_rsi_d * 100  # Приводим к диапазону 0-100
        data.dropna(inplace=True)

        return data

    def calculate_atr(self, data, atr_period):
        high = data['High'].values
        low = data['Low'].values
        close = data['Close'].values

        tr = [0] * len(data)
        atr = [0] * len(data)

        tr[0] = high[0] - low[0]

        # Calculate True Range (TR)
        for i in range(1, len(data)):
            tr_high_low = high[i] - low[i]
            tr_high_close_prev = abs(high[i] - close[i - 1])
            tr_low_close_prev = abs(low[i] - close[i - 1])
            tr[i] = max(tr_high_low, tr_high_close_prev, tr_low_close_prev)

        # Calculate ATR
        atr[atr_period - 1] = sum(tr[:atr_period]) / atr_period

        for i in range(atr_period, len(data)):
            atr[i] = (atr[i - 1] * (atr_period - 1) + tr[i]) / atr_period

        data_copy = data.copy()
        data_copy[f"ATR{atr_period}"] = atr
        data_copy.dropna(inplace=True)

        return data_copy, atr[-1]

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
    
    def calculate_vpvr(self, data, min_bins=10, max_bins=50):
        # Вычисляем динамическое количество корзин (bins) на основе количества свечей
        num_candles = self.ema_trend_line
        bins = min(max(min_bins, num_candles // 10), max_bins)
        data = data.tail(self.ema_trend_line)
        # print(data)        
        # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
        price_range = pd.cut(data['Close'], bins=bins)
        vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
        return vpvr

    def find_vpvr_levels(self, vpvr, num_levels=2):
        # Поиск наиболее объемных зон VPVR
        top_vpvr_indexes = vpvr.nlargest(num_levels).index
        vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
        return vpvr_levels
    
    def immediate_vpvr_level_defender(self, cur_price, vpvr_levels):
        disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
                    (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
        if not disposition:
            immediate_level = min(abs(vpvr_levels[0][2] - cur_price), abs(vpvr_levels[1][2] - cur_price)) + cur_price
            strongest_volum_level = [0, 0]

            for _, _, m, v in vpvr_levels:
                cur_volum_level = v / (1 + abs(cur_price - m) / cur_price)
                if cur_volum_level > strongest_volum_level[0]:
                    strongest_volum_level = [cur_volum_level, m]                                

            if vpvr_levels[0][2] > cur_price and vpvr_levels[1][2] > cur_price:
                return "L", immediate_level
            elif vpvr_levels[0][2] < cur_price and vpvr_levels[1][2] < cur_price:
                return "S", immediate_level
            elif strongest_volum_level[1] > cur_price:
                return "L", strongest_volum_level[1]
            elif strongest_volum_level[1] < cur_price:
                return "L", strongest_volum_level[1]

        return
    # ////////////////////
    def trend_line_defender(self, df):
        ema2= df[f"EMA{self.ema2_period}"].iloc[-1]
        ema3 = df[f"EMA{self.ema_trend_line}"].iloc[-1]
        if ema2 > ema3:
            return "L"
        if ema2 < ema3:
            return "S"
        return

    def ema_crossover_defender(self, df):
        ema1 = df[f"EMA{self.ema1_period}"]
        ema2 = df[f"EMA{self.ema2_period}"]
        if (ema1.iloc[-1] > ema2.iloc[-1] and ema1.iloc[-2] < ema2.iloc[-2]):
            return "L"
        if (ema1.iloc[-1] < ema2.iloc[-1] and ema1.iloc[-2] > ema2.iloc[-2]):
            return "S"
        return
    
    def stoch_rsi_srossover_defender(self, df):
        for i in range(1, 4):
            if (df['StochRSI_%K'].iloc[-1] > df['StochRSI_%D'].iloc[-1] and 
                df['StochRSI_%K'].iloc[-(i+1)] < df['StochRSI_%D'].iloc[-(i+1)]):                   
                return "L"
            if (df['StochRSI_%K'].iloc[-1] < df['StochRSI_%D'].iloc[-1] and 
                df['StochRSI_%K'].iloc[-(i+1)] > df['StochRSI_%D'].iloc[-(i+1)]):
                return "S"
        return
    
    def stoch_rsi_overTrade_defender(self, df):
        if df['StochRSI_%K'].iloc[-1] < self.stoch_rsi_over_sell and df['StochRSI_%D'].iloc[-1] < self.stoch_rsi_over_sell:
            return "L"
        if df['StochRSI_%K'].iloc[-1] > self.stoch_rsi_over_buy and (df['StochRSI_%D'].iloc[-1] > self.stoch_rsi_over_buy):
            return "S"
        return
    
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
                signals_list.append((symbol, 1))          

            elif (recommendation == 'STRONG_SELL'):
                signals_list.append((symbol, -1))             

        return signals_list    

class INDICATORS_STRATEGYY(INDICATORS):
    def __init__(self) -> None:
        super().__init__()
        # устанавливаем функциии декораторы
        self.get_signals = self.log_exceptions_decorator(self.get_signals)
    
    def get_signals(self, strategy_list, coins_list):
        # print(ema1_period, self.ema2_period, ema3_period)

        if 'trading_view_ind' in strategy_list:                        
            get_tv_signals_list = self.get_tv_signals(coins_list)
            if get_tv_signals_list:
                for symbol, cur_signal in get_tv_signals_list:
                    df = None
                    try:
                        df = self.get_klines(symbol, self.interval, self.ema_trend_line)
                        if isinstance(df, pd.DataFrame) and not df.empty:
                            cur_price = df['Close'].iloc[-1]
                            if 'trend_line' not in strategy_list:
                                return symbol, cur_signal, cur_price, df
                                            
                            df = self.calculate_ema(df, self.ema1_period, self.ema2_period, self.ema_trend_line)
                            trend_line_defender_val = self.trend_line_defender(df)
                            if cur_signal == 1 and trend_line_defender_val == "L":                                       
                                return symbol, 1, cur_price, df 
                            if cur_signal == -1 and trend_line_defender_val == "S":                         
                                return symbol, -1, cur_price, df
                    except Exception as ex:
                        # print(ex)
                        self.black_coins_list.append(symbol)
                        self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]

                    time.sleep(0.05)
        else:
            for symbol in coins_list:
                signals_assum = 0
                long_trend = False
                short_trend = False
                df = None
                try:                        
                    df = self.get_klines(symbol, self.interval, self.ema_trend_line)
                    if isinstance(df, pd.DataFrame) and not df.empty:
                        df = self.calculate_ema(df, ema1_period, self.ema2_period, self.ema_trend_line
                        cur_price = df["Close"].iloc[-1]
                        # print(f"cur_price: {cur_price}")           
                        
                        if 'ema_crossover' in strategy_list: 
                            ema_crossover_defender_val = ema_crossover_defender(df)                       
                            if ema_crossover_defender_val == "L":
                                # print(f"ema_crossover signals_assum += 1")
                                signals_assum += 1  
                            elif ema_crossover_defender_val == "S":
                                # print(f"ema_crossover signals_assum -= 1")
                                signals_assum -= 1
                            # else:
                            #     print(f"ema_crossover signals_assum: None")

                        if {'trend_line', 'anti_trend_line'} & set(strategy_list):
                            trend_line_defender_val = trend_line_defender(df)
                            if trend_line_defender_val == "L":
                                # print(f"trend_line signals_assum += 1")
                                long_trend = True
                                if 'trend_line' in strategy_list:
                                    signals_assum += 1
                                if 'anti_trend_line' in strategy_list:
                                    signals_assum -= 1
                            elif trend_line_defender_val == "S":
                                # print(f"trend_line signals_assum -= 1")
                                short_trend = True
                                if 'trend_line' in strategy_list:
                                    signals_assum -= 1
                                if 'anti_trend_line' in strategy_list:
                                    signals_assum += 1                    
                            
                        if 'stoch_rsi_crossover' in strategy_list:
                            df = self.calculate_stoch_rsi(df)
                            stoch_rsi_srossover_defender_val = stoch_rsi_srossover_defender(df)
                            if stoch_rsi_srossover_defender_val == "L":
                                signals_assum += 1
                            elif stoch_rsi_srossover_defender_val == "S":
                                signals_assum -= 1

                        if 'stoch_rsi_overTrade' in strategy_list:
                            df = self.calculate_stoch_rsi(df)
                            stoch_rsi_overTrade_defender_val = stoch_rsi_overTrade_defender(df)
                            # print(stoch_rsi_overTrade_defender_val)
                            if stoch_rsi_overTrade_defender_val == "L":
                                signals_assum += 1
                            elif stoch_rsi_overTrade_defender_val == "S":
                                signals_assum -= 1

                        if {'trande_shift_random', 'long_shift_random', 'short_shift_random'} & set(strategy_list):
                            if 'trande_shift_random' in strategy_list:
                                if long_trend:
                                    random_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2]

                                elif short_trend:
                                    random_list = [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1]

                                if long_trend or short_trend:                         
                                    if choice(random_list) % 2 != 0:
                                        return symbol, 1, cur_price, df
                                    else:
                                        return symbol, -1, cur_price, df
                            else:
                                if 'long_shift_random' in strategy_list:
                                    random_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2]
                                if 'short_shift_random' in strategy_list:
                                    random_list = [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1]
                                if choice(random_list) % 2 != 0:
                                    return symbol, 1, cur_price, df
                                else:
                                    return symbol, -1, cur_price, df
                                
                        if 'vpvr_level' in strategy_list:
                            immediate_vpvr_level_defender_val = None
                            vpvr = self.calculate_vpvr(df)                       
                            vpvr_levels = self.find_vpvr_levels(vpvr)
                            immediate_vpvr_level_defender_val = self.immediate_vpvr_level_defender(cur_price, vpvr_levels)
                            
                            if immediate_vpvr_level_defender_val:
                                if immediate_vpvr_level_defender_val[0] == 'L':
                                    # print("L")
                                    signals_assum += 1
                                elif immediate_vpvr_level_defender_val[0] == 'S':
                                    # print("S")
                                    signals_assum -= 1
                                self.vpvr_level_line = immediate_vpvr_level_defender_val[1]

                        if signals_assum > 0 and signals_assum == len(strategy_list):
                            return symbol, 1, cur_price, df 
                        elif signals_assum < 0 and abs(signals_assum) == len(strategy_list):
                            return symbol, -1, cur_price, df
                except Exception as ex:
                    # print(ex)
                    # self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}") 
                    self.black_coins_list.append(symbol)
                    self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]
                
                time.sleep(0.05)

        return None, None, None, None
    
    def closing_by_crossover_signal(self, cur_direction):
        ema_crossover_defender_val = ema_crossover_defender(df)                       
        if ema_crossover_defender_val == "L":
            # print(f"ema_crossover signals_assum += 1")
            signals_assum += 1  
        elif ema_crossover_defender_val == "S":
            # print(f"ema_crossover signals_assum -= 1")
            signals_assum -= 1
        # else:
        #     print(f"ema_crossover signals_assum: None")
   