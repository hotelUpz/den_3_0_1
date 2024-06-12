import pandas as pd
from api_binance import BINANCE_API

def calculate_vpvr(data, min_bins=10, max_bins=50):
    # Вычисляем динамическое количество корзин (bins) на основе количества свечей
    num_candles = len(data)
    bins = min(max(min_bins, num_candles // 10), max_bins)
    
    # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
    price_range = pd.cut(data['Close'], bins=bins)
    vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
    return vpvr

def find_vpvr_levels(vpvr, num_levels=2):
    # Поиск наиболее объемных зон VPVR
    top_vpvr_indexes = vpvr.nlargest(num_levels).index
    vpvr_levels = [(index.left, index.right) for index in top_vpvr_indexes]
    return vpvr_levels

def immediate_vpvr_level(cur_price, vpvr_levels):
    print(cur_price)
    # print(vpvr_levels)
    disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or \
                  (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])
    if not disposition:
        f_lev_midl = (vpvr_levels[0][0] + vpvr_levels[0][1])/2
        s_lev_midl = (vpvr_levels[1][0] + vpvr_levels[1][1])/2
        immediate_level = min(abs(cur_price - f_lev_midl), abs(cur_price - s_lev_midl)) + cur_price
        # print(immediate_level)
        if immediate_level > cur_price:
            return "L", immediate_level
        elif immediate_level < cur_price:
            return "S", immediate_level
    return

# Получение и обработка данных
df = BINANCE_API().get_klines('INJUSDT', '1h', 240)
vpvr = calculate_vpvr(df)

# Определение текущей цены и уровней VPVR
cur_price = df["Close"].iloc[-1]
vpvr_levels = find_vpvr_levels(vpvr)

# Определение текущей позиции
immediate_vpvr_level_val = immediate_vpvr_level(cur_price, vpvr_levels)
print("immediate_vpvr_level:", immediate_vpvr_level_val)
