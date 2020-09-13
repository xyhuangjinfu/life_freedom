import json
import ssl
import time
import urllib.request

context = ssl._create_unverified_context()

url = "https://danjuanapp.com/djapi/index_eva/pe_history/SH000922?day=all"

hed = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "device_id=web_r1xeWejEw; xq_a_token=01cd7758682a857c480534aafa9ea01f6881ae8a; channel=1300100141; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1599959322,1599978923; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1599980356; acw_tc=2760777915999831487063232e40606f19c37508dc99df8a3c03fff159dfdd; timestamp=1599983148722"
}

req = urllib.request.Request(url=url, headers=hed)

resp = urllib.request.urlopen(req)
resp_str = resp.read().decode('utf-8')

body = json.loads(resp_str)
data = body["data"]
index_eva_pe_growths = data["index_eva_pe_growths"]

x = []

for d in index_eva_pe_growths:
    # print(d["pe"], end="    ")
    # 转换成localtime
    # time_local = time.localtime(d["ts"] / 1000)
    # 转换成新的时间格式(精确到秒)
    # dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    # print(dt)  # 2019-10-11 14:15:56
    x.append(float(d["pe"]))

x.sort()
print(x[int(len(x) * 0.2)])
print(x[int(len(x) * 0.5)])
print(x[int(len(x) * 0.8)])


# curl 'https://danjuanapp.com/djapi/index_eva/pe_history/SH000922?day=all' \
#      -H 'Connection: keep-alive' \
#         -H 'Cache-Control: max-age=0' \
#            -H 'Upgrade-Insecure-Requests: 1' \
#               -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36' \
#                  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
#                     -H 'Sec-Fetch-Site: cross-site' \
#                        -H 'Sec-Fetch-Mode: navigate' \
#                           -H 'Sec-Fetch-User: ?1' \
#                              -H 'Sec-Fetch-Dest: document' \
#                                 -H 'Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
#                                    -H 'Cookie: device_id=web_r1xeWejEw; xq_a_token=01cd7758682a857c480534aafa9ea01f6881ae8a; channel=1300100141; Hm_lvt_b53ede02df3afea0608038748f4c9f36=1599959322,1599978923; Hm_lpvt_b53ede02df3afea0608038748f4c9f36=1599980356; acw_tc=2760777915999831487063232e40606f19c37508dc99df8a3c03fff159dfdd; timestamp=1599983148722' \
#                                       --compressed \
#                                       --insecure
