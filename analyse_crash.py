import baostock_helper
import stock


def analyse():
    fd = open("./assets/growth_list.txt")
    lines = []
    li = fd.readline()
    while li:
        lines.append(li)
        li = fd.readline()
    fd.close()

    baostock_helper.login()
    for li in lines:
        seg = li.split(",")
        s = stock.Stock()
        s.exchange = seg[0].strip()
        s.code = seg[1].strip()
        s.name = seg[3].strip()
        s.business = seg[4].strip()

        d15, d18 = baostock_helper.get_crash_condition(s)
        if greater_than_hs300(d15, d18):
            print(f"{s.exchange} {s.code}  {s.name}  {s.business}  {d15}   {d18}")
    baostock_helper.logout()


def greater_than_hs300(d15, d18):
    hs_15 = 2877.47 / 5353.75
    hs_18 = 2969.54 / 4381
    return d15 > hs_15 and d18 > hs_18


if __name__ == '__main__':
    analyse()
