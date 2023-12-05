import requests
import parsel

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
}
url = 'https://www.che168.com/xiamen/list/#pvareaid=100943'

# 接收请求响应文件
response = requests.get(url=url, headers=headers)
data_html = response.text
# print(data_html)

# 筛选数据
selector = parsel.Selector(data_html)
lis = selector.css('.viewlist_ul li')
for li in lis:
    try:
        name = li.css('.card-name::text').get()  # 车名
        unit = li.css('.cards-unit::text').get()  # 信息
        kmNum = unit.split('／')[0]
        years = unit.split('／')[1]
        city = unit.split('／')[2]
        business = unit.split('／')[3]
        price = li.css('.pirce em::text').get()  # 售价
        yprice = li.css('s::text').get()  # 原价
        carinfo = li.css('.carinfo::attr(href)').get()
        img = li.css('img::attr(src)').get()
        print(name, kmNum, years, city, business, price, yprice)
    except:
        pass
