import re

import eastmoney
import sh_exchange
import sz_exchange


def analyse_all():
    stock_list = []
    stock_list.extend(sz_exchange.get_a_all_stock_from_file("./assets/深证A股列表.xlsx"))
    stock_list.extend(sh_exchange.get_a_all_stock_from_file("./assets/上证主板A股.xlsx"))

    for s in stock_list:
        print(f"{s.exchange}{s.code}")
        p = eastmoney.get_profit(s)
        gro = analyse(p)
        print(gro)


def analyse(profit):
    gro = True
    last_value = None
    for p in profit:
        value = _parse_number(p.gsjlr)
        if not last_value:
            last_value = value
        else:
            if last_value < value:
                gro = False
                break
    return gro


def _parse_number(number_str):
    print(number_str)
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
    print(_parse_number("-1.2万"))
