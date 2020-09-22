from xlrd import open_workbook


def get_a_all_class_from_file(xlsx_file):
    business_dict = {}
    wb = open_workbook(filename=xlsx_file)
    for s in wb.sheets():
        for row in range(s.nrows):
            if row == 0:
                continue

            business = None
            code = None
            for col in range(s.ncols):
                if col == 0:
                    business = str(s.cell(row, col).value).strip()
                if col == 1:
                    code = str(int(s.cell(row, col).value) + 1000000)[1:]
            business_dict[code] = business
    return business_dict


if __name__ == '__main__':
    print(get_a_all_class_from_file("./assets/申万行业分类.xlsx"))
