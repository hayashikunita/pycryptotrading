import os
import cx_Oracle
import pandas as pd
import datetime

def main():
 
    ##### (1)csvの読み込み
    # 第一引数＝csvファイルのパス
    # 第二引数＝encoding＝エンコーディング方式
    url = r'/Users/hayashikunita/python/csv_sql_convert/cryptodata.csv'
    df = pd.read_csv(url,encoding = 'utf-8')
    df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')
    ##### (2)DB接続のためのエンジン生成
    # 引数 max_identifier_length : テーブルの名前の限界値を指定。
    # (バージョン12.1以下のDBだと30が限界なので30で指定)
    from sqlalchemy import create_engine
    # engine = create_engine('oracle://[SchemaName]:[Password]@[Host/IPaddress]:[port]/[SID]',encoding='utf-8',max_identifier_length=30)
    engine = create_engine(f'sqlite:///cryptodata.sql',encoding='utf-8',max_identifier_length=30)
 
    ##### (3)DBへのINSERT準備
    # テーブル名を定義
    tbl_name='BITFINEX_BTCJPY'
    #カラム名も略語に置き換え


    # df.columns = [col.replace('time','time') for col in df.columns]
    # df.columns = [col.replace('open','open') for col in df.columns]
    # df.columns = [col.replace('high','high') for col in df.columns]
    # df.columns = [col.replace('low','low') for col in df.columns]
    # df.columns = [col.replace('close','close') for col in df.columns]
 
    ##### (4)DBへのINSERT処理
    # 引数con : engineを指定します
    # 引数name : テーブル名を指定します
    # 引数schema : スキーマ名を指定します
    df.to_sql(con=engine,name=tbl_name)
 
if __name__ == '__main__':
    main()