#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import demjson
import pandas as pd


def my_stock_zh_index_daily_em(
        symbol: str = "sh000913",
        start_date: str = "19900101",
        end_date: str = "20220101",
) -> pd.DataFrame:
    """
    东方财富股票指数数据
    http://quote.eastmoney.com/center/hszs.html
    :param end_date:
    :param start_date:
    :param symbol: 带市场标识的指数代码
    :type symbol: str
    :return: 指数数据
    :rtype: pandas.DataFrame
    """
    start_date = start_date.replace("-", "")
    end_date = end_date.replace("-", "")
    market_map = {"sz": "0", "sh": "1"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "cb": "jQuery1124033485574041163946_1596700547000",
        "secid": f"{market_map[symbol[:2]]}.{symbol[2:]}",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "klt": "101",  # 日频率
        "fqt": "0",
        "beg": start_date,
        "end": end_date,
        "_": "1596700547039",
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = demjson.decode(data_text[data_text.find("{"):-2])
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = ["date", "open", "close", "high", "low", "volume", "amount", "_"]
    temp_df = temp_df[["date", "open", "close", "high", "low", "volume", "amount"]]
    temp_df = temp_df.astype({
        "open": float,
        "close": float,
        "high": float,
        "low": float,
        "volume": float,
        "amount": float,
    })
    return temp_df




