

# class DEV():

#     def find_horizontal_flats(df, window=60, percentile=0.30, range_threshold=0.02):
        
#         # Расчет скользящего стандартного отклонения цен закрытия
#         df['RollingStdDev'] = df['Close'].rolling(window=window).std()
        
#         # Расчет перцентиля стандартного отклонения
#         std_dev_threshold = df['RollingStdDev'].quantile(percentile)
        
#         # Расчет среднего значения цен закрытия за окно
#         df['RollingMean'] = df['Close'].rolling(window=window).mean()
        
#         # Определение флэта на основе порога стандартного отклонения и диапазона
#         df['IsFlat'] = np.where(
#             (df['RollingStdDev'] < std_dev_threshold) &
#             ((df['Close'] <= df['RollingMean'] * (1 + range_threshold)) & (df['Close'] >= df['RollingMean'] * (1 - range_threshold))),
#             1, 0
#         )
        
#         return df['IsFlat'].iloc[-2]
    
#     # def filter_flat_coins_by_BB_and_KC(self, data, atr_period):
#     #     df = data.copy()
#     #     df['sma'] = df['Close'].rolling(window=atr_period).mean()
#     #     df['stddev'] = df['Close'].rolling(window=atr_period).std()
#     #     df['lower_band'] = df['sma'] - (self.BB_stddev_MULTIPLITER * df['stddev'])
#     #     df['upper_band'] = df['sma'] + (self.BB_stddev_MULTIPLITER * df['stddev'])

#     #     atr_column_name = f"ATR{atr_period}"
#     #     # Продолжение с вычислением Keltner Channel
#     #     df['lower_keltner'] = df['sma'] - (df[atr_column_name] * self.KC_stddev_MULTIPLITER)
#     #     df['upper_keltner'] = df['sma'] + (df[atr_column_name] * self.KC_stddev_MULTIPLITER)
        
#     #     # Проверяем условие для последних шести строк
#     #     last_6_rows = df.iloc[-6:]        
#     #     return (last_6_rows['lower_band'] > last_6_rows['lower_keltner']).all() & \
#     #         (last_6_rows['upper_band'] < last_6_rows['upper_keltner']).all()

#     def filter_flat_coins_by_BB_and_KC(self, data, atr_period):
#         df = data.copy()
#         df['sma'] = df['Close'].rolling(window=atr_period).mean()
#         df['stddev'] = df['Close'].rolling(window=atr_period).std()
#         df['lower_band'] = df['sma'] - (self.BB_stddev_MULTIPLITER * df['stddev'])
#         df['upper_band'] = df['sma'] + (self.BB_stddev_MULTIPLITER * df['stddev'])

#         df['TR'] = abs(df['High'] - df['Low'])
#         df['ATR'] = df['TR'].rolling(window=20).mean()
#         df['lower_keltner'] = df['sma'] - (df['ATR'] * self.KC_stddev_MULTIPLITER)
#         df['upper_keltner'] = df['sma'] + (df['ATR'] * self.KC_stddev_MULTIPLITER)
        
#         # Проверяем условие для последних шести строк
#         last_6_rows = df.iloc[-6:]        
#         return (last_6_rows['lower_band'] > last_6_rows['lower_keltner']).all() & \
#             (last_6_rows['upper_band'] < last_6_rows['upper_keltner']).all()
        
#     def change_volatility_indicator(self, df, atr_period):
#         speed_change_consistence, flat_consistence, average_consistence = False, True, False
#         # Установка периодов для расчета скользящего среднего ATR
#         atr_period1 = self.ema1_period
#         atr_period2 = self.ema2_period

#         # Получение текущих значений ATR для заданного периода
#         atr_rolling_mean = df[f"ATR{atr_period}"]

#         # Расчет скользящих средних ATR для двух различных периодов
#         atr_rolling_mean_1 = atr_rolling_mean.rolling(window=atr_period1).mean()
#         atr_rolling_mean_2 = atr_rolling_mean.rolling(window=atr_period2).mean()

