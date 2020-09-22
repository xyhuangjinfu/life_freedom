import json
import ssl
import urllib.request

import finance
import stock


def get_profit(sto):
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


if __name__ == '__main__':
    s = stock.Stock()
    s.exchange = "SH"
    s.code = "600276"
    p = get_profit(s)
    print(p)
