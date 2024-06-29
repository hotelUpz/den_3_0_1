import numpy as np
from api_binance import BINANCE_API

def find_horizontal_flats(df, window=20, percentile=0.10, range_threshold=2):
    
    # Расчет скользящего стандартного отклонения цен закрытия
    df['RollingMean'] = df['Close'].rolling(window=window).mean()
    df['RollingStdDev'] = df['Close'].rolling(window=window).std()
    df.dropna(inplace=True)
    
    # Расчет перцентиля стандартного отклонения
    std_dev_threshold = df['RollingStdDev'].quantile(percentile)
    print(std_dev_threshold)
    
    # Определение флэта на основе порога стандартного отклонения и диапазона
    df['IsFlat'] = np.where(
        (df['RollingStdDev'] < std_dev_threshold) &
        ((df['Close'] <= df['RollingMean'] * (1 + range_threshold)) & (df['Close'] >= df['RollingMean'] * (1 - range_threshold))),
        1, 0
    )
    
    return df['IsFlat']

df = BINANCE_API().get_klines('BTCUSDT', '1m', 240)
print(find_horizontal_flats(df))