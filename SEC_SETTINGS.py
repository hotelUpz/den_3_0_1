import math
import pytz
from SETTINGS import SETTINGSS

class SEC_SETTINGSS(SETTINGSS):
    def __init__(self) -> None:
        super().__init__()
        self.my_name = 'Николай' # Ваше имя
        self.veryf_attemts_number = 9 # количество попыток доступа в ваш тг бот после неверно введенного пароля
        self.show_statistic_hour = 21 # время показа дневной статистики (21 - в 9 часов вечера каждого дня)
        self.local_tz = pytz.timezone('Europe/Kiev') # 'Europe/Berlin' -- часовой пояс

        # //////////////////////////// НАСТРОЙКИ ФИЛЬТРА МОНЕТ:
        self.default_black_coins_list = self.black_coins_list = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'UNIUSDT', 'FETUSDT'] # монеты исключения
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