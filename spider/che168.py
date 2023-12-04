import requests
from bs4 import BeautifulSoup

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
}
url = 'https://www.che168.com/xiamen/list/#pvareaid=100943'

# 接收请求响应文件
response = requests.get(url=url, headers=headers)
soup_details = BeautifulSoup(response.text, 'html.parser')
print(soup_details)

