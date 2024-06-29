import pandas as pd
from random import choice
import pandas as pd
import pandas_ta as ta
import numpy as np
from api_binance import BINANCE_API
import time
import os
import inspect
current_file = os.path.basename(__file__)

# self.swirch_to_WMA_flag

class INDICATORS(BINANCE_API):
    def __init__(self) -> None:
        super().__init__()  
        # устанавливаем функциии декораторы
        self.calculate_ema = self.log_exceptions_decorator(self.calculate_ema)
        self.calculate_wma = self.log_exceptions_decorator(self.calculate_wma)
        self.calculate_atr = self.log_exceptions_decorator(self.calculate_atr)
        self.calculate_stoch_rsi = self.log_exceptions_decorator(self.calculate_stoch_rsi)
        self.calculate_vpvr = self.log_exceptions_decorator(self.calculate_vpvr)
        self.find_vpvr_levels = self.log_exceptions_decorator(self.find_vpvr_levels)
        self.calculate_anomalous_volume_1 = self.log_exceptions_decorator(self.calculate_anomalous_volume_1)
        self.calculate_anomalous_volume_2 = self.log_exceptions_decorator(self.calculate_anomalous_volume_2)
        # self.filter_flat_coins_by_BB_and_KC = self.log_exceptions_decorator(self.filter_flat_coins_by_BB_and_KC)
        # self.change_volatility_indicator = self.log_exceptions_decorator(self.change_volatility_indicator)

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
            # 13 - 'find_coins_in_flat + volum_splash_indicator' # ищим флеты и ждем всплеска обьема 
        """  
    
    def calculate_ema(self, data):
        close = data['Close']
        # if not self.peacock_tail_EMA_flag:
        data[f"{self.ma_key_name}{self.ema1_period}"] = close.ewm(span=self.ema1_period, adjust=False).mean()
        data[f"{self.ma_key_name}{self.ema2_period}"] = close.ewm(span=self.ema2_period, adjust=False).mean()
        # else:
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[0]}"] = close.ewm(span=self.EMA_degree_tuple[0], adjust=False).mean()
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[1]}"] = close.ewm(span=self.EMA_degree_tuple[1], adjust=False).mean()
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[2]}"] = close.ewm(span=self.EMA_degree_tuple[2], adjust=False).mean()
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[3]}"] = close.ewm(span=self.EMA_degree_tuple[3], adjust=False).mean()
        data[f"{self.ma_key_name}{self.ema_trend_line}"] = close.ewm(span=self.ema_trend_line, adjust=False).mean()
        data.dropna(inplace=True)
        return data

    def calculate_wma(self, data):
        close = data['Close']

        def weighted_moving_average(values, window):
            weights = np.arange(1, window + 1)
            return values.rolling(window).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

        # if not self.peacock_tail_EMA_flag:
        data[f"{self.ma_key_name}{self.ema1_period}"] = weighted_moving_average(close, self.ema1_period)
        data[f"{self.ma_key_name}{self.ema2_period}"] = weighted_moving_average(close, self.ema2_period)
        # else:
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[0]}"] = weighted_moving_average(close, self.EMA_degree_tuple[0])
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[1]}"] = weighted_moving_average(close, self.EMA_degree_tuple[1])
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[2]}"] = weighted_moving_average(close, self.EMA_degree_tuple[2])
        #     data[f"{self.ma_key_name}{self.EMA_degree_tuple[3]}"] = weighted_moving_average(close, self.EMA_degree_tuple[3])
            
        data[f"{self.ma_key_name}{self.ema_trend_line}"] = weighted_moving_average(close, self.ema_trend_line)
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
    
    # //////////////////////// volums assets:    
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

    # ///////// for 13 ind number:
    def calculate_anomalous_volume_1(self, df):
        # 1. Вычисляем скользящее среднее по объему
        df['AverageVolume'] = df['Volume'].rolling(window=self.average_volume_window).mean()

        # 2. Рассчитываем перцентиль средне минимального и среднемаксимального процентиля без последнего значения
        low_percentile_value = df['Volume'].iloc[:-1].rolling(window=self.average_volume_window).quantile(q=self.low_volume_percentile_anomalous_volume_1)
        
        high_percentile_value = df['Volume'].iloc[:-1].rolling(window=self.average_volume_window).quantile(q=self.high_volume_percentile_anomalous_volume_1)
        
        # 3. Проверяем условия аномального объема
        conditions_1 = all(df['Volume'].iloc[i] < low_percentile_value.iloc[-1] for i in range(-6, -1))
        # 4. Последняя свеча выше значения перцентиля
        conditions_2 = df['Volume'].iloc[-1] > high_percentile_value.iloc[-1]
        
        # 6. Определение направления объема (зеленый или красный)
        df['VolumeDirection'] = np.where(df['Close'] > df['Open'], 1, -1)

        return conditions_1 and conditions_2, df['VolumeDirection'].iloc[-1]
    
    # ///////////// for 14 ind number:
    def calculate_anomalous_volume_2(self, df):
        # Расчет среднего и стандартного отклонения объема
        df['AverageVolume'] = df['Volume'].rolling(window=self.average_volume_window).mean()
        df['StdVolume'] = df['Volume'].rolling(window=self.average_volume_window).std()

        # Расчет верхней границы для аномального объема
        df['UpperVolumeLimit'] = df['AverageVolume'] + self.std_multiplier_anomalous_volume_2 * df['StdVolume']

        # Определение, является ли текущий объем аномальным
        df['AnomalousVolume'] = df['Volume'] > df['UpperVolumeLimit']         
        
        # 6. Определение направления объема (зеленый или красный)
        df['VolumeDirection'] = np.where(df['Close'] > df['Open'], 1, -1)

        return df['AnomalousVolume'].iloc[-1], df['VolumeDirection'].iloc[-1]
    
    def filter_flat_coins_by_BB_and_KC(self, data, atr_period):
        df = data.copy()
        df['sma'] = df['Close'].rolling(window=atr_period).mean()
        df['stddev'] = df['Close'].rolling(window=atr_period).std()
        df['lower_band'] = df['sma'] - (self.BB_stddev_MULTIPLITER * df['stddev'])
        df['upper_band'] = df['sma'] + (self.BB_stddev_MULTIPLITER * df['stddev'])

        df['TR'] = abs(df['High'] - df['Low'])
        df['ATR'] = df['TR'].rolling(window=20).mean()

        df['lower_keltner'] = df['sma'] - (df['ATR'] * self.KC_stddev_MULTIPLITER)
        df['upper_keltner'] = df['sma'] + (df['ATR'] * self.KC_stddev_MULTIPLITER)
        
        # Проверяем условие для последних шести свечей
        last_6_rows = df.iloc[-6:]        
        return (last_6_rows['lower_band'] > last_6_rows['lower_keltner']).all() & \
            (last_6_rows['upper_band'] < last_6_rows['upper_keltner']).all()
        
class CONDITION_ANALYSES(INDICATORS):
    def __init__(self) -> None:
        super().__init__() 
        # self.check_stairwell_ema = self.log_exceptions_decorator(self.check_stairwell_ema)
        self.trend_line_defender = self.log_exceptions_decorator(self.trend_line_defender)
        self.ema_crossover_defender = self.log_exceptions_decorator(self.ema_crossover_defender)
        self.stoch_rsi_srossover_defender = self.log_exceptions_decorator(self.stoch_rsi_srossover_defender)
        self.stoch_rsi_overTrade_defender = self.log_exceptions_decorator(self.stoch_rsi_overTrade_defender)
        self.random_defender = self.log_exceptions_decorator(self.random_defender)
        # self.flat_filter_handler = self.log_exceptions_decorator(self.flat_filter_handler)

    def trend_line_defender(self, df):
        ema2= df[f"{self.ma_key_name}{self.ema2_period}"].iloc[-1]
        ema3 = df[f"{self.ma_key_name}{self.ema_trend_line}"].iloc[-1]
        if ema2 > ema3:
            return "L"
        if ema2 < ema3:
            return "S"
        return

    def ema_crossover_defender(self, df):
        ema1 = df[f"{self.ma_key_name}{self.ema1_period}"]
        ema2 = df[f"{self.ma_key_name}{self.ema2_period}"]
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
    
    def random_defender(self, strategy_list, long_trend, short_trend):
        
        if 'simple_random' in strategy_list:
            random_list = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
            if choice(random_list) % 2 != 0:
                return 1
            else:
                return -1

        if {'trande_shift_random', 'long_shift_random', 'short_shift_random'} & set(strategy_list):
            if 'trande_shift_random' in strategy_list:
                if long_trend:
                    random_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2]

                elif short_trend:
                    random_list = [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1]

                if long_trend or short_trend:                         
                    if choice(random_list) % 2 != 0:
                        return 1
                    else:
                        return -1
            else:
                if 'long_shift_random' in strategy_list:
                    random_list = [1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2]
                if 'short_shift_random' in strategy_list:
                    random_list = [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1]
                if choice(random_list) % 2 != 0:
                    return 1
                else:
                    return -1
        return    
    
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

class INDICATORS_STRATEGYY(CONDITION_ANALYSES):
    def __init__(self) -> None:
        super().__init__()
        # устанавливаем функциии декораторы
        self.get_signals = self.log_exceptions_decorator(self.get_signals)
    
    def get_signals(self, strategy_list, coins_list):
        for symbol in coins_list:
            df = None
            signals_assum = 0
            long_trend = False
            short_trend = False
            atr_period = self.ema2_period + self.ema1_period
            try:
                df = self.get_klines(symbol, self.interval, self.ema_trend_line) 
                if (not isinstance(df, pd.DataFrame) or df.empty):
                    continue
                if self.indicators_strategy_number not in [13,14]:
                    if not self.swirch_to_WMA_flag:
                        df = self.calculate_ema(df)
                    else:
                        df = self.calculate_wma(df)
            except Exception as ex:
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
                continue

            # if self.over_moving_by_ATR_flag or self.find_coins_in_flat_by_BB_KC or self.find_coins_in_flat_by_ATR:
            #     if not self.flat_filter_handler(df, atr_period, symbol):                 
            #         continue           

            # print(symbol)
            try:
                cur_price = df["Close"].iloc[-1]
                # print(f"cur_price: {cur_price}")                                        
                if 'ema_crossover' in strategy_list:                    
                    ema_crossover_defender_val = self.ema_crossover_defender(df)                       
                    if ema_crossover_defender_val == "L":
                        # print(f"ema_crossover signals_assum += 1")
                        signals_assum += 1  
                    elif ema_crossover_defender_val == "S":
                        # print(f"ema_crossover signals_assum -= 1")
                        signals_assum -= 1

                if self.indicators_strategy_number == 13:
                    is_anomaly_resp = None             
                    is_anomaly_resp = self.calculate_anomalous_volume_1(df)

                    if is_anomaly_resp is None:
                        print("Проблемы с расчетом аномального индикатора обьема")
                        time.sleep(0.01)
                        continue
                    is_anomaly_volume_true, volum_direction = is_anomaly_resp
                    if is_anomaly_volume_true:
                        return symbol, volum_direction*(-1), cur_price, df
                    
                if self.indicators_strategy_number == 14:
                    if self.filter_flat_coins_by_BB_and_KC(df, atr_period):
                        print(f"{symbol} во флете")
                        is_anomaly_resp = None             
                        is_anomaly_resp = self.calculate_anomalous_volume_2(df)

                        if is_anomaly_resp is None:
                            print("Проблемы с расчетом аномального индикатора обьема 2")
                            time.sleep(0.01)
                            continue
                        is_anomaly_volume_true, volum_direction = is_anomaly_resp
                        if is_anomaly_volume_true:
                            return symbol, volum_direction*(-1), cur_price, df
                    continue

                if self.indicators_strategy_number in [2,3,5,7,9]:
                    trend_line_defender_val = self.trend_line_defender(df)
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

                if self.indicators_strategy_number in [8,9,10,11]:
                    random_defender_repl = None
                    random_defender_repl = self.random_defender(strategy_list, long_trend, short_trend)
                    if not random_defender_repl:
                        self.handle_messagee(f"Какие-то проблемы при попытке получить сигнал от рандомных индикаторов")
                    elif random_defender_repl == 1:
                        return symbol, 1, cur_price, df
                    elif random_defender_repl == -1:
                        return symbol, -1, cur_price, df
                    
                if 'stoch_rsi_crossover' in strategy_list:
                    df = self.calculate_stoch_rsi(df)
                    stoch_rsi_srossover_defender_val = self.stoch_rsi_srossover_defender(df)
                    if stoch_rsi_srossover_defender_val == "L":
                        signals_assum += 1
                    elif stoch_rsi_srossover_defender_val == "S":
                        signals_assum -= 1

                if 'stoch_rsi_overTrade' in strategy_list:
                    df = self.calculate_stoch_rsi(df)
                    stoch_rsi_overTrade_defender_val = self.stoch_rsi_overTrade_defender(df)
                    # print(stoch_rsi_overTrade_defender_val)
                    if stoch_rsi_overTrade_defender_val == "L":
                        signals_assum += 1
                    elif stoch_rsi_overTrade_defender_val == "S":
                        signals_assum -= 1
                        
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
                    # print("LONG " + "Монета: " + symbol)
                    if self.only_short_trading:
                        self.handle_messagee(f"Пропускаем сигнал так как self.only_short_trading == {self.only_short_trading}")
                        time.sleep(0.01)
                        continue
                    return symbol, 1, cur_price, df 
                
                elif signals_assum < 0 and abs(signals_assum) == len(strategy_list):
                    # print("SHORT " + "Монета: " + symbol)
                    if self.only_long_trading:
                        self.handle_messagee(f"Пропускаем сигнал так как self.only_long_trading == {self.only_long_trading}")
                        time.sleep(0.01)
                        continue
                    return symbol, -1, cur_price, df
            except Exception as ex:
                # print(ex)
                self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}") 
                self.black_coins_list.append(symbol)
                self.candidate_symbols_list = [x for x in self.candidate_symbols_list if x not in self.black_coins_list]
            
            time.sleep(0.01)

        return None, None, None, None