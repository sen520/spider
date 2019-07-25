import requests
from lxml import etree
from tools.tools import data_to_json

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "cookie": "lastCity=101010100; __c=1564024475; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D0pnWWmhBBFQN3B6suFNkWPrHuvKRWgoa4BJjr4STkGhp9_Kj2xqzcOofwESZdWk_%26wd%3D%26eqid%3D9c4c770a000a1e73000000045d391eba; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1564024476; _uab_collina=156402447572473883689834; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1564024495; __a=79664001.1564024475..1564024475.3.1.3.3",
    "pragma": "no-cache",
    "referer": "https://www.zhipin.com/c101010100/?query=python&page=2&ka=page-next",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


def get_info(url, data_list):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)

    job_divs = html.xpath('//div[@class="job-list"]//ul//div[@class="job-primary"]')
    for job_div in job_divs:
        company_dict = {}
        info_div = job_div.xpath('./div[@class="info-primary"]')[0]
        company_div = job_div.xpath('./div[@class="info-company"]/div[@class="company-text"]')[0]
        contact_person_div = job_div.xpath('./div[@class="info-publis"]')[0]
        # position
        position = info_div.xpath('.//div[@class="job-title"]/text()')[0]
        treatment = info_div.xpath('.//span/text()')[0]
        info = info_div.xpath('.//p/text()')
        addr_list = info[0].split(' ')
        addr_dict = {'city': addr_list[0], 'area': addr_list[1], 'street': addr_list[2]}
        exp = {'work': info[1], 'edu': info[2]}
        company_dict['position'] = {'name': position, 'treatment': treatment, 'addr': addr_dict, 'exp': exp}
        # company
        company_name = company_div.xpath('./h3/a/text()')[0]
        company_info = company_div.xpath('./p/text()')
        company_tag = ''
        if len(company_info) > 2:
            company_tag = company_info[1]
        company_dict['company'] = {'companyName': company_name, 'companyType': company_info[0],
                                   'companyTag': company_tag, 'companyTeam': company_info[-1]}
        # contacter
        contacter = contact_person_div.xpath('./h3/text()')
        company_dict['contacter'] = {'name': contacter[0], 'position': contacter[-1]}
        data_list.append(company_dict)
    return data_list


if __name__ == '__main__':
    urls = ['https://www.zhipin.com/c101010100/?query=python&page={}&ka=page-next'.format(i) for i in range(1, 11)]
    data_list = []
    total = len(urls)
    for index, url in enumerate(urls):
        print('一共%d个url, 正在抓%d' % (total, index + 1))
        data_list = get_info(url, data_list)
    print(len(data_list))
    data_to_json(data_list, 'job')
