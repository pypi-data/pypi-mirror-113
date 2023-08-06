# coding:utf-8
import datetime
import akshare as ak
import pymongo
import pandas as pd
from xhdata.Util.MongoClient import *
from xhdata.Util.Akshare import my_stock_zh_index_daily_em

from QUANTAXIS.QAUtil import (
    QA_util_log_info,
    QA_util_to_json_from_pandas,
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_to_json_from_pandas,
    trade_date_sse
)


def now_time():
    return str(QA_util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + \
           ' 17:00:00' if datetime.datetime.now().hour < 15 else str(QA_util_get_real_date(
        str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'


def save_stock_list(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    """save stock_list

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    client.drop_collection('stock_list')
    coll = client.stock_list
    coll.create_index('code')

    try:
        # 🛠todo 这个应该是第一个任务 JOB01， 先更新股票列表！！
        QA_util_log_info(
            '##JOB: Now Saving STOCK_LIST ====',
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=5000
        )

        big_df = pd.DataFrame()
        stock_sh = ak.stock_info_sh_name_code(indicator="主板A股")
        stock_sh = stock_sh[["SECURITY_CODE_A", "SECURITY_ABBR_A", "LISTING_DATE"]]
        stock_sh.columns = ["code", "name", "start_date"]

        stock_sz = ak.stock_info_sz_name_code(indicator="A股列表")
        stock_sz = stock_sz[["A股代码", "A股简称", "A股上市日期"]]
        stock_sz.columns = ["code", "name", "start_date"]

        stock_kcb = ak.stock_info_sh_name_code(indicator="科创板")
        stock_kcb = stock_kcb[["SECURITY_CODE_A", "SECURITY_ABBR_A", "LISTING_DATE"]]
        stock_kcb.columns = ["code", "name", "start_date"]

        stock_info_sz_delist_df = ak.stock_info_sz_delist(indicator="终止上市公司")
        stock_info_sz_delist_df = stock_info_sz_delist_df[["证券代码", "证券简称", "上市日期"]]
        stock_info_sz_delist_df.columns = ["code", "name", "start_date"]

        stock_info_sh_delist_df = ak.stock_info_sh_delist(indicator="终止上市公司")
        stock_info_sh_delist_df = stock_info_sh_delist_df[["SECURITY_CODE_A", "SECURITY_ABBR_A", "LISTING_DATE"]]
        stock_info_sh_delist_df.columns = ["code", "name", "start_date"]

        big_df = big_df.append(stock_sh, ignore_index=True)
        big_df = big_df.append(stock_sz, ignore_index=True)
        big_df = big_df.append(stock_kcb, ignore_index=True)
        big_df = big_df.append(stock_info_sz_delist_df, ignore_index=True)
        big_df = big_df.append(stock_info_sh_delist_df, ignore_index=True)
        big_df.columns = ["code", "name", "start_date"]

        #stock_list_from_tdx = ak.stock_info_a_code_name()
        pandas_data = QA_util_to_json_from_pandas(big_df)
        coll.insert_many(pandas_data)
        QA_util_log_info(
            "完成股票列表获取",
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=10000
        )
    except Exception as e:
        QA_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.QA_SU_save_stock_list exception!")

        pass


def save_stock_day(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    '''
     save stock_day
    保存日线数据
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    stock_list = ak.stock_info_a_code_name().code.unique().tolist()
    coll_stock_day = client.stock_day
    coll_stock_day.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date",
          pymongo.ASCENDING)]
    )
    err = []

    def __get_stock_day(code, start_date, end_date):
        stock_zh_a_hist_df = ak.stock_zh_a_hist(
            str(code),
            start_date,
            end_date
        )
        stock_zh_a_hist_df['code'] = code
        stock_zh_a_hist_df.columns = ["date", "open", "close", "high", "low", "vol", "amount", "amplitude",
                                      "change_pct", "change_amount", "turnover_ratio", "code"]
        return stock_zh_a_hist_df

    def __saving_work(code, coll_stock_day):
        try:
            QA_util_log_info(
                '##JOB: Now Saving STOCK_DAY==== {}'.format(str(code)),
                ui_log
            )

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll_stock_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                QA_util_log_info(
                    'UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    coll_stock_day.insert_many(
                        QA_util_to_json_from_pandas(
                            __get_stock_day(
                                str(code),
                                QA_util_get_next_day(start_date),
                                end_date
                            )
                        )
                    )

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '1990-01-01'
                QA_util_log_info(
                    'UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    coll_stock_day.insert_many(
                        QA_util_to_json_from_pandas(
                            __get_stock_day(
                                str(code),
                                start_date,
                                end_date
                            )
                        )
                    )
        except Exception as error0:
            print(error0)
            err.append(str(code))

    for item in range(len(stock_list)):
        QA_util_log_info('The {} of Total {}'.format(item, len(stock_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {} {}'.format(
            str(float(item / len(stock_list) * 100))[0:4] + '%',
            ui_log
        )
        intProgressToLog = int(float(item / len(stock_list) * 100))
        QA_util_log_info(
            strProgressToLog,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intProgressToLog
        )

        __saving_work(stock_list[item], coll_stock_day)

    if len(err) < 1:
        QA_util_log_info('SUCCESS save stock day ^_^', ui_log)
    else:
        QA_util_log_info('ERROR CODE \n ', ui_log)
        QA_util_log_info(err, ui_log)


def save_stock_fq_factor(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    '''
     save stock_fq_factor
    保存股票复权因子
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    stock_list = ak.stock_info_a_code_name().code.unique().tolist()
    coll = client.stock_fq_factor
    coll.create_index('code')
    err = []

    def __saving_work(code, coll):
        QA_util_log_info(
            '##JOB: Now Saving stock_fq_factor ==== {}'.format(str(code)),
            ui_log=ui_log
        )
        try:
            coll.delete_many({'code': code})

            qfq_factor_df = ak.stock_zh_a_daily(
                symbol=str("sh" + code if code[0] == "6" else "sz" + code), adjust="qfq-factor")
            qfq_factor_df.columns = ["date", "factor"]
            qfq_factor_df['code'] = code
            qfq_factor_df['adjust'] = 'qfq'

            hfq_factor_df = ak.stock_zh_a_daily(
                symbol=str("sh" + code if code[0] == "6" else "sz" + code), adjust="hfq-factor")
            hfq_factor_df.columns = ["date", "factor"]
            hfq_factor_df['code'] = code
            hfq_factor_df['adjust'] = 'hfq'

            coll.insert_many(QA_util_to_json_from_pandas(qfq_factor_df))
            coll.insert_many(QA_util_to_json_from_pandas(hfq_factor_df))
        except:
            err.append(str(code))

    for i_ in range(len(stock_list)):
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(stock_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(stock_list) * 10000.0))
        QA_util_log_info('The {} of Total {}'.format(i_, len(stock_list)))
        QA_util_log_info(
            strLogProgress,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )

        __saving_work(stock_list[i_], coll)

    if len(err) < 1:
        QA_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


# ************基金************************* #
def save_fund_list(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    """save stock_list

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    client.drop_collection('fund_list')
    coll = client.fund_list
    coll.create_index('code')

    try:
        QA_util_log_info(
            '##JOB: Now Saving FUND_LIST ====',
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=5000
        )
        fund_em_fund_name = ak.fund_em_fund_name()
        fund_em_fund_name.columns = ["code", "pinyin", "name", "type", "pinyin_full"]
        pandas_data = QA_util_to_json_from_pandas(fund_em_fund_name)
        coll.insert_many(pandas_data)
        QA_util_log_info(
            "完成基金列表获取",
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=10000
        )
    except Exception as e:
        QA_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.save_fund_list exception!")

        pass


def save_fund_day(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    '''
     save index_day
    保存股票复权因子
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    fund_list = list(client.fund_list.find())
    coll = client.fund_day
    coll.create_index('code')
    err = []

    def __saving_work(code, coll):
        try:
            QA_util_log_info(
                '##JOB: Now Saving fund_day==== {}'.format(str(code)),
                ui_log
            )

            def __get_fund_day(_code, _start_date, _end_date):
                stock_zh_index_daily_em = my_stock_zh_index_daily_em(
                    str("sh" + _code if _code[0] == "5" else "sz" + _code),
                    _start_date,
                    _end_date
                )
                stock_zh_index_daily_em['code'] = code
                return stock_zh_index_daily_em

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                QA_util_log_info(
                    'UPDATE_FUND_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            __get_fund_day(
                                str(code),
                                QA_util_get_next_day(start_date),
                                end_date
                            )
                        )
                    )

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '1990-01-01'
                QA_util_log_info(
                    'UPDATE_FUND_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            __get_fund_day(
                                str(code),
                                start_date,
                                end_date
                            )
                        )
                    )
        except Exception as error0:
            print(error0)
            err.append(str(code))

    for i_ in range(len(fund_list)):
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(fund_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(fund_list) * 10000.0))
        QA_util_log_info('The {} of Total {}'.format(i_, len(fund_list)))
        QA_util_log_info(
            strLogProgress,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )
        # sz: 15 16 18
        # sh: 5
        if fund_list[i_]['code'][0:2] in ['15', '16', '18']:
            __saving_work(fund_list[i_]['code'], coll)

        if fund_list[i_]['code'][0] in ['5']:
            __saving_work(fund_list[i_]['code'], coll)

    if len(err) < 1:
        QA_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


# ************指数************************* #
def save_index_list(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    """save stock_list

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    client.drop_collection('index_list')
    coll = client.index_list
    coll.create_index('code')

    try:
        QA_util_log_info(
            '##JOB: Now Saving INDEX_LIST ====',
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=5000
        )
        index_stock_info_df = ak.index_stock_info()
        index_stock_info_df.columns = ["code", "name", "date"]
        pandas_data = QA_util_to_json_from_pandas(index_stock_info_df)
        coll.insert_many(pandas_data)
        QA_util_log_info(
            "完成指数列表获取",
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=10000
        )
    except Exception as e:
        QA_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.QA_SU_save_stock_list exception!")
        pass


def save_index_day(client=MongoClient().client.akshare, ui_log=None, ui_progress=None):
    '''
     save index_day
    保存股票复权因子
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    index_list = ak.index_stock_info().index_code.unique().tolist()
    coll = client.index_day
    coll.create_index('code')
    err = []

    def __saving_work(code, coll):
        try:
            QA_util_log_info(
                '##JOB: Now Saving index_day==== {}'.format(str(code)),
                ui_log
            )

            def __get_index_day(_code, _start_date, _end_date):
                stock_zh_index_daily_em = my_stock_zh_index_daily_em(
                    str("sh" + _code if _code[0] == "0" else "sz" + _code),
                    _start_date,
                    _end_date
                )
                stock_zh_index_daily_em['code'] = code
                return stock_zh_index_daily_em

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                QA_util_log_info(
                    'UPDATE_INDEX_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            __get_index_day(
                                str(code),
                                QA_util_get_next_day(start_date),
                                end_date
                            )
                        )
                    )

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '1990-01-01'
                QA_util_log_info(
                    'UPDATE_INDEX_DAY \n Trying updating {} from {} to {}'
                        .format(code,
                                start_date,
                                end_date),
                    ui_log
                )
                if start_date != end_date:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            __get_index_day(
                                str(code),
                                start_date,
                                end_date
                            )
                        )
                    )
        except Exception as error0:
            print(error0)
            err.append(str(code))

    for i_ in range(len(index_list)):
        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(index_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(index_list) * 10000.0))
        QA_util_log_info('The {} of Total {}'.format(i_, len(index_list)))
        QA_util_log_info(
            strLogProgress,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )

        __saving_work(index_list[i_], coll)

    if len(err) < 1:
        QA_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)



