import re
import socket

import eastmoney
import sh_exchange
import stock
import sw
import sz_exchange


def analyse_all(offset):
    stock_list = []
    stock_list.extend(sz_exchange.get_a_all_stock_from_file("./assets/深证A股列表.xlsx"))
    stock_list.extend(sh_exchange.get_a_all_stock_from_file("./assets/上证主板A股.xlsx"))

    business_dict = sw.get_a_all_class_from_file("./assets/申万行业分类.xlsx")
    for s in stock_list:
        if s.code in business_dict:
            s.business = business_dict[s.code]

    gro_count = 0
    idx = -1
    for s in stock_list:
        idx += 1

        if idx < offset:
            continue

        print(idx)
        gro_nd = _analyse_single_growth_nd(s)
        pe_ttm = eastmoney.get_stock_market(s)
        gro_bgq = _analyse_single_growth_bgq(s)
        if gro_nd and gro_bgq > 0:
            print(
                f"{s.exchange} {s.code}  [{pe_ttm} / {gro_bgq} = {_analyse_single_peg(s, pe_ttm, gro_bgq)}]  {s.name}  {s.business}")
            gro_count += 1
    print(gro_count)


def _analyse_single_growth_nd(sto):
    p = eastmoney.get_lrb_nd(sto)
    gro = _check_profit_growth(p)
    return gro


def _analyse_single_growth_bgq(sto):
    p = eastmoney.get_lrb_bgq(sto)
    return ((_parse_number(p[0].kfjlr) / _parse_number(p[4].kfjlr)) - 1) * 100


def _analyse_single_peg(sto, pe_ttm=None, gro_bgq=None):
    if not pe_ttm:
        pe_ttm = eastmoney.get_stock_market(sto)
    if not gro_bgq:
        gro_bgq = _analyse_single_growth_bgq(sto)
    return pe_ttm / gro_bgq


def _check_profit_growth(profit):
    gro = True
    last_value = None
    for p in profit:
        value = _parse_number(p.kfjlr)
        if last_value:
            if last_value < value * 0.9:
                gro = False
                break
        last_value = value
    return gro


def _parse_number(number_str):
    if "--" == number_str or "" == number_str:
        return -1
    if number_str.endswith("亿"):
        pat = re.compile("([0-9\.\-]+)亿")
        n = float(re.fullmatch(pat, number_str).group(1))
        return n * 100000000
    if number_str.endswith("万"):
        pat = re.compile("([0-9\.\-]+)万")
        n = float(re.fullmatch(pat, number_str).group(1))
        return n * 10000
    return float(number_str)


if __name__ == '__main__':
    socket.setdefaulttimeout(60)
    analyse_all(700)
    # s = stock.Stock()
    # s.exchange = "SZ"
    # s.code = "000672"
    # gro_nd = _analyse_single_growth_nd(s)
    # pe_ttm = eastmoney.get_stock_market(s)
    # gro_bgq = _analyse_single_growth_bgq(s)
    # if gro_nd and gro_bgq > 0:
    #     print(
    #         f"{s.exchange} {s.code}  [{pe_ttm} / {gro_bgq} = {_analyse_single_peg(s, pe_ttm, gro_bgq)}]  {s.name}  {s.business}")
