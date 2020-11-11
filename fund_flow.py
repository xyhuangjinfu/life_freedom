import json
import socket
import ssl
import urllib.request

from colorama import Fore, Style
from xlrd import open_workbook

import sh_exchange
import sz_exchange


def _get_stock_real_time_fund_flow(stock):
    req = urllib.request.Request(
        url=f"http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid={0 if stock.exchange == 'SZ' else 1}.{stock.code}&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    return json.loads(resp_body)["data"]["klines"]


def _get_stock_history_fund_flow(stock):
    req = urllib.request.Request(
        url=f"http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=0&klt=101&secid={0 if stock.exchange == 'SZ' else 1}.{stock.code}&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    return json.loads(resp_body)["data"]["klines"]


def _get_all_stock():
    stock_list = []
    stock_list.extend(sz_exchange.get_a_all_stock_from_file("./assets/深证A股列表.xlsx"))
    stock_list.extend(sh_exchange.get_a_all_stock_from_file("./assets/上证主板A股.xlsx"))
    stock_dict = {}
    for stock in stock_list:
        stock_dict[stock.code] = stock
    return stock_dict


def _get_index_stock_code_list(index_code):
    req = urllib.request.Request(
        url=f"http://www.csindex.com.cn/uploads/file/autofile/cons/{index_code}cons.xls")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read()

    wb = open_workbook(file_contents=resp_body)
    stock_code_list = []
    for s in wb.sheets():
        for row in range(s.nrows):
            if row == 0:
                continue
            for col in range(s.ncols):
                if col == 4:
                    stock_code_list.append(str(int(s.cell(row, col).value) + 1000000)[1:])
    return stock_code_list


def _analyse_index_real_time_fund_flow(index_code):
    stock_dict = _get_all_stock()
    stock_code_list = _get_index_stock_code_list(index_code)
    flow_zl = 0
    flow_cdd = 0
    flow_dd = 0
    flow_zd = 0
    flow_xd = 0
    for stock_code in stock_code_list:
        fund_flow_list = _get_stock_real_time_fund_flow(stock_dict[stock_code])
        fund_flow = fund_flow_list[len(fund_flow_list) - 1]
        fund_flow_seg = fund_flow.split(",")
        flow_zl = float(fund_flow_seg[1]) + flow_zl
        flow_xd = float(fund_flow_seg[2]) + flow_xd
        flow_zd = float(fund_flow_seg[3]) + flow_zd
        flow_dd = float(fund_flow_seg[4]) + flow_dd
        flow_cdd = float(fund_flow_seg[5]) + flow_cdd
    return flow_zl, flow_cdd, flow_dd, flow_zd, flow_xd


def _analyse_index_history_fund_flow(index_code):
    stock_dict = _get_all_stock()
    stock_code_list = _get_index_stock_code_list(index_code)
    fund_flow_dict = {}
    for stock_code in stock_code_list:
        fund_flow_list = _get_stock_history_fund_flow(stock_dict[stock_code])
        fund_flow_dict[stock_code] = fund_flow_list
    for idx in range(0, 30):
        flow_date = None
        flow_zl = 0
        flow_cdd = 0
        flow_dd = 0
        flow_zd = 0
        flow_xd = 0
        for k, v in fund_flow_dict.items():
            fund_flow = v[len(v) - 1 - idx]
            fund_flow_seg = fund_flow.split(",")
            flow_date = fund_flow_seg[0]
            flow_zl = float(fund_flow_seg[1]) + flow_zl
            flow_xd = float(fund_flow_seg[2]) + flow_xd
            flow_zd = float(fund_flow_seg[3]) + flow_zd
            flow_dd = float(fund_flow_seg[4]) + flow_dd
            flow_cdd = float(fund_flow_seg[5]) + flow_cdd
        print(Fore.RED if flow_zl > 0 else Fore.GREEN, end="")
        print(
            f"{flow_date},     主力:{_format_fund_display(flow_zl)}, 超大单:{_format_fund_display(flow_cdd)}, 大单:{_format_fund_display(flow_dd)}, 中单:{_format_fund_display(flow_zd)}, 小单:{_format_fund_display(flow_xd)}")
        print(Style.RESET_ALL, end="")


def _get_pre_install_index_list():
    index_list = [("399975", "证券公司"),
                  ("399986", "中证银行"),
                  ("399973", "中证国防"),
                  ("931071", "人工智能"),
                  ("931406", "5G 50"),
                  ("399976", "CS新能车"),
                  ("931380", "科技50"),
                  ("931140", "医药50"),
                  ("000932", "中证消费"),
                  ("000300", "沪深300"),
                  ("000905", "中证500")]
    return index_list


def _analyse_all_index_real_time_fund_flow():
    index_list = _get_pre_install_index_list();
    for index in index_list:
        flow = _analyse_index_real_time_fund_flow(index[0])
        print(Fore.RED if flow[0] > 0 else Fore.GREEN, end="")
        print(
            f"{index[1]},     主力:{_format_fund_display(flow[0])}, 超大单:{_format_fund_display(flow[1])}, 大单:{_format_fund_display(flow[2])}, 中单:{_format_fund_display(flow[3])}, 小单:{_format_fund_display(flow[4])}")
        print(Style.RESET_ALL, end="")


def _format_fund_display(fund):
    y = 100000000
    if abs(fund) > y:
        return f"{round(fund / y, 2)}亿"
    w = 10000
    if abs(fund) > w:
        return f"{round(fund / w, 2)}万"
    return f"{round(fund, 2)}元"


if __name__ == '__main__':
    socket.setdefaulttimeout(60)
    # _analyse_all_index_fund_flow()
    # s = stock.Stock()
    # s.code = "300555"
    # s.exchange = "SZ"
    # _get_stock_history_fund_flow(s)
    # _analyse_index_history_fund_flow(931406)
