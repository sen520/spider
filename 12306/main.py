import requests

# url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC&ts=%E4%B8%8A%E6%B5%B7&date=2019-06-25&flag=N,N,Y'
url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-06-25&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'

res = requests.get(url)
print(res.text)