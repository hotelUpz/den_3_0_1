is_terminal_only = True # True/False только терминал/тг бот + терминал (1/0)

class SETTINGSS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        # /////////////// БАЗОВЫЕ ТОРГОВЫЕ ПАРАМЕТРЫ:
        self.depo = 12 # депозит в USDT -- считатеся вместе с кредитным плечом. Если == 1000 и кредитное плечо равно 10 то ваших денег == 1000/ 10 то есть 100
        self.lev_size = 2 # размер кредитного плеча
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)
        self.secondary_orders_type = 1 # 1/2: 'TAKE_PROFIT_MARKET'/'LIMIT'
        
        # //////////////////////////// НАСТРОЙКИ ИНДИКАТОРА:
        self.indicators_strategy_number = 14 # номер стратегии индикаторов

        # номера индикаторов:
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
        # 8 -- 'ema_crossover + simple_random': кроссовер ema как тригер но выбор сигнала рандомный. Вероятность выбора 1:1
        # 9 -- 'ema_crossover + trande_shift_random': кроссовер ema как тригер но выбор сигнала рандомный со смещением вероятности в сторону тренда. Вероятность выбора 1:1.6
        # 10 -- 'ema_crossover + long_shift_random': кроссовер ema как тригер но выбор сигнала рандомный со смещением вероятности в лонговую сторону. Вероятность выбора 1:1.6. Можно попробовать с настройкой фильтра self.daily_filter_direction = 1, то есть на бычьем рынке
        # 11 -- 'ema_crossover + short_shift_random': кроссовер ema как тригер но выбор сигнала рандомный со смещением вероятности в шортовую сторону. Вероятность выбора 1:1.6. Можно попробовать с настройкой фильтра self.daily_filter_direction = -1, то есть на медвежьем рынке

        # (инновационные)
        # 12 - 'ema_crossover + vpvr_level' # кроссовер ema плюс + vpvr индикатор
        # 13 - 'volum_splash_indicator' # ищим флеты обьема и ждем всплеска обьема
        # 14 - 'find_flats + volum_splash_indicator_2' # ищим флеты цены и ждем всплеска обьема

        # /////////////// для всех видов индикаторов:
        self.swirch_to_WMA_flag = False # использовать WMA вместо EMA
        self.is_reverse_signal = 1 # Вкл/Выкл: -1/1 # использовать обратный сигнал. Если шорт то лонг и наоборот. Чтобы активировать введите значение -1 (минус один)
        self.is_reverse_defencive_mehanizm = False # Вкл/Выкл:  True/False -- применять антистратегию в случае неудачной сделки
        self.only_long_trading = False # Вкл/Выкл: True/False -- торговать только лонговые позиции. Можно пробовать под бычью фазу рынка
        self.only_short_trading = False # Вкл/Выкл: True/False -- торговать только шортовые позиции. Можно пробовать под медвежью фазу рынка
        self.defend_total_market_trend_flag = False # определять тренд рынка автоматически
        self.only_stop_loss_flag = False # торговать только со стопами
        self.only_take_profit_flag = False # торговать только с тейк профитом
        self.closing_by_ema_crossover_flag = True # True/False Закрывать позицию по сигналу ema crossover/нет
        
        # ////////// для всех стратегий индикаторов кроме 13 и 14:
        self.ema1_period = 7 # - длина короткой волны
        self.ema2_period = 21 # - длина длинной волны
        self.ema_trend_line = 240 # - длинга тренда

        # ////////// для индикаторов 6 и 7:
        self.stoch_rsi_over_sell, self.stoch_rsi_over_buy = 30, 70 # уровни перепроданности и перекупленности стохастик-рси.

        # ////////// для индикатора 13:
        self.low_volume_percentile_anomalous_volume_1 = 0.38 # нижний перцентиль для индикатора обЬема
        self.high_volume_percentile_anomalous_volume_1 = 0.95 # верхний перцентиль для индикатора обЬема
        
        # ////////// для индикатора 14:
        self.std_multiplier_anomalous_volume_2 = 3.0 # множитель стандартного отклонения обьема при вычислении индикатора обема
        self.BB_stddev_MULTIPLITER = 2.1 # параметр жесткости фильтра BB (Линии Боллинджера)
        self.KC_stddev_MULTIPLITER = 1.6 # параметр жесткости фильтра KC (Канал Кэтлера)      

        # //////////////////// ТАЙМ ФРЕЙМ:
        self.kline_time, self.time_frame = 1, 'm' # таймфрейм где челое число - период, а буква - сам тайм фрейм (минута, час и т.д (m, h))

        # //////////////////////////// НАСТРОЙКИ СТОП ЛОСС И ТЕЙК ПРОФИТА:
        self.stop_loss_global_type = 2
        # 1 -- 'TRAILLING_CUSTOM' # треллинг стоп лосс кастомный (не бинансовский)
        # 2 -- 'FIXED' # фиксированные стоп лосс и тейк профит
        self.risk_reward_ratio = '1.1:0.9'  # соотношение риска к прибыли.
        # //////// способы вычисления точки стоп лосса: /////////////////

        self.stop_loss_ratio_mode = 8 # Метод для расчета коэффициента стоп-лосса. 
        # '1': 'static', -- статический процент. Рекомендуется для self.stop_loss_global_type = 1 ('TRAILLING_CUSTOM')
        # '2': 'volatility_period_20', -- по волатильности последних 20 свечей
        # '3': 'last_volatility', -- по волатильности последней свечи
        # '4': 'last_candle_length', --- по длине последней свечи
        # '5': 'last_candle_length/2', --- по длине последней свечи/ 2 - почти то же что и '3': 'last_volatility'
        # '6': 'last_minimum', -- предпоследний минимум или максимум - в зависимости от направленности сигнала
        # '7': 'absolute_minimum', наибольший минимум или максимум последних 20 свечей - в зависимости от направленности сигнала
        # '8': 'vpvr_level', -- по уровням обьема (ликвидности)
        
        self.stop_loss_ratio = None # в % Множитель стоп лосса. Для self.stop_loss_ratio_mode 2 - 8  -- расчитывается динамически -- этот параметр НЕ ТРОГАТЬ!! Он приведен для информации!
        self.static_stop_loss_ratio_val = 0.5 # в % Множитель стоп лосса. Только для статического стоп лосс коэффициента -- self.stop_loss_ratio_mode = 1
        self.min_default_ratio = 0.5 # в %. self.stop_loss_ratio сбрасывается к этому значению если расчетное значение self.stop_loss_ratio НИЖЕ этого порога
        self.max_default_ratio = 3.0 # в % self.stop_loss_ratio сбрасывается к этому значению если расчетное значение self.stop_loss_ratio ВЫШЕ этого порога

        # //////////////////////////// НАСТРОЙКИ МАРТИН ГЕЙЛА:
        self.martin_gale_flag = False # мартин гейл флаг. Включить/выкл: --  True/False. Рекомендуется использовать вместе с self.stop_loss_ratio_mode = 1 -- статические величины стоп лосс коэфф в процентах
        # ///////// следующие настройки мартин гейла актуальны только если self.martin_gale_flag = True
        self.classikal_martin_gale = True # Вкл/Выкл: True/False -- классический мартин гейл  
        self.martin_gale_ratio = 2.0 # множитель депозита
        self.max_martin_gale_counter_auto_true = False # Вкл/Выкл: True/False # расчитать множитель мартин гейла автоматически с учетом общего баланса
        self.max_martin_gale_counter = 2 # сколько раз умножать позицию. При self.max_martin_gale_counter_auto_true = True расчитает этот счетчик автоматически
        self.play_by_leverage = True # Вкл/Выкл: True/False умножать депозит за счет плеча/за счет собственных средств
     
        # /////////// ЗАЩИТНЫЕ МЕХАНИЗМЫ:
        self.losses_protection = True # Вкл/Выкл: True/False. Стратегия защиты от потерь. Если включена то устанавливается лимит неудачных сделок. После серии таких сделок, робот отключается. Значение (количество потерь) задается ниже
        self.losses_until_value = 2 # количество неудачных сделок после которого робот выключится

        self.is_proxies_true = False # Вкл/Выкл: True/False Использовать прокси/не использовать