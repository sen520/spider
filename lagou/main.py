from collections import defaultdict
import requests
import time
from tools.tools import data_to_json, data_to_csv


def parse_page(json_object, company_list):
    if json_object['msg'] == "您操作太频繁,请稍后再访问":
        print('wait.......')
        time.sleep(20)
        return
    else:
        items = json_object['content']['positionResult']['result']
        return parse_items(items, company_list)


def parse_items(items, company_list):
    for item in items:
        company_dict = defaultdict()
        company_dict['company_name'] = item['companyFullName']
        company_dict['company_name_short'] = item['companyShortName']
        company_dict['position_name'] = item['positionName']
        company_dict['workYear'] = item['workYear']
        company_dict['education'] = item['education']
        company_dict['jobNature'] = item['jobNature']
        company_dict['salary'] = item['salary']
        company_dict['city'] = item['city']
        company_dict['financeStage'] = item['financeStage']
        company_dict['industryField'] = item['industryField']
        company_dict['positionAdvantage'] = item['positionAdvantage']
        company_dict['companyLabelList'] = ', '.join(item['companyLabelList'])
        company_dict['district'] = item['district']
        company_dict['positionLables'] = ', '.join(item['positionLables'])
        company_dict['businessZones'] = ', '.join(item['businessZones']) if type(item['businessZones']) == list else item['businessZones']
        company_dict['firstType'] = item['firstType']
        company_dict['secondType'] = item['secondType']
        company_dict['thirdType'] = ', '.join(item['skillLables'])
        company_list.append(company_dict)
        print(company_dict)
    return company_list


if __name__ == '__main__':
    company_list = []
    start_url = 'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=python'
    pares_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        'Referer': "https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=pyt"
    }
    cookies = requests.get(start_url, headers=headers).cookies
    for i in range(1, 10):
        data = {'first': 'false', 'pn': str(i), 'kd': 'python'}
        num = 0
        while True:
            res = requests.post(url=pares_url, headers=headers, cookies=cookies, data=data)
            l = parse_page(res.json(), company_list)
            if l:
                break
            num += 1
            if num > 3:
                break
        if num > 3:
            break
        company_list = l
        time.sleep(3)
        csv_key = ['company_name', 'company_name_short', 'position_name', 'workYear', 'education', 'jobNature',
                   'salary', 'city', 'financeStage', 'industryField', 'positionAdvantage', 'companyLabelList',
                   'district', 'positionLables', 'businessZones', 'firstType', 'secondType', 'thirdType']
        data_to_csv(company_list, csv_key, 'lagou')
        data_to_json(company_list, 'company')
        print('============')
