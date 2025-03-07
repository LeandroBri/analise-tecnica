import ccxt
import pandas as pd
import pandas_ta as ta

exchange = ccxt.binance()

# Lista de pares disponíveis
crypto_options = [
    {"label": "Kaito (KAITO/USDT)", "value": "KAITO/USDT"},
    {"label": "BNX (BNX/USDT)", "value": "BNX/USDT"},
    {"label": "Bera (BERA/USDT)", "value": "BERA/USDT"},
    {"label": "Wif (WIF/USDT)", "value": "WIF/USDT"},
    {"label": "Bitcoin (BTC/USDT)", "value": "BTC/USDT"},
    {"label": "Ethereum (ETH/USDT)", "value": "ETH/USDT"},
    {"label": "Solana (SOL/USDT)", "value": "SOL/USDT"},
    {"label": "Binance (BNB/USDT)", "value": "BNB/USDT"},
]

# Lista de timeframes disponíveis
timeframes = [
    {"label": "1 Minuto", "value": "1m"},
    {"label": "5 Minutos", "value": "5m"},
    {"label": "15 Minutos", "value": "15m"},
    {"label": "1 Hora", "value": "1h"},
    {"label": "1 Dia", "value": "1d"},
]

# Intervalos de atualização
update_intervals = [
    {"label": "2s", "value": 2000},
    {"label": "5s", "value": 5000},
    {"label": "10s", "value": 10000},
    {"label": "30s", "value": 30000},
    {"label": "1 min", "value": 60000},
]


def get_ohlcv(pair, timeframe):
    ohlcv = exchange.fetch_ohlcv(pair.replace("/", ""), timeframe=timeframe, limit=50)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def calculate_macd(df):
    macd_data = df.ta.macd(close="close", fast=12, slow=26, signal=9)
    df["MACD"] = macd_data["MACD_12_26_9"]
    df["Signal"] = macd_data["MACDs_12_26_9"]
    return df

def calculate_indicators(df, indicators):
    if "RSI" in indicators:
        df["RSI"] = df.ta.rsi(close="close", length=14)
    if "EMA" in indicators:
        df["EMA"] = df.ta.ema(close="close", length=14)
    if "SMA" in indicators:
        df["SMA"] = df.ta.sma(close="close", length=14)
    if "BB" in indicators:
        bb_data = df.ta.bbands(close="close", length=20)
        df["BB_Middle"] = bb_data["BBM_20_2.0"]
        df["BB_Upper"] = bb_data["BBU_20_2.0"]
        df["BB_Lower"] = bb_data["BBL_20_2.0"]
    return df



