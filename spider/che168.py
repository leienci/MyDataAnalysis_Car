import random
import time
import csv
import threading

import requests
import parsel

# 保存数据到csv
csv_che168 = open('che168.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_che168)

# 请求头
headers = {
    'Cookie': 'sessionid=a9ed945a-418f-403d-9a33-5b7751885887; autouserid=265286305; pcpopclub=2e33b060b6c34d6e8203a7c3eb3ef8a00fcff2a1; clubUserShow=265286305|363|2|%e7%a6%8f%e5%b7%9e%e8%bd%a6%e5%8f%8b7247497|0|0|0|/g28/M07/0A/33/120X120_0_q87_autohomecar__ChxkmmKgBBqAFnOmAAE3xEBqo2s116.jpg|2023-09-26 15:49:44|0; fvlid=1701670113422lBNZadXipIRF; che_sessionid=45329946-82E7-4DE5-81F5-BEE572308660%7C%7C2023-12-04+14%3A08%3A51.790%7C%7C0; smidV2=20231204140920c7d1b39ce9e2cb9503750a5fc2d7be960052fe1bfe03c4c00; memberPhoneInfo=%7C15750876872%7C1; uarea=350200%7Cxiamen; area=350211; Hm_lvt_d381ec2f88158113b9b76f14c497ed48=1701670128,1701736436; userarea=350200; listuserarea=350200; sessionuserid=265286305; sessionlogin=0774f8c6b56045d6955e27a0dbe487880fcff2a1; usedcaruid=8Ad1eUNkLO8tlcIcb9KiVA==; UsedCarBrowseHistory=0%3A48156422%2C0%3A49464485%2C0%3A49569123%2C0%3A49601540%2C0%3A48986739%2C0%3A49585743%2C0%3A49578530%2C0%3A49540382%2C0%3A49500970%2C0%3A49387624; sessionvisit=5f1bee5b-8b67-44e1-8304-9e7399420d98; sessionvisitInfo=a9ed945a-418f-403d-9a33-5b7751885887|www.che168.com|104888; che_sessionvid=3FDEC5CB-7062-48C5-B14A-BE22E2632C7F; sessionip=36.248.247.254; ahpvno=70; Hm_lpvt_d381ec2f88158113b9b76f14c497ed48=1701769544; ahuuid=0F485E18-D0AE-439F-9BF2-77FDF366579F; showNum=64; v_no=67; visit_info_ad=45329946-82E7-4DE5-81F5-BEE572308660||3FDEC5CB-7062-48C5-B14A-BE22E2632C7F||-1||-1||67; che_ref=www.autohome.com.cn%7C0%7C110965%7C0%7C2023-12-05+17%3A45%3A43.887%7C2023-12-04+14%3A31%3A04.157; sessionuid=a9ed945a-418f-403d-9a33-5b7751885887',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
}


# 爬取车辆信息
def Spider_car_info(carinfo):
    # 拼接完整链接
    link = f'https://www.che168.com/{carinfo}'
    # 接收请求响应文件
    response = requests.get(url=link, headers=headers)
    data_html = response.text
    # 筛选数据
    selector = parsel.Selector(data_html)
    gearbox = selector.xpath('//*[@id="nav1"]/div[1]/ul[1]/li[3]/text()').get()  # 变速箱
    emission = selector.xpath('//*[@id="nav1"]/div[1]/ul[1]/li[4]/text()').get()  # 排放标准
    displacement = selector.xpath('//*[@id="nav1"]/div[1]/ul[1]/li[5]/text()').get()  # 排量
    release = selector.xpath('//*[@id="nav1"]/div[1]/ul[1]/li[6]/text()').get()  # 发布时间
    annual = selector.xpath('//*[@id="nav1"]/div[1]/ul[2]/li[1]/text()').get()  # 年检到期
    expiration = selector.xpath('//*[@id="nav1"]/div[1]/ul[2]/li[2]/text()').get()  # 保险到期
    transfers = (selector.xpath('//*[@id="nav1"]/div[1]/ul[2]/li[5]/text()').get()
                 .replace("次（以车辆登记证为准）", ""))  # 过户次数
    engine = selector.xpath('//*[@id="nav1"]/div[1]/ul[3]/li[1]/text()').get()  # 发动机
    horsepower = engine.split(' ')[1].replace("马力", "")  # 马力
    cylinder = engine.split(' ')[2]  # 气缸类型
    vehicle = selector.xpath('//*[@id="nav1"]/div[1]/ul[3]/li[2]/text()').get()  # 车辆级别
    fuel = (selector.xpath('//*[@id="nav1"]/div[1]/ul[3]/li[4]/text()').get()
            .replace("号", ""))  # 燃油标号
    drive = selector.xpath('//*[@id="nav1"]/div[1]/ul[3]/li[5]/text()').get()  # 驱动方式
    brand = selector.xpath('/html/body/div[4]/a[4]/text()').get().replace("二手", "")  # 品牌
    # print(gearbox, emission, displacement, release, annual,
    #       expiration, transfers, engine, vehicle, fuel, drive)
    # 返回详情信息
    return (gearbox, emission, displacement, release, annual, expiration,
            transfers, horsepower, cylinder, vehicle, fuel, drive, brand)


def Spider_car(page):
    url = f'https://www.che168.com/fujian/a0_0msdgscncgpi1ltocsp{page}exx0/?pvareaid=102179#currengpostion/'
    # 接收请求响应文件
    response = requests.get(url=url, headers=headers)
    data_html = response.text
    # print(data_html)

    # 筛选数据
    selector = parsel.Selector(data_html)
    lis = selector.css('.viewlist_ul li')
    tag = 0
    fail = 0
    for li in lis:
        try:
            name = li.css('.card-name::text').get()  # 车名
            unit = li.css('.cards-unit::text').get()  # 信息
            km = unit.split('／')[0].replace("万公里", "")  # 里程数
            years = unit.split('／')[1]  # 年份
            city = unit.split('／')[2]  # 城市
            # business = unit.split('／')[3]  # 商家
            sale = li.css('.pirce em::text').get()  # 售价
            price = li.css('s::text').get().replace("万", "")  # 原价
            links = li.css('.carinfo::attr(href)').get()  # 车辆链接
            # img = li.css('img::attr(src)').get()
            info = Spider_car_info(links)
            print(name, km, years, city, sale, price)
            print(info)
            # 保存数据
            (gearbox, emission, displacement, release, annual, expiration,
             transfers, horsepower, cylinder, vehicle, fuel, drive, brand) = info
            csv_writer.writerow([name, km, years, city, sale, price, gearbox, emission, displacement,
                                 release, annual, expiration, transfers, horsepower, cylinder, vehicle,
                                 fuel, drive, brand])
            tag = tag + 1
            print('爬取成功^_^')
        except:
            fail = fail + 1
            print('爬取失败QaQ')
            pass
        print(f'第{page}页，爬取成功{tag}辆，爬取失败{fail}辆')
        time.sleep(random.randint(1, 7))


def main():
    # 循环翻页
    for page in range(1, 101):
        print(f'正在爬取第{page}页...')
        Spider_car(page)
        print(f'第{page}页爬取完成')


if __name__ == '__main__':
    main()
