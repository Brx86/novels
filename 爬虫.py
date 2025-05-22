import requests
from lxml import etree


请求头 = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Cookie": "XXX",
}


def 获取文章列表():
    所有内容 = []
    for 页码 in range(1, 6):
        链接 = f"http://swarmgymbag.lofter.com/?page={页码}"
        请求结果 = requests.get(链接, 请求头=请求头)
        网页内容 = etree.HTML(请求结果.text)
        每页文章列表 = 网页内容.xpath('//div[@class="content"]/div')
        for 文章 in 每页文章列表:
            网址 = 文章.xpath("h2/a/@href")[0]
            标题 = 文章.xpath("h2/a/text()")[0]
            文章内容 = 文章.xpath("p/text()")
            print(标题, 网址)
            if "智力缺陷" in 标题:
                所有内容.append(f"## {标题}\n{网址}\n\n{'\n\n'.join(文章内容)}\n\n\n\n")
    所有内容.reverse()
    return 所有内容


with open("小说.md", "a", encoding="u8") as 文件:
    for 文本 in 获取文章列表():
        文件.write(文本)
