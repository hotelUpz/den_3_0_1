from SETTINGS import SETTINGSS
import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS(SETTINGSS):
    def __init__(self) -> None:
        super().__init__()
        # print("init VARIABLES")
        self.market_place = 'binance'
        self.default_tg_vars() 
        self.init_all_params()

        # /////////
        self.init_main_file_variables()
        self.init_keys()

    def init_main_file_variables(self):
        self.current_signal_val = None
        self.last_signal_val = None
        self.in_position = False 
        self.last_direction = None   
        self.close_open_dispetcher = False 
        self.is_first_position = True  
        self.create_order_success_flag = False
        self.is_no_signal_counter = 0
        self.show_absent_or_signal_every = 20
        self.cur_price = None
        self.enter_price = None
        self.last_enter_price = None
        self.qty = None
        self.price_precession = None
        self.total_potential_losses = 0
        self.losses_counter = 0
        self.is_trailing_stop_start = False
        self.executed_qty = None
        self.stop_loss_ratio = None
        self.stop_loss_multiplier = None 
        self.trigger_multiplier = None
        self.next_trigger_price = None
        self.sl_order_id = None
        self.last_date = None
        self.cur_date = None
        self.is_time_to_show_done = False

    def init_all_params(self):

        # ////////////////////// некоторые переменные:
        self.cur_klines_data = None
        self.direction = None 
        self.was_change_leverage_true = False  
        self.cur_martin_gale_counter = 0  
        self.last_message = None
        #///////////////////////////////////////////////
        self.ema_settings()
        self.default_statistic_vars()
        # self.init_keys()

    def ema_settings(self):
        self.interval = str(self.kline_time) + self.time_frame
        self.max_period = max(self.ema1_period, self.ema2_period)
        self.indicators_strategy_list_list = [['ema_crossover'], ['ema_crossover', 'trend_line'], ['ema_crossover', 'stoch_rsi_crossover'], ['ema_crossover', 'stoch_rsi_overTrade'], ['ema_crossover', 'stoch_rsi_overTrade', 'trend_line'], ['trend_line', 'smart_random']]
        self.indicators_strategy_list = self.indicators_strategy_list_list[self.indicators_strategy_number - 1]

    def default_statistic_vars(self):        
        self.win_los = 0 # результат последней сделки (в плюс или в минус)
        self.daily_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов
        self.total_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов

    # /////////// переменные... - суто по тех части: ///////////////////////
    def default_tg_vars(self):
        self.run_flag = 0
        self.stop_bot_flag = 0          
        self.block_acess_flag = 0
        self.start_flag = 0
        self.start_day_date = None
        self.block_acess_counter = 0
        self.seq_control_flag = 0
        self.stop_redirect_flag = 0  
        self.settings_redirect_flag = 0
        
    def init_keys(self): 
        # #////////////////////////////// для деплоя на сервер:
        self.api_key = os.getenv(f"{self.market_place.upper()}_API_PUBLIC_KEY", "")
        self.api_secret = os.getenv(f"{self.market_place.upper()}_API_PRIVATE_KEY", "")
        self.tg_api_token = os.getenv("TG_TOKEN", "")
        # print(self.tg_api_token)
        self.coinMarketCup_api_token = os.getenv("COIN_MARKET_CUP_TOKEN", "")
        self.seq_control_token = os.getenv("ACESS_TOKEN", "")
        self.proxy_host = os.getenv("proxy_host", "")
        self.proxy_port = os.getenv("proxy_port", "")
        self.proxy_username = os.getenv("proxy_username", "")
        self.proxy_password = os.getenv("proxy_password", "")
        # ////////////////////// инициализация ключей: ///////////////////////////////
        # self.api_key = BINANCE_API_PUBLIC_KEY
        # self.api_secret = BINANCE_API_PRIVATE_KEY 
        # # print(self.api_key)
        # self.tg_api_token = TG_TOKEN
        # # print(self.tg_api_token)
        # self.seq_control_token = ACESS_TOKEN
        # self.coinMarketCup_api_token = COIN_MARKET_CUP_TOKEN
        # self.proxy_host = proxy_host
        # self.proxy_port = proxy_port
        # self.proxy_username = proxy_username
        # self.proxy_password = proxy_password
