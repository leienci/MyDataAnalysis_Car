import random
import time

import requests
import parsel
import csv

# 请求头
headers = {
    'Cookie': 'sessionid=a9ed945a-418f-403d-9a33-5b7751885887; autouserid=265286305; pcpopclub=2e33b060b6c34d6e8203a7c3eb3ef8a00fcff2a1; clubUserShow=265286305|363|2|%e7%a6%8f%e5%b7%9e%e8%bd%a6%e5%8f%8b7247497|0|0|0|/g28/M07/0A/33/120X120_0_q87_autohomecar__ChxkmmKgBBqAFnOmAAE3xEBqo2s116.jpg|2023-09-26 15:49:44|0; fvlid=1701670113422lBNZadXipIRF; che_sessionid=45329946-82E7-4DE5-81F5-BEE572308660%7C%7C2023-12-04+14%3A08%3A51.790%7C%7C0; smidV2=20231204140920c7d1b39ce9e2cb9503750a5fc2d7be960052fe1bfe03c4c00; memberPhoneInfo=%7C15750876872%7C1; uarea=350200%7Cxiamen; area=350211; Hm_lvt_d381ec2f88158113b9b76f14c497ed48=1701670128,1701736436; userarea=350200; listuserarea=350200; sessionuserid=265286305; sessionlogin=0774f8c6b56045d6955e27a0dbe487880fcff2a1; usedcaruid=8Ad1eUNkLO8tlcIcb9KiVA==; UsedCarBrowseHistory=0%3A48156422%2C0%3A49464485%2C0%3A49569123%2C0%3A49601540%2C0%3A48986739%2C0%3A49585743%2C0%3A49578530%2C0%3A49540382%2C0%3A49500970%2C0%3A49387624; sessionvisit=5f1bee5b-8b67-44e1-8304-9e7399420d98; sessionvisitInfo=a9ed945a-418f-403d-9a33-5b7751885887|www.che168.com|104888; che_sessionvid=3FDEC5CB-7062-48C5-B14A-BE22E2632C7F; sessionip=36.248.247.254; ahpvno=70; Hm_lpvt_d381ec2f88158113b9b76f14c497ed48=1701769544; ahuuid=0F485E18-D0AE-439F-9BF2-77FDF366579F; showNum=64; v_no=67; visit_info_ad=45329946-82E7-4DE5-81F5-BEE572308660||3FDEC5CB-7062-48C5-B14A-BE22E2632C7F||-1||-1||67; che_ref=www.autohome.com.cn%7C0%7C110965%7C0%7C2023-12-05+17%3A45%3A43.887%7C2023-12-04+14%3A31%3A04.157; sessionuid=a9ed945a-418f-403d-9a33-5b7751885887',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
}
# 保存数据到csv
csv_che168 = open('che168.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_che168)

# 循环翻页
for page in range(1, 66):
    url = f'https://www.che168.com/xiamen/a0_0msdgscncgpi1ltocsp{page}exx0/'
    print('正在爬取第', page, '页')
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
            # 保存数据
            csv_writer.writerow([name, kmNum, years, city, business, price, yprice])
        except:
            pass
    time.sleep(random.randint(5, 9))
