import re

import eastmoney
import sh_exchange
import stock
import sw
import sz_exchange


def analyse_all():
    stock_list = []
    stock_list.extend(sz_exchange.get_a_all_stock_from_file("./assets/深证A股列表.xlsx"))
    stock_list.extend(sh_exchange.get_a_all_stock_from_file("./assets/上证主板A股.xlsx"))

    business_dict = sw.get_a_all_class_from_file("./assets/申万行业分类.xlsx")
    for s in stock_list:
        if s.code in business_dict:
            s.business = business_dict[s.code]

    gro_count = 0
    for s in stock_list:
        gro = _analyse_single(s)
        if gro:
            print(f"{s.exchange}  {s.code}    {s.name}  {s.business}")
            gro_count += 1
    print(gro_count)


def _analyse_single(sto):
    p = eastmoney.get_lrb_nd(sto)
    gro = _check_profit_growth(p)
    return gro


def _analyse_single_lr_rate(sto):
    p = eastmoney.get_lrb_bgq(sto)
    return ((_parse_number(p[0].gsjlr) / _parse_number(p[4].gsjlr)) - 1) * 100


def _check_profit_growth(profit):
    gro = True
    last_value = None
    for p in profit:
        value = _parse_number(p.gsjlr)
        if last_value:
            if last_value < value:
                gro = False
                break
        last_value = value
    return gro


def _parse_number(number_str):
    if "--" == number_str:
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
    # analyse_all()
    s = stock.Stock()
    s.exchange = "SH"
    s.code = "600276"
    r = _analyse_single_lr_rate(s)
    print(r)
