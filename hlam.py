import pandas as pd
import matplotlib.pyplot as plt
from api_binance import BINANCE_API

def find_vpvr_levels(vpvr, num_levels=2):
    # Находим две самые объемные зоны VPVR
    top_vpvr_indexes = vpvr.nlargest(num_levels).index
    # Преобразуем индексы в список кортежей
    vpvr_levels = [(index.left, index.right) for index in top_vpvr_indexes]
    return vpvr_levels

def calculate_vpvr(data, bins=20):
    # Разбиваем данные на карманы (bins) и вычисляем объем в каждом кармане
    price_range = pd.cut(data['Close'], bins=bins)
    vpvr = data.groupby(price_range)['Volume'].sum()
    return vpvr

def plot_vpvr(vpvr):
    plt.barh(vpvr.index.astype(str), vpvr.values, height=0.5)
    plt.ylabel('Price Range')
    plt.xlabel('Volume')
    plt.title('Volume Profile Visible Range (VPVR)')
    plt.show()

def plot_cur_price(cur_price):
    plt.axhline(y=cur_price, color='green', linestyle='--', linewidth=2, label='Current Price')    
    plt.legend()
    plt.show()

# Пример использования:
data = BINANCE_API().get_klines('BTCUSDT', '1h', 20)

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Вычисляем VPVR
vpvr = calculate_vpvr(df)
# print(vpvr)

# Получаем текущую цену
cur_price = data["Close"].iloc[-1]
print(f"cur_price: {cur_price}")
vpvr_levels = find_vpvr_levels(vpvr)
print(vpvr_levels[0], vpvr_levels[1])
disposition = (vpvr_levels[0][0] <= cur_price <= vpvr_levels[0][1]) or (vpvr_levels[1][0] <= cur_price <= vpvr_levels[1][1])

if not disposition:
    f_lev = (vpvr_levels[0][0] + vpvr_levels[0][1])/2
    s_lev = (vpvr_levels[1][0] + vpvr_levels[1][1])/2
    print(f"f_lev_midl: {f_lev}")
    print(f"s_lev_midl: {s_lev}")
    nearest_lev = max(abs(cur_price - f_lev), abs(cur_price - s_lev)) - cur_price

    if nearest_lev - cur_price > 0:
        print("L")
    elif nearest_lev - cur_price < 0:
        print("S")
else:
    print("pass")

# Визуализируем результат с текущей ценой
plot_vpvr(vpvr)
# plot_cur_price(cur_price)
