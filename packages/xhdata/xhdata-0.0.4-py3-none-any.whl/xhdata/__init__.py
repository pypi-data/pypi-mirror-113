#coding :utf-8

"""

Quantitative Financial Data Framework

by xhdata

2021/6/20
"""
import faulthandler
faulthandler.enable()
from dotenv import load_dotenv
load_dotenv(verbose=True)

__version__ = '0.0.4'
__author__ = 'xhdata'


from xhdata.Data.stock import (
    stock_zh_a_daily,
)


# 输出聚宽样式的数据
from xhdata.Data.jq_style import (
    get_price,
    get_all_securities,
)

