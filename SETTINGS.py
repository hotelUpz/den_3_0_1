import math

is_terminal_only = 1
#
class SETTINGSS():
    def __init__(self) -> None:
        # print("init SETTINGS")
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        self.my_name = 'Николай' # Ваше имя
        self.veryf_attemts_number = 9 # количество попыток доступа в ваш тг бот после неверно введенного пароля
        self.show_statistic_hour = 21 # время показа дневной статистики (21 - в 9 часов вечера каждого дня)
        self.is_proxies_true = 0 # Использовать прокси. Вкл/Выкл: 1/0
        self.init_main_settings()               

    def init_main_settings(self):
        # /////////////// БАЗОВЫЕ ТОРГОВЫЕ ПАРАМЕТРЫ:
        self.start_depo = self.depo = 10 # депозит в USDT -- считатеся вместе с кредитным плечом
        self.lev_size = 1 # размер кредитного плеча
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)
        self.losses_protection = 1 # Вкл/Выкл: 1/0. Стратегия защиты от потерь. Если включена то устанавливается лимит неудачных сделок. После серии таких сделок, робот отключается. Значение (количество) задается ниже
        self.losses_until_value = 3 # количество неудачных сделок после которого робот выключится

        # /////////////////////////////////////////////////////////////
        # //////////////////////////// НАСТРОЙКИ ИНДИКАТОРА:
        self.kline_time, self.time_frame = 1, 'm' # таймфрейм где челое число - период, а буква - сам тайм фрейм (минута, час и т.д (m, h))
        self.indicators_strategy_number = 5 # номер стратегии индикаторов
        # 1 -- 'ema_crossover': классическая стратегия прересечения двух ema (кроссовер)
        # 2 -- 'ema_crossover + trend_line': кроссовер ema плюс ориентироваться на линию тренда ema. Период равен ema_trend_line, cмотри ниже
        # 3 -- 'ema_crossover + stoch_rsi_crossover': ema кроссовер плюс кроссовер стохастик_рси
        # 4 -- 'ema_crossover + stoch_rsi_crossover + trend_line': ema кроссовер плюс кроссовер стохастик_рси плюс линия тренда
        # 5 -- 'ema_crossover + stoch_rsi_overTrade':  ema кроссовер плюс кроссовер стохастик_рси
        # 6 -- 'ema_crossover + stoch_rsi_overTrade + trend_line': то же что и предыдущий но плюс ориентрироваться на линию тренда
        # 7 - 'smart_random + trend_line' # рандомный выбор сигнала с ориентацией на тренд
        # 8 - 'trading_view_ind' # индикатор трейдинг вью
        # 9 - 'trading_view_ind + trend_line' # индикатор трейдинг вью + ориентироваться на линию тренда
        self.ema1_period = 5 # - длина короткой волны
        self.ema2_period = 20 # - длина длинной волны
        self.ema_trend_line = 240 # - длинга тренда
        self.stoch_rsi_over_sell, self.stoch_rsi_over_buy = 30, 70 # уровни перепроданности и перекупленности стохастик-рси
        self.is_reverse_signal = 1 # Вкл/Выкл: -1/1 # использовать обратный сигнал. Если шорт то лонг и наоборот. Чтобы активировать введите значение -1 (минус один)

        # /////////////////////////////////////////////////////////////
        # //////////////////////////// НАСТРОЙКИ СТОП ЛОСС И ТЕЙК ПРОФИТА:
        self.stop_loss_global_type = 2
        # 1 -- 'TRAILLING_CUSTOM' # треллинг стоп лосс кастомный (не бинансовский)
        # 2 -- 'FIXED' # фиксированные стоп лосс и тейк профит
        self.risk_reward_ratio = '0.7:0.9'  # соотношение риска к прибыли. только для 'FIXED или для'SIGNAL_ADVANCED'
        # //////// способы вычисления точки стоп лосса: /////////////////

        self.stop_loss_ratio_mode = 2 # Метод для расчета коэффициента стоп-лосса. В интерфейсе телеграм бота -- соответсвующий номер стратегии. По умолчанию равен 1 (статический коэффициент, равный установленному значению. Сейчас стоит 1 % (в процентах) -- смотри ниже, а так же смотри инструкцию внизу страницы
        self.static_stop_loss_ratio_val = 0.5 # в % Множитель стоп лосса. Для статического стоп лосс коэффициента
        self.min_default_ratio = 0.5 # в %. минимальное дефолтное значение коэффициента стоп лосса к которому сбрасываются значение стоп лосс коэффициента если расчетные значения слишком малы. В %
        self.max_default_ratio = 5 # в % максимальное дефолтное значение коэффициента стоп лосса
        # ///////////////////////////////////
        # /////////////////////////////////////////////////////////////
        # //////////////////////////// НАСТРОЙКИ МАРТИН ГЕЙЛА:
        self.martin_gale_flag = 0 # мартин гейл отключен. Включить/выкл: - 1/0
        self.martin_gale_ratio = 2.0 # множитель депозита
        self.max_martin_gale_counter_auto_true = 1 # расчитать множитель мартин гейла автоматически с учетом общего баланса
        self.max_martin_gale_counter = 3 # сколько раз умножать позицию. При self.max_martin_gale_counter_auto_true = 1 расчитает этот параметр автоматически

        # /////////////////////////////////////////////////////////////
        # /////////////////////////////////////////////////////////////
        # //////////////////////////// НАСТРОЙКИ ФИЛЬТРА МОНЕТ:
        self.black_coins_list = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT'] # монеты исключения. Например ['shitokusdt', 'shitok2usdt']
        self.price_filter_flag = 0 # фильтр по цене. Сейчас отключен. Включить/выкл: - 1/0
        self.MIN_FILTER_PRICE = 0 # минимальный порог цены. Можете указать свое значение.
        self.MAX_FILTER_PRICE = math.inf # максимальный порог цены. Можете указать свое значение.
        self.daily_filter_direction = 0 # 1 -- искать только которые показывают растущую динамику (зеленые графики). -1 --- для падающих (красные графики) на бинанс. 0 -- и то и другое
        self.slice_volum_flag = 1 # флаг фильтра по объему. Включить/выкл: - 1/0
        self.slice_volatilyty_flag = 1 # находить самые волатильные на бинанс. Включить/выкл: - 1/0
        self.SLICE_VOLATILITY = 90 # срез волатильности. То есть первые 40 самых волатильных
        self.min_volume_usdtFilter_flag = 0 # искать по минимальному объему торгов за сутки на бинанс. Включить/выкл: - 1/0
        self.MIN_VOLUM_USDT = 10000000 # размер минимального обьема в usdt. При активном флаге self.min_volume_usdtFilter_flag = 1
        self.SLICE_VOLUME_BINANCE_PAIRS = 90 # срез монет по объему торгов на бинанс То есть первые 60 самых проторгованных
        self.volume_range_true = 0 # ранжировать по объему. Включить/выкл: - 1/0
        self.volatility_range_true = 1 # ранжировать по волатильности. Включить/выкл: - 1/0
        self.in_coinMarketCup_is = 1 # показывать только те монеты которые есть в топе Coin Market Cup. Включить/выкл: - 1/0
        self.TOP_MARKET_CUP = 90 if self.indicators_strategy_number == 8 else 60 # срез монет. по коин маркет кап это будет первая тридцатка
            
