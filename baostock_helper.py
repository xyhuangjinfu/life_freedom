import baostock as bs

import stock


def login():
    bs.login()


def logout():
    bs.logout()


def get_crash_condition(sto):
    data_2015_06_08 = None
    data_2016_02_29 = None
    rs = bs.query_history_k_data_plus(f"{'sz' if sto.exchange == 'SZ' else 'sh'}.{sto.code}",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
                                      start_date='2015-06-01', end_date='2015-06-10',
                                      frequency="d", adjustflag="2")
    while (rs.error_code == '0') & rs.next():
        if rs.get_row_data()[0] == "2015-06-08":
            data_2015_06_08 = rs.get_row_data()[5]

    rs = bs.query_history_k_data_plus(f"{'sz' if sto.exchange == 'SZ' else 'sh'}.{sto.code}",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
                                      start_date='2016-02-20', end_date='2016-03-02',
                                      frequency="d", adjustflag="2")
    while (rs.error_code == '0') & rs.next():
        if rs.get_row_data()[0] == "2016-02-29":
            data_2016_02_29 = rs.get_row_data()[5]

    data_2018_01_26 = None
    data_2019_01_02 = None
    rs = bs.query_history_k_data_plus(f"{'sz' if sto.exchange == 'SZ' else 'sh'}.{sto.code}",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
                                      start_date='2018-01-01', end_date='2018-02-10',
                                      frequency="d", adjustflag="2")
    while (rs.error_code == '0') & rs.next():
        if rs.get_row_data()[0] == "2018-01-26":
            data_2018_01_26 = rs.get_row_data()[5]

    rs = bs.query_history_k_data_plus(f"{'sz' if sto.exchange == 'SZ' else 'sh'}.{sto.code}",
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
                                      start_date='2018-12-20', end_date='2019-01-10',
                                      frequency="d", adjustflag="2")
    while (rs.error_code == '0') & rs.next():
        if rs.get_row_data()[0] == "2019-01-02":
            data_2019_01_02 = rs.get_row_data()[5]

    d15 = -1
    d18 = -1
    if data_2016_02_29 and data_2015_06_08:
        d15 = float(data_2016_02_29) / float(data_2015_06_08)
    if data_2019_01_02 and data_2018_01_26:
        d18 = float(data_2019_01_02) / float(data_2018_01_26)

    return d15, d18


if __name__ == '__main__':
    s = stock.Stock()
    s.code = "002705"
    s.exchange = "SZ"
    get_crash_condition(s)
