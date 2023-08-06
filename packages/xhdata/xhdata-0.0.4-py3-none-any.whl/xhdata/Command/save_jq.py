# coding:utf-8
import datetime
import akshare as ak
import pymongo

from xhdata.Util.MongoClient import *

from QUANTAXIS.QAUtil import (
    QA_util_log_info,
    QA_util_to_json_from_pandas,
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_to_json_from_pandas,
    trade_date_sse
)

import jqdatasdk
jqdatasdk.auth(os.environ.get("JQUSERNAME", ''), os.environ.get("JQUSERPASSWD", ''))


def now_time():
    """
    1. 当前日期如果是交易日且当前时间在 17:00 之前，默认行情取到上个交易日收盘
    2. 当前日期如果是交易日且当前时间在 17:00 之后，默认行情取到当前交易日收盘
    """
    return (str(
        QA_util_get_real_date(
            str(datetime.date.today() - datetime.timedelta(days=1)),
            trade_date_sse,
            -1,
        )) + " 17:00:00" if datetime.datetime.now().hour < TRADE_HOUR_END else str(
            QA_util_get_real_date(
                str(datetime.date.today()), trade_date_sse, -1)) + " 17:00:00")


def save_all_securities(client=MongoClient().client.jq, ui_log=None, ui_progress=None):
    """save all_securities

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    client.drop_collection('all_securities')
    coll = client.all_securities
    coll.create_index('code')

    try:
        QA_util_log_info(
            '##JOB: Now Saving all_securities ====',
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=5000
        )
        sec = ['stock', 'fund', 'index', 'futures', 'etf', 'lof', 'fja', 'fjb', 'open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund']
        get_all_securities = jqdatasdk.get_all_securities(sec)
        get_all_securities = get_all_securities.reset_index().rename(columns={
            "index": "code",
        })
        pandas_data = QA_util_to_json_from_pandas(get_all_securities)
        coll.insert_many(pandas_data)
        QA_util_log_info(
            "完成所有标的列表获取",
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=10000
        )
    except Exception as e:
        QA_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.all_securities exception!")

        pass