#         # Проверка на наличие NaN и замена их на предыдущие значения или 0
#         atr_rolling_mean_1.bfill(inplace=True)
#         atr_rolling_mean_2.bfill(inplace=True)
#         atr_rolling_mean_1.fillna(0, inplace=True)
#         atr_rolling_mean_2.fillna(0, inplace=True)

#         # Проверка деления на ноль и на NaN
#         if atr_rolling_mean_2.iloc[-1] == 0:
#             return speed_change_consistence, flat_consistence, average_consistence

#         # Вычисление текущего отношения ATR к его более длинному скользящему среднему
#         atr_cur_moving = atr_rolling_mean.iloc[-1] / atr_rolling_mean_2.iloc[-1]

#         # Вычисление отношения более короткого скользящего среднего ATR к более длинному
#         atr_mean_moving = atr_rolling_mean_1.iloc[-1] / atr_rolling_mean_2.iloc[-1]

#         # Условия для оценки консистенции изменения скорости, флэта и средней консистенции
#         speed_change_consistence = atr_cur_moving > self.ATR_rigidity_upper
#         flat_consistence = atr_mean_moving < self.ATR_rigidity_lower
#         average_consistence = self.ATR_rigidity_lower <= atr_mean_moving <= self.ATR_rigidity_upper

#         return speed_change_consistence, flat_consistence, average_consistence
    

#     # def check_stairwell_ema(self, df, ema_degrees):
#     #     ema_slice = df.iloc[-ema_degrees[0]:-2]

#     #     # Check if all values are in either ascending or descending order
#     #     ascending_order = all((ema_slice[f"{self.ma_key_name}{ema_degrees[i]}"] < ema_slice[f"{self.ma_key_name}{ema_degrees[i + 1]}"]).all() for i in range(len(ema_degrees) - 1))
#     #     descending_order = all((ema_slice[f"{self.ma_key_name}{ema_degrees[i]}"] > ema_slice[f"{self.ma_key_name}{ema_degrees[i + 1]}"]).all() for i in range(len(ema_degrees) - 1))

#     #     return ascending_order or descending_order
        
#     # def flat_filter_handler(self, df, atr_period, symbol):
#     #     try:
#     #         if self.find_coins_in_flat_by_BB_KC:                                
#     #             is_flat_by_BB_and_KC_true = self.filter_flat_coins_by_BB_and_KC(df, atr_period)
#     #             if is_flat_by_BB_and_KC_true is None:
#     #                 return
#     #             if (self.find_coins_in_flat_by_BB_KC and is_flat_by_BB_and_KC_true):
#     #                 print(f"Монета {symbol} во флете BB+KC")
#     #                 return True

#     #         if self.find_coins_in_flat_by_ATR or self.over_moving_by_ATR_flag:               
#     #             change_volatility_indicator_answ = self.change_volatility_indicator(df, atr_period)
#     #             if change_volatility_indicator_answ is None:
#     #                 return
#     #             speed_change_consistence, flat_consistence, average_consistence = change_volatility_indicator_answ
#     #             if self.find_coins_in_flat_by_ATR and flat_consistence:
#     #                 print(f"Монета {symbol} во флете ATR")
#     #                 # total_flat_list_ATR.append(symbol)
#     #                 return True
#     #             if self.over_moving_by_ATR_flag and not speed_change_consistence:
#     #                 print(f"Монета {symbol} не соответствует фильтру over_moving_by_ATR_flag")
#     #                 # total_flat_list_ATR.append(symbol)
#     #                 return True

#     #         if self.peacock_tail_EMA_flag:
#     #             if not self.check_stairwell_ema(df, self.EMA_degree_tuple):
#     #                 print(f"Монета {symbol} не соответствует фильтру Stairwell_Ema")
#     #                 # total_flat_list_EMA_DEGREE.append(symbol)
#     #                 return True
#     #     except Exception as ex:
#     #         self.handle_exception(f"{ex} {inspect.currentframe().f_lineno}")
#     #     return