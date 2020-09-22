from xlrd import open_workbook

import stock


def get_a_all_stock_from_file(xlsx_file):
    stock_list = []
    wb = open_workbook(filename=xlsx_file)
    for s in wb.sheets():
        for row in range(s.nrows):
            if row == 0:
                continue

            sto = stock.Stock()
            sto.exchange = "SH"
            for col in range(s.ncols):
                if col == 0:
                    sto.code = str(int(s.cell(row, col).value) + 1000000)[1:]
                if col == 1:
                    sto.name = str(s.cell(row, col).value).strip()
            stock_list.append(sto)
    return stock_list


if __name__ == '__main__':
    get_a_all_stock_from_file("./assets/上证主板A股.xlsx")
