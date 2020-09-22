import json
import ssl
import time
import urllib.request

import finance
import stock


def get_stock_market(sto):
    req = urllib.request.Request(
        url=f"http://push2.eastmoney.com/api/qt/stock/get?invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292&secid={0 if sto.exchange == 'SZ' else 1}.{sto.code}")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("UTF-8")
    da = json.loads(resp_body)
    return da["data"]["f164"]


def get_lrb_bgq(sto):
    # req_date = urllib.request.Request(
    #     url=f"http://f10.eastmoney.com/NewFinanceAnalysis/lrbDateAjax?reportDateType=0&code={sto.exchange}{sto.code}")
    # resp_date = urllib.request.urlopen(req_date, context=ssl._create_unverified_context())
    # resp_date_body = resp_date.read().decode("UTF-8")

    req_lrb = urllib.request.Request(
        url=f"http://f10.eastmoney.com/NewFinanceAnalysis/lrbAjax?companyType=4&reportDateType=0&reportType=1&endDate={_next_bgq()}&code={sto.exchange}{sto.code}")
    resp_lrb = urllib.request.urlopen(req_lrb, context=ssl._create_unverified_context())
    resp_lrb_body = resp_lrb.read().decode("UTF-8")
    resp_lrb_body = resp_lrb_body.replace("\\", "")
    resp_lrb_body = resp_lrb_body[1:len(resp_lrb_body) - 1]
    bgq_list = json.loads(resp_lrb_body)
    profit_list = []
    for bgq in bgq_list:
        p = finance.Profit()
        p.date = bgq["REPORTDATE"]
        p.gsjlr = bgq["PARENTNETPROFIT"]
        profit_list.append(p)
    return profit_list


def get_lrb_nd(sto):
    req = urllib.request.Request(
        url=f"http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type=1&code={sto.exchange}{sto.code}")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("UTF-8")
    return _parse(resp_body)


def _parse(resp_body):
    lr_list = json.loads(resp_body)
    profit_list = []
    for lr in lr_list:
        p = finance.Profit()
        p.date = lr["date"]
        p.gsjlr = lr["gsjlr"]
        profit_list.append(p)
    return profit_list


def _next_bgq():
    # TODO
    lt = time.localtime(time.time())
    time.strftime(f"%Y-%m-%d", lt)
    return "2020-9-30"


if __name__ == '__main__':
    s = stock.Stock()
    s.exchange = "SH"
    s.code = "600276"
    p = get_stock_market(s)
    print(p)
