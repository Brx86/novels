import httpx
import time
from lxml import etree

请求头 = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Cookie": "xxx",
}


def 获取文章列表():
    for 页码 in range(1, 4):
        链接 = f"http://futaningmengcha991.lofter.com/?page={页码}"
        请求结果 = httpx.get(链接, headers=请求头)
        网页内容 = etree.HTML(请求结果.text, parser=None)
        每页文章列表 = 网页内容.xpath('//li[@class="article"]/a')
        for 文章 in 每页文章列表:
            网址 = 文章.xpath("@href")[0]
            标题 = 文章.xpath("span/h2/text()")[0]
            yield (标题, 网址)


def 下载文章(标题, 链接):
    请求结果 = httpx.get(链接, headers=请求头)
    网页内容 = etree.HTML(请求结果.text.replace("&nbsp;", " "), parser=None)
    文章内容 = 网页内容.xpath('//div[@class="text"]/p/text()')
    发布时间 = 网页内容.xpath('//span[@class="date"]/text()')[0]
    with open("小说.md", "a") as 文件:
        文件.write(f"## {标题}\n\n发布时间: {发布时间}\n\n")
        for 段落 in 文章内容:
            文件.write(f"{段落}\n\n")


for 文章 in 获取文章列表():
    print(f"正在下载-{文章[0]}: {文章[1]}")
    time.sleep(2)
    下载文章(*文章)