"""
Типы глобальных стратегий стоп-лосса:
    (Регулируется параметром self.stop_loss_global_type. В интерфейсе телеграм бота -- соответсвующий номер стратегии. По умолчанию равен 2 (фиксированные стоп лосс/тейк профит))

    1 -- 'TRAILLING': Трейлинг-стоп, перемещающийся стоп-лосс, следуя за ценой.
    2 -- 'FIXED': Фиксированные стоп-лосс и тейк-профит.
.................

Методы для расчета коэффициента стоп-лосса:
    (Регулируется параметром self.stop_loss_ratio_mode. В интерфейсе телеграм бота -- соответсвующий номер метода. По умолчанию равен 1 (статический коэффициент, равный установленному значению. Сейчас стоит 1 % (в процентах))

    - fixed_stop_loss_ratio_val %: Фиксированное значение стоп-лосса для типа 'STATIC'.
    - min_default_ratio %: Минимальное значение коэффициента стоп-лосса по умолчанию.

    1. STATIC: Возвращает фиксированное значение стоп-лосса, заданное параметром fixed_stop_loss_ratio_val.

    2. VOLATILITY_PERIOD_20: Расчитывает коэффициент стоп-лосса на основе среднего истинного диапазона (ATR) за период, равный половине количества свечей в candles_df, плюс одна свеча.

    3. LAST_VOLATILITY: Использует максимальное отклонение закрытия второй с конца свечи от её минимума или максимума.

    4. LAST_CANDLE_LENGTH: Рассчитывает коэффициент стоп-лосса как разницу между максимумом и минимумом второй с конца свечи.

    5. LAST_CANDLE_LENGTH/2: Аналогично LAST_CANDLE_LENGTH, но значение делится пополам.

    6. LAST_MINIMUM: Если позиция длинная (direction = 1), используется разница между закрытием и минимумом второй с конца свечи; если короткая (direction = -1), используется разница между закрытием и максимумом второй с конца свечи.

    7. ABSOLUTE_MIN: Для длинной позиции рассчитывается разница между ценой входа и абсолютным минимумом свечей периода 20; для короткой позиции - между ценой входа и абсолютным максимумом свечей. Если минимум/максимум выходит за пределы цены входа, возвращается фиксированное значение стоп-лосса.
    .............................

- risk_reward_ratio = '1:1.5' -- соотношение риска к прибыли. только для 'FIXED'

"""