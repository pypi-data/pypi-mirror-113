#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
import pandas as pd
import numpy as np
import akshare as ak
import time
import datetime
from xhdata.Util.MongoClient import *
from xhdata.Util.TransCode import *
from xhdata.Data.stock import (
    stock_zh_a_daily,
    stock_zh_index_daily,
    stock_zh_fund_daily
)


def get_price(
        security,
        start_date=None,
        end_date=None,
        frequency='daily',
        fields=None,
        skip_paused=False,
        fq='pre',
        count=None
) -> pd.DataFrame:
    """
    获取一支或者多只股票的行情数据, 按天或者按分钟
    :param fq:  复权选项:
    :param skip_paused: 默认为 False 是否跳过不交易日期(包括停牌, 未上市或者退市后的日期). 如果不跳过, 停牌时会使用停牌前的数据填充(具体请看SecurityUnitData的paused属性), 上市前或者退市后数据都为 nan,
    :param fields: 字符串list, 选择要获取的行情数据字段, 默认是None(表示['open', 'close', 'high', 'low', 'volume', 'money']这几个标准字段), 支持SecurityUnitData里面的所有基本属性,，包含：['open', ' close', 'low', 'high', 'volume', 'money', 'factor', 'high_limit',' low_limit', 'avg', ' pre_close', 'paused']
    :param frequency: 单位时间长度, 几天或者几分钟, 现在支持'Xd','Xm', 'daily'(等同于'1d'), 'minute'(等同于'1m'), X是一个正整数, 分别表示X天和X分钟(不论是按天还是按分钟回测都能拿到这两种单位的数据), 注意, 当X > 1时, fields只支持['open', 'close', 'high', 'low', 'volume', 'money']这几个标准字段. 默认值是daily
    :param end_date: 结束时间
    :param count: 与 start_date 二选一，不可同时使用. 数量, 返回的结果集的行数, 即表示获取 end_date 之前几个 frequency 的数据
    :param start_date: 开始时间
    :param security:一支股票代码或者一个股票代码的list
    :return:
    """

    def get_data(symbol):
        _variety = code_to_variety(symbol)
        if _variety == Variety.STOCK:
            if frequency == 'daily':
                return stock_zh_a_daily(symbol=symbol,
                                        start_date=start_date,
                                        end_date=end_date,
                                        fields=fields,
                                        adjust=fq,
                                        count=count)
        elif _variety == Variety.INDEX:
            return stock_zh_index_daily(symbol=symbol,
                                        start_date=start_date,
                                        end_date=end_date,
                                        fields=fields,
                                        adjust=fq,
                                        count=count)
        elif _variety == Variety.FUND:
            return stock_zh_fund_daily(symbol=symbol,
                                       start_date=start_date,
                                       end_date=end_date,
                                       fields=fields,
                                       adjust=fq,
                                       count=count)
        elif _variety == Variety.FUTURES:
            pass
        else:
            pass

    # 判断security 股票/基金/指数/期货
    big_df = pd.DataFrame()
    if isinstance(security, str):
        big_df = big_df.append(get_data(security))
    elif isinstance(security, list):
        for _security in security:
            big_df = big_df.append(get_data(_security), ignore_index=True)
            big_df.index = big_df.index.map(big_df['code'])
    else:
        return big_df

    return big_df


def get_all_securities(
        types=['stock'],
        date=None
) -> pd.DataFrame:
    """
    获取平台支持的所有股票、基金、指数、期货信息
    :parameter
        types: list: 用来过滤securities的类型, list元素可选: 'stock', 'fund', 'index', 'futures', 'etf', 'lof', 'fja', 'fjb', 'open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund'。 types为空时返回所有股票, 不包括基金,指数和期货
        date: 日期, 一个字符串或者 [datetime.datetime]/[datetime.date] 对象, 用于获取某日期还在上市的股票信息. 默认值为 None, 表示获取所有日期的股票信息
    :return:  pandas.DataFrame
    """
    try:
        client = MongoClient().client.jq
        coll = client.all_securities
        condition = {}

        if types is not None:
            condition['type'] = {"$in": types}
        if date is not None:
            strptime = time.strptime(date, "%Y-%m-%d")
            mktime = int(time.mktime(strptime) * 1000)
            condition['end_date'] = {"$lt": mktime}

        res = coll.find(condition)
        df = pd.DataFrame(list(res))
        if df.empty:
            return df
        df = df[["code", "display_name", "name", "start_date", "end_date", "type"]]
        df["start_date"] = df["start_date"].map(lambda x: time.strftime("%Y-%m-%d", time.localtime(x/1000)))
        df["end_date"] = df["end_date"].map(lambda x: time.strftime("%Y-%m-%d", time.localtime(x / 1000)))
        df.index = df.index.map(df['code'])
        return df


        big_df = pd.DataFrame()
        stock_list = pd.DataFrame(list(client.stock_list.find()))
        stock_list = stock_list[["code", "name"]]
        stock_list['type'] = 'stock'

        fund_list = pd.DataFrame(list(client.fund_list.find()))
        fund_list = fund_list[["code", "name"]]
        fund_list['type'] = 'fund'

        index_list = pd.DataFrame(list(client.index_list.find()))
        index_list = index_list[["code", "name"]]
        index_list['type'] = 'index'

        big_df = big_df.append(stock_list, ignore_index=True)
        big_df = big_df.append(fund_list, ignore_index=True)
        big_df = big_df.append(index_list, ignore_index=True)

        return big_df
    except Exception as err:
        print(err)



