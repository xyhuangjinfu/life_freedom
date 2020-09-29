import json
import socket
import ssl
import urllib.request

"""
curl -H 'Host: www.csindex.com.cn' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: http://www.csindex.com.cn/zh-CN/indices/index?class_1=1&class_10=10&class_16=16&class_17=17&class_18=18&class_19=19&class_20=20&class_21=21&class_7=7&is_custom_0=1' -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' -H 'Cookie: Hm_lvt_12373533b632515a7c0ccd65e7fc5835=1600678447,1600738886,1600848473,1601344033; Hm_lpvt_12373533b632515a7c0ccd65e7fc5835=1601357335; acw_tc=2f624a7316013576325317563e43902a842ff20cf2f928a89a45bd5ee0c1c0; XSRF-TOKEN=eyJpdiI6IkdvZHFcLzZSbmU4eE9kSWttUnV4YnpBPT0iLCJ2YWx1ZSI6Ik9MQXZjVnE5MHRNWTRRQUp3bFVXdE9Vbk93ZFlNOWNjUTRIQjB0dDVCWmpJWVVKSTF3QVdJcWx2VlNFcGxwSVRLeVVwTXpjTjBGeVwvSUJRTGFnSTRQZz09IiwibWFjIjoiYjAwNjkyZDQzZTI4MzQ1YzNlYWI4YjY1NzI2Y2I1MzlhYzc1YmZkYzVhZWI1ZTQ0Yjg1MzhjMzEwYWNmZjY4NCJ9; laravel_session=eyJpdiI6Ik5VUWtjc29HTmxSY2lmREtvUWRXY3c9PSIsInZhbHVlIjoiM3hXVDZcL0VocEtWbkgxczFjWVRvSk15eERlN29rd09ZbzJ6UzZyUGZJWkc4ZTFVbVZFZjNsSDhJVEtETHEwajJPK0Y3RkJicWcwREpKYk1kVmRLVVB3PT0iLCJtYWMiOiI3MWUyZjExNGQwNDc2NTI3YTFlNWJmOWUzNTJiYjNmYmJkNDIwM2I2ZWI4ZDZjZDAyZjNlZDFiNWI2YmM0ODk3In0%3D' --compressed 'http://www.csindex.com.cn/zh-CN/indices/index?page=20&page_size=50&by=asc&order=%E5%8F%91%E5%B8%83%E6%97%B6%E9%97%B4&data_type=json&class_1=1&class_7=7&class_10=10&class_16=16&class_17=17&class_18=18&class_19=19&class_20=20&class_21=21&is_custom_0=1'
{"total":579,"page_size":"50","total_page":13,"list":[]}% 
"""


def get_index_list():
    page = 1
    li = []
    while True:
        l = _get_index_list_by_page(page)
        if not l:
            break
        li.extend(l)
        page += 1
    return li


def _get_index_list_by_page(page):
    req = urllib.request.Request(
        url=f"http://www.csindex.com.cn/zh-CN/indices/index?page={page}&page_size=50&by=asc&order=%E5%8F%91%E5%B8%83%E6%97%B6%E9%97%B4&data_type=json&class_1=1&class_7=7&class_10=10&class_16=16&class_17=17&class_18=18&class_19=19&class_20=20&class_21=21&is_custom_0=1")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    return json.loads(resp_body)["list"]


def get_index_earnings_performance(index_code):
    req = urllib.request.Request(
        url=f"http://www.csindex.com.cn/zh-CN/indices/index-detail/{index_code}?earnings_performance=5%E5%B9%B4&data_type=json")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    return json.loads(resp_body)


def analyse():
    fd = open("assets/csindex.json", "r+")
    li = json.load(fd)
    fd.close()
    found = False
    last = "931380"
    for i in li:
        if not found and last:
            if last == i["index_code"]:
                found = True
            continue

        earn_dict = get_jd_earn(i["index_code"])
        earn_rate = _get_earn_rate(earn_dict, "2015-09-30", "2020-09-28")
        print(f"{i['index_code']}  ,  {earn_rate}  ,  {i['indx_sname']}")


def _get_earn_rate(earn_dict, start, end):
    if start not in earn_dict:
        return -1
    if end not in earn_dict:
        return -1
    return float(earn_dict[end]) / float(earn_dict[start])


def get_jd_earn(index_code):
    jd = ["2015-03-31", "2015-06-30", "2015-09-30", "2015-12-31",
          "2016-03-31", "2016-06-30", "2016-09-30", "2016-12-30",
          "2017-03-31", "2017-06-30", "2017-09-29", "2017-12-29",
          "2018-03-30", "2018-06-29", "2018-09-28", "2018-12-28",
          "2019-03-29", "2019-06-28", "2019-09-30", "2019-12-31",
          "2020-03-31", "2020-06-30", "2020-09-28", "2020-12-31"]
    es = get_index_earnings_performance(index_code)

    earn_dict = {}
    ie = 0
    for j in jd:
        if _compare_date(j, es[ie]["tradedate"].split(" ")[0]) < 0:
            continue
        while ie < len(es):
            if es[ie]["tradedate"].split(" ")[0] == j:
                # print(f"{j}   {es[ie]['tclose']}")
                earn_dict[j] = es[ie]['tclose']
                break
            ie += 1

    return earn_dict


def _compare_date(d1, d2):
    seg1 = d1.split("-")
    seg2 = d2.split("-")
    if seg1[0] != seg2[0]:
        return int(seg1[0]) - int(seg2[0])
    if seg1[1] != seg2[1]:
        return int(seg1[1]) - int(seg2[1])
    if seg1[2] != seg2[2]:
        return int(seg1[2]) - int(seg2[2])
    return 0


if __name__ == '__main__':
    socket.setdefaulttimeout(60)
    analyse()
    # get_index_earnings_performance("000932")
    # get_jd_earn("000932")
