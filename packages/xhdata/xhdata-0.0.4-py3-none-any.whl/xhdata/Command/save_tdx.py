import datetime
import pymongo


from xhdata.Util.MongoClient import *

from QUANTAXIS.QAFetch.QATdx import (
    QA_fetch_get_option_day,
    QA_fetch_get_option_min,
    QA_fetch_get_index_day,
    QA_fetch_get_index_min,
    QA_fetch_get_stock_day,
    QA_fetch_get_stock_info,
    QA_fetch_get_stock_list,
    QA_fetch_get_future_list,
    QA_fetch_get_index_list,
    QA_fetch_get_future_day,
    QA_fetch_get_future_min,
    QA_fetch_get_stock_min,
    QA_fetch_get_stock_transaction,
    QA_fetch_get_index_transaction,
    QA_fetch_get_stock_xdxr,
    QA_fetch_get_bond_day,
    QA_fetch_get_bond_list,
    QA_fetch_get_bond_min,
    select_best_ip,
    QA_fetch_get_hkstock_day,
    QA_fetch_get_hkstock_list,
    QA_fetch_get_hkstock_min,
    QA_fetch_get_usstock_list,
    QA_fetch_get_usstock_day,
    QA_fetch_get_usstock_min,
)

from QUANTAXIS.QAUtil import (
    QA_util_log_info,
    QA_util_to_json_from_pandas,
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_to_json_from_pandas,
    trade_date_sse
)

from QUANTAXIS.QAData.data_fq import _QA_data_stock_to_fq
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day


def now_time():
    return str(QA_util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + \
           ' 17:00:00' if datetime.datetime.now().hour < 15 else str(QA_util_get_real_date(
        str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'


def save_stock_list(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
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
        stock_list_from_tdx = QA_fetch_get_stock_list()
        pandas_data = QA_util_to_json_from_pandas(stock_list_from_tdx)
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


def save_stock_info(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    """save stock_info

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    client.drop_collection('stock_info')
    stock_list = QA_fetch_get_stock_list().code.unique().tolist()
    coll = client.stock_info
    coll.create_index('code')
    err = []

    def __saving_work(code, coll):
        QA_util_log_info(
            '##JOB: Now Saving STOCK INFO ==== {}'.format(str(code)),
            ui_log=ui_log
        )
        try:
            coll.insert_many(
                QA_util_to_json_from_pandas(QA_fetch_get_stock_info(str(code)))
            )

        except:
            err.append(str(code))

    for i_ in range(len(stock_list)):
        # __saving_work('000001')

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


def save_stock_day(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    '''
     save stock_day
    保存日线数据
    :param client:
    :param ui_log:  给GUI qt 界面使用
    :param ui_progress: 给GUI qt 界面使用
    :param ui_progress_int_value: 给GUI qt 界面使用
    '''
    stock_list = QA_fetch_get_stock_list().code.unique().tolist()
    coll_stock_day = client.stock_day
    coll_stock_day.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []

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
                            QA_fetch_get_stock_day(
                                str(code),
                                QA_util_get_next_day(start_date),
                                end_date,
                                '00'
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
                            QA_fetch_get_stock_day(
                                str(code),
                                start_date,
                                end_date,
                                '00'
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


def save_stock_xdxr(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    """[summary]

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    stock_list = QA_fetch_get_stock_list().code.unique().tolist()
    # client.drop_collection('stock_xdxr')

    try:
        coll = client.stock_xdxr
        coll.create_index(
            [('code',
              pymongo.ASCENDING),
             ('date',
              pymongo.ASCENDING)],
            unique=True
        )
        coll_adj = client.stock_adj
        coll_adj.create_index(
            [('code',
                pymongo.ASCENDING),
                ('date',
                pymongo.ASCENDING)],
            unique=True
        )
    except:
        client.drop_collection('stock_xdxr')
        coll = client.stock_xdxr
        coll.create_index(
            [('code',
              pymongo.ASCENDING),
             ('date',
              pymongo.ASCENDING)],
            unique=True
        )
        client.drop_collection('stock_adj')
        coll_adj = client.stock_adj
        coll_adj.create_index(
            [('code',
                pymongo.ASCENDING),
                ('date',
                pymongo.ASCENDING)],
            unique=True
        )

    err = []

    def __saving_work(code, coll):
        QA_util_log_info(
            '##JOB: Now Saving XDXR INFO ==== {}'.format(str(code)),
            ui_log=ui_log
        )
        try:

            xdxr  = QA_fetch_get_stock_xdxr(str(code))
            try:
                coll.insert_many(
                    QA_util_to_json_from_pandas(xdxr),
                    ordered=False
                )
            except:
                pass
            try:
                data = QA_fetch_stock_day(str(code), '1990-01-01',str(datetime.date.today()), 'pd')
                qfq = _QA_data_stock_to_fq(data, xdxr, 'qfq')
                qfq = qfq.assign(date=qfq.date.apply(lambda x: str(x)[0:10]))
                adjdata = QA_util_to_json_from_pandas(qfq.loc[:, ['date','code', 'adj']])
                coll_adj.delete_many({'code': code})
                #print(adjdata)
                coll_adj.insert_many(adjdata)


            except Exception as e:
                print(e)


        except Exception as e:
            print(e)

            err.append(str(code))

    for i_ in range(len(stock_list)):
        QA_util_log_info(
            'The {} of Total {}'.format(i_,
                                        len(stock_list)),
            ui_log=ui_log
        )
        strLogInfo = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(stock_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(stock_list) * 100))
        QA_util_log_info(
            strLogInfo,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )
        __saving_work(stock_list[i_], coll)


def save_etf_list(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    """save etf_list

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    try:
        QA_util_log_info(
            '##JOB: Now Saving ETF_LIST ====',
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=5000
        )
        etf_list_from_tdx = QA_fetch_get_stock_list(type_="etf")
        pandas_data = QA_util_to_json_from_pandas(etf_list_from_tdx)

        if len(pandas_data) > 0:
            # 获取到数据后才进行drop collection 操作
            client.drop_collection('etf_list')
            coll = client.etf_list
            coll.create_index('code')
            coll.insert_many(pandas_data)
        QA_util_log_info(
            "完成ETF列表获取",
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=10000
        )
    except Exception as e:
        QA_util_log_info(e, ui_log=ui_log)
        print(" Error save_tdx.QA_SU_save_etf_list exception!")
        pass


def save_etf_day(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    """save etf_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = QA_fetch_get_stock_list('etf')
    coll = client.index_day
    coll.create_index(
        [('code',
          pymongo.ASCENDING),
         ('date_stamp',
          pymongo.ASCENDING)]
    )
    err = []

    def __saving_work(code, coll):

        try:

            ref_ = coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']

                QA_util_log_info(
                    '##JOB: Now Saving ETF_DAY==== \n Trying updating {} from {} to {}'
                        .format(code,
                                start_time,
                                end_time),
                    ui_log=ui_log
                )

                if start_time != end_time:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                QA_util_get_next_day(start_time),
                                end_time
                            )
                        )
                    )
            else:
                start_time = '1990-01-01'
                QA_util_log_info(
                    '##JOB06 Now Saving ETF_DAY==== \n Trying updating {} from {} to {}'
                        .format(code,
                                start_time,
                                end_time),
                    ui_log=ui_log
                )

                if start_time != end_time:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                start_time,
                                end_time
                            )
                        )
                    )
        except:
            err.append(str(code))

    for i_ in range(len(__index_list)):
        # __saving_work('000001')
        QA_util_log_info(
            'The {} of Total {}'.format(i_,
                                        len(__index_list)),
            ui_log=ui_log
        )

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(__index_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(__index_list) * 10000.0))
        QA_util_log_info(
            strLogProgress,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )

        __saving_work(__index_list.index[i_][0], coll)
    if len(err) < 1:
        QA_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


