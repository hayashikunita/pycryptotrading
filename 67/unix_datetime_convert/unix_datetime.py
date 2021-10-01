import os
import cx_Oracle
import pandas as pd
import datetime

def main():
 
    ##### (1)csvの読み込み
    # 第一引数＝csvファイルのパス
    # 第二引数＝encoding＝エンコーディング方式
    url = r'/Users/hayashikunita/python/Unix_datetime_convert/cryptodata.csv'
    df = pd.read_csv(url,encoding = 'utf-8')
    df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')

    df.to_csv("cryptodata1.csv", encoding="utf-8")


if __name__ == '__main__':
    main()