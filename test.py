import pandas as pd
import matplotlib.pyplot as plt
from api_binance import BINANCE_API


def calculate_vpvr(data, min_bins=10, max_bins=50):
    # Вычисляем динамическое количество корзин (bins) на основе количества свечей
    num_candles = 240
    bins = min(max(min_bins, num_candles // 10), max_bins)
    data = data.tail(240)
    # print(data)        
    # Разбиваем данные на корзины (bins) и вычисляем объем в каждой корзине
    price_range = pd.cut(data['Close'], bins=bins)
    vpvr = data.groupby(price_range, observed=False)['Volume'].sum()
    return vpvr

def find_vpvr_levels(vpvr, num_levels=2):
    # Поиск наиболее объемных зон VPVR
    top_vpvr_indexes = vpvr.nlargest(num_levels).index
    vpvr_levels = [(index.left, index.right, (index.left + index.right)/2, vpvr[index]) for index in top_vpvr_indexes]
    return vpvr_levels

def immediate_vpvr_level_defender(cur_price, vpvr_levels):
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

def plot_vpvr(vpvr):
    plt.barh(vpvr.index.astype(str), vpvr.values, height=0.5)
    plt.ylabel('Price Range')
    plt.xlabel('Volume')
    plt.title('Volume Profile Visible Range (VPVR)')
    plt.show()

df = BINANCE_API().get_klines('BTCUSDT', '5m', 20)
vpvr = calculate_vpvr(df)
cur_price = df["Close"].iloc[-1]
print(f"cur_price: {cur_price}")

immediate_vpvr_level_defender_val = None
vpvr = calculate_vpvr(df)                       
vpvr_levels = find_vpvr_levels(vpvr)
immediate_vpvr_level_defender_val = immediate_vpvr_level_defender(cur_price, vpvr_levels)

if immediate_vpvr_level_defender_val:
    if immediate_vpvr_level_defender_val[0] == 'L':
        print("vpr indicator: Long")
    elif immediate_vpvr_level_defender_val[0] == 'S':
        print("vpr indicator: Short")
    print(f"level: {immediate_vpvr_level_defender_val[1]}")

plot_vpvr(vpvr)