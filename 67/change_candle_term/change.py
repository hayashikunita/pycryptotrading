import os
import cx_Oracle
import pandas as pd
import datetime

url = r'/Users/hayashikunita/python/changecandleterm/cryptodata.csv'
df = pd.read_csv(url,encoding = 'utf-8')


df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
# "datetime"列をDataFrameのインデックスに設定
df = df.set_index("datetime")
pd.to_datetime(df.index, utc=True)

# 15m単位にリサンプリング
df = df.resample("15T").agg({
                "timestamp": "first", # 先頭
                "open":      "first", # 先頭
                "high":      "max",   # 最大
                "low":       "min",   # 最小
                "close":     "last",  # 末尾
                "volume":    "sum",   # 合計
            })


df.to_csv("cryptodata1.csv", encoding="utf-8")