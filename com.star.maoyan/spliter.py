import requests
import json
import re
import time
from requests.exceptions import RequestException

# 请求url
def get_one_page (url):

    try:
        # 用户代理：浏览器标识信息，防止禁止爬取。PC端chrome浏览器的判断标准是chrome字段，chrome后面的数字为版本号；
        # 移动端的chrome浏览器判断”android“、”linux“、”mobile safari“等字段，version后面的数字为版本号。
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
# 解析网页
def parse_one_page(html):
    pattern = re.compile(

        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
        + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
        + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    #findall获取正则表达式下所有内容

    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)



if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)