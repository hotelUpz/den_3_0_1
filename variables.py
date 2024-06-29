from SEC_SETTINGS import SEC_SETTINGSS
# from HIDDEN.config import *
import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS(SEC_SETTINGSS):
    def __init__(self) -> None:
        super().__init__()
        self.market_place = 'binance'
        self.order_id = None
        self.sl_order_id, self.tp_order_id = None, None
        self.target_tp_price = None
        self.last_stop_loss_price = None
        self.start_depo = self.depo
        self.lev_size_default = self.lev_size
        self.retry_trade = False
        self.last_win_los = None
        if self.only_long_trading or self.only_short_trading:
            self.only_long_trading = not self.only_short_trading
        self.default_reverse_signal = self.is_reverse_signal
        if not self.martin_gale_flag:
            self.classikal_martin_gale = False
        self.only_long_trading_default = self.only_long_trading
        self.only_short_trading_default = self.only_short_trading   
        if (self.only_stop_loss_flag or self.only_take_profit_flag) and self.stop_loss_global_type != 2:
            self.only_stop_loss_flag, self.only_take_profit_flag = False, False
            print("Смена флагов self.only_stop_loss_flag и self.only_take_profit_flag в режим True допустима только для фиксированной стратегии стоп лосса (self.stop_loss_global_type = 2). Поэтому данные флаги неактивны")
            print("self.only_stop_loss_flag, self.only_take_profit_flag = False, False")
        self.average_volume_window = self.ema2_period + self.ema1_period
        self.EMA_degree_tuple = (self.ema1_period, self.ema1_period*2, self.ema1_period*3, self.ema1_period*4) # значение волн ema для self.peacock_ tail_EMA_flag = True
        self.ma_key_name = 'EMA'
        if self.swirch_to_WMA_flag:
            self.ma_key_name = 'WMA'        
        self.default_tg_vars()
        self.init_some_params()
        self.init_main_file_variables()
        self.ema_settings()
        self.default_statistic_vars()
        self.init_keys()
        self.indicators_strategy_text_patterns = {
            '1': 'ema_crossover',
            '2': 'ema_crossover + trend_line',
            '3': 'ema_crossover + anty_trend_line',
            '4': 'ema_crossover + stoch_rsi_crossover',
            '5': 'ema_crossover + stoch_rsi_crossover + trend_line',
            '6': 'ema_crossover + stoch_rsi_overTrade',
            '7': 'ema_crossover + stoch_rsi_overTrade + trend_line',
            '8': 'ema_crossover + simple_random',
            '9': 'ema_crossover + trande_shift_random',
            '10': 'ema_crossover + long_shift_random',
            '11': 'ema_crossover + short_shift_random',
            '12': 'ema_crossover + vpvr_level',
            '13': 'volum_splash_indicator',
            '14': 'find_flats + volum_splash_indicator_2'
        }

        self.stop_loss_global_type_text_patterns = {
            '1': 'Trailing',
            '2': 'Fixed',      
        }

        self.stop_loss_ratio_mode_text_patterns = {
            '1': 'static',
            '2': 'volatility_period_20',
            '3': 'last_volatility',
            '4': 'last_candle_length',
            '5': 'last_candle_length/2',
            '6': 'last_minimum',
            '7': 'absolute_minimum',
            '8': 'vpvr_level',
        }

    def init_main_file_variables(self):
        self.symbol = None   
        self.vpvr_level_line = None
        self.candidate_symbols_list = [] 
        self.current_signal_val = None
        self.last_signal_val = None
        self.in_position = False 
        self.close_open_dispetcher = False 
        self.is_first_position = True  
        self.create_order_success_flag = False
        self.is_no_signal_counter = 0
        self.show_absent_signal_interval = 20
        self.cur_price = None
        self.enter_price = None
        self.last_enter_price = None
        self.qty = None
        self.price_precession = None
        self.price_precession_limit = None
        self.total_potential_losses = 0
        self.losses_counter = 0
        self.is_trailing_stop_start = False
        self.executed_qty = None
        self.stop_loss_ratio = None
        self.stop_loss_multiplier = None 
        self.trigger_multiplier = None
        self.next_trigger_price = None
        self.last_date = None
        self.cur_date = None
        self.is_time_to_show_done = False
        self.sl_risk_reward_multiplier, self.tp_risk_reward_multiplier = None, None

    def init_some_params(self):
        # ////////////////////// некоторые переменные:
        self.wait_candle_flag = True
        self.cur_klines_data = None
        self.was_change_leverage_true = False
        self.cur_martin_gale_counter = 0
        self.black_coins_list = self.default_black_coins_list
        #///////////////////////////////////////////////

    def ema_settings(self):
        self.interval = str(self.kline_time) + self.time_frame
        self.indicators_strategy_list_list = [
            [self.SOLI_DEO_GLORIA],
            ['ema_crossover'],
            ['ema_crossover', 'trend_line'],
            ['ema_crossover', 'anty_trend_line'],
            ['ema_crossover', 'stoch_rsi_crossover'],
            ['ema_crossover', 'stoch_rsi_crossover', 'trend_line'],
            ['ema_crossover', 'stoch_rsi_overTrade'],
            ['ema_crossover', 'stoch_rsi_overTrade', 'trend_line'],
            ['ema_crossover', 'simple_random'],
            ['ema_crossover', 'trande_shift_random'],
            ['ema_crossover', 'long_shift_random'],
            ['ema_crossover', 'short_shift_random'],
            ['ema_crossover', 'vpvr_level'],
            ['volum_splash_indicator'],
            ['find_flats', 'volum_splash_indicator_2']
        ]
        self.indicators_strategy_list = self.indicators_strategy_list_list[self.indicators_strategy_number]

    def default_statistic_vars(self):        
        self.win_los = 0 # результат последней сделки (в плюс или в минус)
        self.daily_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов
        self.total_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов

    # /////////// переменные... - суто по тех части: ///////////////////////
    def default_tg_vars(self):
        self.run_flag = False
        self.stop_bot_flag = False         
        self.block_acess_flag = False
        self.start_flag = False
        self.start_day_date = None
        self.block_acess_counter = 0
        self.seq_control_flag = False
        self.stop_redirect_flag = False 
        self.settings_redirect_flag = False
        self.last_message = None
        
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
        self.proxy_socks5_port = os.getenv("proxy_socks5_port", "")
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
        # self.proxy_socks5_port = proxy_socks5_port
        # self.proxy_username = proxy_username
        # self.proxy_password = proxy_password
