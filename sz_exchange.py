import json
import re
import ssl
import urllib.request

from xlrd import open_workbook

import stock


def get_a_all_stock_from_file(xlsx_file):
    stock_list = []
    wb = open_workbook(filename=xlsx_file)
    print(wb)
    for s in wb.sheets():
        for row in range(s.nrows):
            if row == 0:
                continue

            sto = stock.Stock()
            sto.exchange = "SZ"
            for col in range(s.ncols):
                if col == 4:
                    sto.code = s.cell(row, col).value
                if col == 5:
                    sto.name = s.cell(row, col).value
                if col == 17:
                    sto.business = s.cell(row, col).value
            stock_list.append(sto)
    return stock_list


def get_a_all_stock_from_remote():
    page_no = 1
    page_count = None
    stock_list = []
    while True:
        req = urllib.request.Request(
            url=f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO={page_no}",
            headers={"Host": "www.szse.cn", "Accept": "application/json, text/javascript, */*; q=0.01",
                     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                     "X-Request-Type": "ajax"})
        resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
        resp_body = resp.read().decode("UTF-8")

        s_list = _get_a_stock(resp_body)
        stock_list.extend(s_list)

        if not page_count:
            page_count = _get_a_page_count(resp_body)

        page_no += 1
        if page_no > page_count:
            break


def _get_a_page_count(resp_body):
    type_list = json.loads(resp_body)
    for type in type_list:
        if "A股列表" == type["metadata"]["name"]:
            return type["metadata"]["pagecount"]


def _get_a_stock(resp_body):
    stock_list = []
    patt = re.compile("<a.*><u>(.+)</u></a>")
    type_list = json.loads(resp_body)
    for type in type_list:
        if "A股列表" == type["metadata"]["name"]:
            for d in type["data"]:
                s = stock.Stock()
                s.exchange = "SZ"
                s.code = d["agdm"]
                s.business = d["sshymc"]
                s.name = re.fullmatch(patt, d["agjc"]).group(1)
                stock_list.append(s)
    return stock_list


if __name__ == '__main__':
    # wb = open_workbook(filename="./assets/深证A股列表.xlsx")
    # print(wb)
    # for s in wb.sheets():
    #     print(s.name)
    #     for row in range(s.nrows):
    #         values = []
    #         for col in range(s.ncols):
    #             values.append(s.cell(row, col).value)
    #         print(values)
    #     print()

    get_a_all_stock_from_file("./assets/深证A股列表.xlsx")
