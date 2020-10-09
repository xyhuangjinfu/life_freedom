import json
import re
import ssl
import urllib.request
import urllib.parse


# http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?callback=jQuery18306933264876761891_1601561535189&m=0&key=%E6%B2%AA%E6%B7%B1300&_=1601561535214


def get_spx_500():
    """
    # url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?callback=jQuery18307544284580519562_1601556115391&m=1&key=%E4%B8%AD%E8%AF%81500&pageindex=0&pagesize=147&_=1601556118483"
    :return:
    """
    req = urllib.request.Request(
        url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=1&key=%E6%A0%87%E6%99%AE500&pageindex=0&pagesize=200")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    d = json.loads(resp_body)
    return d["Datas"]


def get_hs_300():
    """
    # url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?callback=jQuery18307544284580519562_1601556115391&m=1&key=%E4%B8%AD%E8%AF%81500&pageindex=0&pagesize=147&_=1601556118483"
    :return:
    """
    req = urllib.request.Request(
        url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=1&key=%E6%B2%AA%E6%B7%B1300&pageindex=0&pagesize=200")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    d = json.loads(resp_body)
    return d["Datas"]


def get_zz_500():
    """
    # url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?callback=jQuery18307544284580519562_1601556115391&m=1&key=%E4%B8%AD%E8%AF%81500&pageindex=0&pagesize=147&_=1601556118483"
    :return:
    """
    req = urllib.request.Request(
        url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=1&key=%E4%B8%AD%E8%AF%81500&pageindex=0&pagesize=200")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    d = json.loads(resp_body)
    return d["Datas"]


def get(search):
    """
    # url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?callback=jQuery18307544284580519562_1601556115391&m=1&key=%E4%B8%AD%E8%AF%81500&pageindex=0&pagesize=147&_=1601556118483"
    :return:
    """
    req = urllib.request.Request(
        url=f"http://fundsuggest.eastmoney.com/FundSearch/api/FundSearchPageAPI.ashx?m=1&key={urllib.parse.quote(search)}&pageindex=0&pagesize=200")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    d = json.loads(resp_body)
    return d["Datas"]


def get_jjfl(code):
    req = urllib.request.Request(
        url=f"http://fundf10.eastmoney.com/jjfl_{code}.html")
    resp = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    resp_body = resp.read().decode("utf-8-sig")
    pattern_glfl = re.compile("<td.*>管理费率</td><td.*?>(.*?)</td>")
    pattern_tgfl = re.compile("<td.*>托管费率</td><td.*?>(.*?)</td>")
    pattern_xsfwfl = re.compile("<td.*>销售服务费率</td><td.*?>(.*?)</td>")
    pattern_sgfl = re.compile("申购费率（前端）.*?<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>.*?([\.0-9]+%).*?</td>")

    glfl_list = re.findall(pattern_glfl, resp_body)
    glfl = glfl_list[0] if glfl_list else "0.00%（每年）"
    tgfl_list = re.findall(pattern_tgfl, resp_body)
    tgfl = tgfl_list[0] if tgfl_list else "0.00%（每年）"
    xsfwfl_list = re.findall(pattern_xsfwfl, resp_body)
    xsfwfl = xsfwfl_list[0] if xsfwfl_list else "0.00%（每年）"
    sgfl_list = re.findall(pattern_sgfl, resp_body)
    sgfl = sgfl_list[0] if sgfl_list else "0.00%"

    return glfl, tgfl, xsfwfl, sgfl


if __name__ == '__main__':
    jj_list = get("易方达")
    for j in jj_list:
        code = j["CODE"]
        name = j["NAME"]
        fl = get_jjfl(code)
        print(f"{code}  {fl}   {name}")

    # x = get_jjfl("005919")
    # x = get_jjfl("501036")
    # x = get_jjfl("008001")
    # print(x)
    # s = """
    # 申购费率（前端）</label><label class="right"></label></h4><div class="space0"></div><table class="w650 comm jjfl" style='width:720px;'><thead><tr><th class="first je">适用金额</th><th class="qx">适用期限</th><th class="last fl speciacol w230" style='width:230px;'><span class="sgfv">原费率</span><span class="sgline">|</span><div class="sgyh"  style='width:154px;'>天天基金优惠费率<br/>银行卡购买<span class="sgline" style='float:none;'>|</span>活期宝购买</div></th></tr></thead><tbody><tr><td class="th">小于50万元</td><td>---</td><td><strike class='gray'>0.80%</strike>&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.08%&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;0.08%</td></tr><tr><td class="th">大于等于50万元，小于100万元</td><td>---</td><td><strike class='gray'>0.50%</strike>&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.05%&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;0.05%</td></tr><tr><td class="th">大于等于100万元</td><td>---</td><td>每笔1000元</td></tr></tbody></table><div class='sgfltip'><div class='hqbtip'><font class='px12'>
    # """
    # pattern_sgfl = re.compile("申购费率[\s\S]*([\.0-9]{+}%)")
    # pattern_sgfl = re.compile("申购费率（前端）.*?<td.*>")
    # pattern_sgfl = re.compile("申购费率（前端）.*?<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>.*?([\.0-9]+%).*?</td>")
    # # pattern_sgfl = re.compile("申购费率（前端）.*?<td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>")
    # # pattern_sgfl = re.compile("申购费率（前端）.*?([\.0-9]+%)")
    # print(re.findall(pattern_sgfl, s))
