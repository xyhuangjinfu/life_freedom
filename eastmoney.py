import json
import ssl
import time
import urllib.request

import finance
import stock


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
    print(resp_lrb_body)
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
    p = get_lrb_bgq(s)
    print(p)
