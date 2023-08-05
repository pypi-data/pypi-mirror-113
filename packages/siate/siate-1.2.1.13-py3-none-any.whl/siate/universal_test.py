# -*- coding: utf-8 -*-

#======================================================================
import os;os.chdir("S:/siateng")
from siate import *

tickers=["XPEV","000625.SZ","600104.SS","2238.HK","0175.HK","LI","NIO"]
gm=compare_snapshot(tickers,"Gross Margin",axisamp=1.9)
pm=compare_snapshot(tickers,"Profit Margin",axisamp=2)
#======================================================================
#======================================================================
#======================================================================
#======================================================================
#======================================================================
import os;os.chdir("S:/siat")
from siat import *

codetranslate("0175.HK")
codetranslate("601825.SS")
codetranslate("601827.SS")
codetranslate("000003.SS")

codename=codetranslate("002003.SZ")
if codename[-2]==' ':
    codename=codename[:-3]

codetranslate("002003.SZ")
codetranslate("PLTR")

tickers=["XPEV","000625.SZ","600104.SS","2238.HK","0175.HK","LI","NIO"]
gm=compare_snapshot(tickers,"Gross Margin",axisamp=1.9)
#======================================================================
import akshare as ak

#列表中最后一个为最新名称
code="601825.SS"
suffix=code[-3:]
stock=code[:-3]
names = ak.stock_info_change_name(stock=stock)
if not (names is None):
    codename=names[-1]
else:
    codename=code



#======================================================================
import yfinance as yf

tp=yf.Ticker("XPEV")
dic=tp.info
current_name_eng=dic["shortName"]