def save_index_list(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    index_list = QA_fetch_get_index_list()
    coll_index_list = client.index_list
    coll_index_list.create_index("code", unique=True)

    try:
        coll_index_list.insert_many(
            QA_util_to_json_from_pandas(index_list),
            ordered=False
        )
    except:
        pass


def save_index_day(client=MongoClient().client.tdx, ui_log=None, ui_progress=None):
    """save index_day

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """

    __index_list = QA_fetch_get_stock_list('index')
    coll = client.index_day
    coll.create_index(
        [('code',
          pymongo.ASCENDING),
         ('date_stamp',
          pymongo.ASCENDING)]
    )
    err = []

    def __saving_work(code, coll):

        try:
            ref_ = coll.find({'code': str(code)[0:6]})
            end_time = str(now_time())[0:10]
            if ref_.count() > 0:
                start_time = ref_[ref_.count() - 1]['date']

                QA_util_log_info(
                    '##JOB: Now Saving INDEX_DAY==== \n Trying updating {} from {} to {}'
                        .format(code,
                                start_time,
                                end_time),
                    ui_log=ui_log
                )

                if start_time != end_time:
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                QA_util_get_next_day(start_time),
                                end_time
                            )
                        )
                    )
            else:
                try:
                    start_time = '1990-01-01'
                    QA_util_log_info(
                        '##JOB: Now Saving INDEX_DAY==== \n Trying updating {} from {} to {}'
                            .format(code,
                                    start_time,
                                    end_time),
                        ui_log=ui_log
                    )
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                start_time,
                                end_time
                            )
                        )
                    )
                except:
                    start_time = '2009-01-01'
                    QA_util_log_info(
                        '##JOB: Now Saving INDEX_DAY==== \n Trying updating {} from {} to {}'
                            .format(code,
                                    start_time,
                                    end_time),
                        ui_log=ui_log
                    )
                    coll.insert_many(
                        QA_util_to_json_from_pandas(
                            QA_fetch_get_index_day(
                                str(code),
                                start_time,
                                end_time
                            )
                        )
                    )
        except Exception as e:
            QA_util_log_info(e, ui_log=ui_log)
            err.append(str(code))
            QA_util_log_info(err, ui_log=ui_log)

    for i_ in range(len(__index_list)):
        # __saving_work('000001')
        QA_util_log_info(
            'The {} of Total {}'.format(i_,
                                        len(__index_list)),
            ui_log=ui_log
        )

        strLogProgress = 'DOWNLOAD PROGRESS {} '.format(
            str(float(i_ / len(__index_list) * 100))[0:4] + '%'
        )
        intLogProgress = int(float(i_ / len(__index_list) * 10000.0))
        QA_util_log_info(
            strLogProgress,
            ui_log=ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intLogProgress
        )
        __saving_work(__index_list.index[i_][0], coll)
    if len(err) < 1:
        QA_util_log_info('SUCCESS', ui_log=ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ', ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)
