# import requests
#
# req_url = 'https://www.lagou.com/zhaopin/Java/2/?filterOption=3&sid=a81596021eaa4b788ade5d981349178e'
# # 2. 请求头 headers
# headers = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "no-cache",
#     "Connection": "keep-alive",
#     "Cookie": "_ga=GA1.2.616456481.1560847629; user_trace_token=20190618164712-aa165d07-91a5-11e9-b0f2-525400f775ce; LGUID=20190618164712-aa166105-91a5-11e9-b0f2-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b69d39cd0592-0686516593b823-3b654406-2073600-16b69d39cd1428%22%2C%22%24device_id%22%3A%2216b69d39cd0592-0686516593b823-3b654406-2073600-16b69d39cd1428%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2275.0.3770.100%22%7D%7D; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAAAGFABEF41F8DD3A5D1B32345F2C113E62BFCEE3; WEBTJ-ID=20190812105948-16c83c47e301e6-00d45888690f31-396a4507-2073600-16c83c47e313b8; _gid=GA1.2.122701185.1565578789; TG-TRACK-CODE=index_navigation; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1565578789,1565579253,1565582306,1565589001; _gat=1; SEARCH_ID=84fa5c59803a41c99ba25edb0d80840e; X_HTTP_TOKEN=f2915f61101f8d428485955651e79642f8d7aa3490; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1565595851; LGSID=20190812154412-fa1dd5f8-bcd4-11e9-894b-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F2%2F%3FfilterOption%3D3%26sid%3Da81596021eaa4b788ade5d981349178e; LGRID=20190812154412-fa1dd743-bcd4-11e9-894b-525400f775ce",
#     "Host": "www.lagou.com",
#     "Pragma": "no-cache",
#     "Referer": "https://www.lagou.com/zhaopin/Java/?labelWords=label",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
#
# }
# res = requests.get(req_url, headers=headers)
# res.text.encode('utf-8')
# print(res.text)



import requests

start_url = 'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=pyt'
pares_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    'Referer': "https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=pyt"
}
for i in range(1,10):
    data = {'first': 'false', 'pn': str(i), 'kd': 'python'}
    cookies = requests.get(url=start_url, headers=headers).cookies
    response = requests.post(url=pares_url, headers=headers, cookies=cookies, data=data)
    items = response.json()['content']['positionResult']['result']
    for item in items:
        print('--' * 30)
        print('职位：%s\t\t学历：%s\t\t工作年限：%s\t\t薪资：%s' % (item['positionName'], item['education'], item['workYear'], item['salary']))
        print('公司：%s\t\t行政区：%s\t\t公司全称：%s' % (item['companyShortName'], item['district'], item['companyFullName']))
        print('##' * 50)
    print('==='*30)
