import httpx
from lxml import etree


def 获取文章列表():
    全部文章列表 = []
    for 页码 in range(1, 4):
        链接 = f"http://futaningmengcha991.lofter.com/?page={页码}"
        请求结果 = httpx.get(链接)
        网页内容 = etree.HTML(请求结果.text, parser=None)
        每页文章列表 = 网页内容.xpath('//li[@class="article"]/a')
        for 文章 in 每页文章列表:
            网址 = 文章.xpath("@href")[0]
            标题 = 文章.xpath("span/h2/text()")[0]
            全部文章列表.append((标题, 网址))
    return 全部文章列表


def 下载文章(title, url):
    请求结果 = httpx.get(url)
    网页内容 = etree.HTML(请求结果.text.replace("&nbsp;", " "), parser=None)
    文章内容 = 网页内容.xpath('//div[@class="text"]/p/text()')
    with open(f"README.md", "a") as f:
        f.write(f"## {title}\n\n")
        for 段落 in 文章内容:
            f.write(f"{段落}\n\n")


for 文章 in 获取文章列表():
    print(f"正在下载-{文章[0]}")
    下载文章(*文章)
