is_terminal_only = 0 # только терминал/тг бот + терминал (1/0)

class SETTINGSS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        # /////////////// БАЗОВЫЕ ТОРГОВЫЕ ПАРАМЕТРЫ:
        self.depo = 20 # депозит в USDT -- считатеся вместе с кредитным плечом. Если == 1000 и кредитное плечо равно 10 то ваших денег == 1000/ 10 то есть 100
        self.lev_size = 2 # размер кредитного плеча
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)
        self.secondary_orders_type = 2 # 1/2:  'TAKE_PROFIT_MARKET'/'LIMIT'
        
        # //////////////////////////// НАСТРОЙКИ ИНДИКАТОРА:
        self.indicators_strategy_number = 2 # номер стратегии индикаторов
        self.is_reverse_signal = 1 # Вкл/Выкл: -1/1 # использовать обратный сигнал. Если шорт то лонг и наоборот. Чтобы активировать введите значение -1 (минус один)
        # 1 -- 'ema_crossover': классическая стратегия прересечения двух ema (кроссовер)
        # 2 -- 'ema_crossover + trend_line': кроссовер ema плюс ориентироваться на линию тренда ema. Период равен ema_trend_line, cмотри ниже
        # 3 -- 'ema_crossover + stoch_rsi_crossover': ema кроссовер плюс кроссовер стохастик_рси
        # 4 -- 'ema_crossover + stoch_rsi_crossover + trend_line': ema кроссовер плюс кроссовер стохастик_рси плюс линия тренда
        # 5 -- 'ema_crossover + stoch_rsi_overTrade':  ema кроссовер плюс кроссовер стохастик_рси
        # 6 -- 'ema_crossover + stoch_rsi_overTrade + trend_line': то же что и предыдущий но плюс ориентрироваться на линию тренда
        # 7 - 'smart_random + trend_line' # рандомный выбор сигнала с ориентацией на тренд
        # 8 - 'trading_view_ind' # индикатор трейдинг вью
        # 9 - 'trading_view_ind + trend_line' # индикатор трейдинг вью + ориентироваться на линию тренда
        # 10 - 'ema_crossover + vpvr_level' # кроссовер ema плюс + vpvr индикатор        

        # Потенциально прибыльные связки для прямой стратегии (self.is_reverse_signal = 1):
            # 5-ЕМА и 20-ЕМА 
            # 5-ЕМА и 26-ЕМА
            # 13-ЕМА и 26-ЕМА
            # 13-ЕМА и 48-ЕМА 
            # 13-ЕМА и 49-ЕМА 
        # Потенциально прибыльные связки для антистратегии (self.is_reverse_signal = -1):
            # Короткая EMA: 5, Длинная EMA: 30
            # Короткая EMA: 5, Длинная EMA: 50
            # Короткая EMA: 7, Длинная EMA: 40
            # Короткая EMA: 10, Длинная EMA: 30
            # Короткая EMA: 15, Длинная EMA: 60
            # Короткая EMA: 25, Длинная EMA: 75
            # Короткая EMA: 10, Длинная EMA: 50
            # Короткая EMA: 20, Длинная EMA: 100
            # Короткая EMA: 50, Длинная EMA: 200

        self.ema1_period = 5 # - длина короткой волны
        self.ema2_period = 20 # - длина длинной волны
        self.ema_trend_line = 240 # - длинга тренда
        self.stoch_rsi_over_sell, self.stoch_rsi_over_buy = 30, 70 # уровни перепроданности и перекупленности стохастик-рси. Для стратегий индикатора 5 и 6 (self.indicators_strategy_number = 5 или self.indicators_strategy_number = 6)

        # //////////////////// ТАЙМ ФРЕЙМ:
        self.kline_time, self.time_frame = 15, 'm' # таймфрейм где челое число - период, а буква - сам тайм фрейм (минута, час и т.д (m, h))

        # //////////////////////////// НАСТРОЙКИ СТОП ЛОСС И ТЕЙК ПРОФИТА:
        self.stop_loss_global_type = 1
        # 1 -- 'TRAILLING_CUSTOM' # треллинг стоп лосс кастомный (не бинансовский)
        # 2 -- 'FIXED' # фиксированные стоп лосс и тейк профит
        self.risk_reward_ratio = '1:2'  # соотношение риска к прибыли.
        # //////// способы вычисления точки стоп лосса: /////////////////

        self.stop_loss_ratio_mode = 2 # Метод для расчета коэффициента стоп-лосса. 
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
        self.max_default_ratio = 1.5 # в % self.stop_loss_ratio сбрасывается к этому значению если расчетное значение self.stop_loss_ratio ВЫШЕ этого порога

        # //////////////////////////// НАСТРОЙКИ МАРТИН ГЕЙЛА:
        self.martin_gale_flag = 0 # мартин гейл флаг. Включить/выкл: - 1/0. Рекомендуется использовать вместе с self.stop_loss_ratio_mode = 1 -- статические величины в процентах
        # ///////// следующие настройки мартин гейла актуальны только если self.martin_gale_flag = 1
        self.martin_gale_ratio = 2.0 # множитель депозита
        self.max_martin_gale_counter_auto_true = 0 # расчитать множитель мартин гейла автоматически с учетом общего баланса
        self.max_martin_gale_counter = 3 # сколько раз умножать позицию. При self.max_martin_gale_counter_auto_true = 1 расчитает этот счетчик автоматически
        self.play_by_leverage = 1 # умножать депозит за счет плеча/за счет собственных средств: 1/0
     
        # /////////// ЗАЩИТНЫЕ МЕХАНИЗМЫ:
        self.losses_protection = 1 # Вкл/Выкл: 1/0. Стратегия защиты от потерь. Если включена то устанавливается лимит неудачных сделок. После серии таких сделок, робот отключается. Значение (количество потерь) задается ниже
        self.losses_until_value = 3 # количество неудачных сделок после которого робот выключится

        self.is_proxies_true = 1 # Использовать прокси/не использовать (1/0)