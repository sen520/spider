import requests
from lxml import etree


def get_page_info(res, company_list):

    lis = html.xpath('//ul[@class="item_con_list"]/li')
    for li in lis:
        top = li.xpath('./div[@class="list_item_top"]')
        postion = top[0].xpath('./div[@class="position"]')
        title = postion[0].xpath('.//h3/text()')[0]
        addr = postion[0].xpath('.//span[@class="add"]/em/text()')[0]
        money = postion[0].xpath('.//span[@class="money"]/text()')[0]
        exp = ''.join(postion[0].xpath('.//div[@class="li_b_l"]/text()'))

        company = top[0].xpath('./div[@class="company"]')
        company_name = company[0].xpath('./div[@class="company_name"]/a/text()')[0]
        company_industry = company[0].xpath('./div[@class="industry"]/text()')[0]

        bottom = li.xpath('./div[@class="list_item_bot"]')
        tag = bottom[0].xpath('./div[@class="li_b_l"]/span/text()')
        service = bottom[0].xpath('./div[@class="li_b_r"]/text()')
        company_list.append({'title': title, 'addr': addr, 'money': money, 'exp': exp.strip(), 'company_name': company_name,
                             'company_industry': company_industry.strip(), 'tag': tag, 'service': service})
        print(company_list)
        return company_list


if __name__ == '__main__':
    company_list = []
    for page in range(1, 20):
        # req_url = 'https://www.lagou.com/zhaopin/{}/?filterOption=3&sid=2fcd9ee5596648908c08a102f62f591b'.format(
        #     'java')
        req_url = 'https://www.lagou.com/zhaopin/Java/?filterOption=3&sid=a81596021eaa4b788ade5d981349178e'
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "_ga=GA1.2.616456481.1560847629; user_trace_token=20190618164712-aa165d07-91a5-11e9-b0f2-525400f775ce; LGUID=20190618164712-aa166105-91a5-11e9-b0f2-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b69d39cd0592-0686516593b823-3b654406-2073600-16b69d39cd1428%22%2C%22%24device_id%22%3A%2216b69d39cd0592-0686516593b823-3b654406-2073600-16b69d39cd1428%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2275.0.3770.100%22%7D%7D; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAAAGFABEF41F8DD3A5D1B32345F2C113E62BFCEE3; WEBTJ-ID=20190812105948-16c83c47e301e6-00d45888690f31-396a4507-2073600-16c83c47e313b8; _gid=GA1.2.122701185.1565578789; TG-TRACK-CODE=index_navigation; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1564379962,1565578789,1565579253,1565582306; LGSID=20190812115826-6fb12d99-bcb5-11e9-a4ff-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pcbt; PRE_HOST=sp0.baidu.com; PRE_SITE=https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fZNKw_0pEIb0FNkUsjx3dKI00000Zc2r7C00000F0XxQm.THd_myIEIfK85yF9pywd0ZnqujDzP1DkPAnsnjDsmvm1mfKd5HKDwjujrHFarjTvnRn4fbndwWbznjTsfRFAPjbsfbFa0ADqI1YhUyPGujY1nWTYPjTzrH03FMKzUvwGujYkP6K-5y9YIZK1rBtEILILQhk9uvqdQhPEUiq_my4bpy4MQgK9uvRETAnETvN9ThPCQh9YUysOIgwVgLPEIgFWuHdVgvPhgvPsI7qBmy-bINqsmvFY0APzm1YdrHmknf%26tpl%3Dtpl_11534_19968_16032%26l%3D1513622130%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E5%252587%252586%2525E5%2525A4%2525B4%2525E9%252583%2525A8-%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591-%252520%2525E9%2525AB%252598%2525E8%252596%2525AA%2525E5%2525A5%2525BD%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E5%2525AE%25259E%2525E6%252597%2525B6%2525E6%25259B%2525B4%2525E6%252596%2525B0%21%2526xp%253Did%28%252522m3274472908_canvas%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D177%26ie%3DUTF-8%26f%3D8%26tn%3Dbaidu%26wd%3Dlagou%26oq%3Dlagou%26rqlang%3Dcn; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm_source%3Dm_cf_cpt_baidu_pcbt; SEARCH_ID=c0ed7653ff3b4a23843abed0801e7e32; X_HTTP_TOKEN=f2915f61101f8d424232855651e79642f8d7aa3490; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1565582325; LGRID=20190812115844-7af909dc-bcb5-11e9-a4ff-5254005c3644",
            "Host": "www.lagou.com",
            "Pragma": "no-cache",
            "Referer": "https://www.lagou.com/zhaopin/Java/?labelWords=label",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
            }
        res = requests.get(req_url, headers=headers)
        html = etree.HTML(res.text)
        company_list = get_page_info(html, company_list)
        next_page = html.xpath('//a[text()="下一页"]/@href')[0]
        res = requests.get(next_page, headers=headers)
        print(res.text)
        break
