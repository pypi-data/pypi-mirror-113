#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from multiprocessing import Lock
import pymongo


class EXCHANGE:
    XSHG = 'XSHG'
    SSE = 'XSHG'
    SH = 'XSHG'
    XSHE = 'XSHE'
    SZ = 'XSHE'
    SZE = 'XSHE'


class Variety:
    STOCK = 'STOCK'
    FUND = 'FUND'
    INDEX = 'INDEX'
    FUTURES = 'FUTURES'


def normalize_code(symbol, pre_close=None):
    """
    归一化证券代码

    :param pre_close:
    :param symbol:如000001
    :return 证券代码的全称 如000001.XSHE
    """
    if not isinstance(symbol, str):
        return symbol

    if symbol.startswith('sz') and (len(symbol) == 8):
        ret_normalize_code = '{}.{}'.format(symbol[2:8], EXCHANGE.SZ)
    elif symbol.startswith('sh') and (len(symbol) == 8):
        ret_normalize_code = '{}.{}'.format(symbol[2:8], EXCHANGE.SH)
    elif symbol.startswith('00') and (len(symbol) == 6):
        if (pre_close is not None) and (pre_close > 2000):
            # 推断是上证指数
            ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SH)
        else:
            ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SZ)
    elif ((symbol.startswith('399') or symbol.startswith('159') or
           symbol.startswith('150')) and (len(symbol) == 6)):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SH)
    elif ((len(symbol) == 6) and (symbol.startswith('399') or
                                  symbol.startswith('159') or symbol.startswith('150') or
                                  symbol.startswith('16') or symbol.startswith('184801') or
                                  symbol.startswith('201872'))):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SZ)
    elif ((len(symbol) == 6) and (symbol.startswith('50') or
                                  symbol.startswith('51') or symbol.startswith('60') or
                                  symbol.startswith('688') or symbol.startswith('900') or
                                  (symbol == '751038'))):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SH)
    elif ((len(symbol) == 6) and (symbol[:3] in ['000', '001', '002',
                                                 '200', '300'])):
        ret_normalize_code = '{}.{}'.format(symbol, EXCHANGE.SZ)
    else:
        print(symbol)
        ret_normalize_code = symbol

    return ret_normalize_code


def code_to_variety(symbol):
    """
    根据symbol判断交易品种 股票stock/基金fund/指数index/期货futures
    如果是6位纯数字，默认当作股票
    :param symbol: 000001 000001.XSHE  000001.SZ
    :param pre_close:
    :return:
    """
    if len(symbol) == 6 and (symbol.startswith('0') or symbol.startswith('6')):
        return Variety.STOCK
    elif symbol.startswith('00') and symbol.startswith(EXCHANGE.XSHG, 7, 11):
        return Variety.INDEX
    elif symbol.startswith('399') and symbol.startswith(EXCHANGE.XSHE, 7, 11):
        return Variety.INDEX
    elif symbol.startswith('15') or symbol.startswith('5'):
        return Variety.FUND
    elif symbol.startswith('OF', 7, 9):
        return Variety.FUND
    else:
        return Variety.STOCK



