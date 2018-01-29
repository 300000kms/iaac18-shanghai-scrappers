'''
combiene actualizar la cookie
'''
import requests
import pprint
from lxml import etree
from tinydb import TinyDB, Query

pp= pprint.PrettyPrinter(indent=4)
db = TinyDB('dianping2.json')
# www.dianping.com%2Fsearch%2Fcategory%2F1%2F10
n=1
while n != False:
    # http://www.dianping.com/search/category/1/10/p50?aid=17648683%2C16789967%2C23999832%2C63177252%2C27421074%2C28425895
    url ="http://www.dianping.com/search/category/1/10/p%s?" %(n)
    print url
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'es-ES,es;q=0.8,ca;q=0.6,en;q=0.4,en-US;q=0.2'
    headers['Connection'] = 'keep-alive'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Cookie'] = 'navCtgScroll=0; _hc.v=eeb59a5e-fd58-5a3f-60f6-e60430faa227.1511436978; __mta=213185195.1513608321706.1513608321706.1513608321706.1; _lxsdk_cuid=1606a16421ec8-0973332003a6c3-38710357-1fa400-1606a16421fc8; _lxsdk=1606a16421ec8-0973332003a6c3-38710357-1fa400-1606a16421fc8; aburl=1; cye=shanghai; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; cy=1; s_ViewType=10; _lxsdk_s=1607e5730fd-b91-0c2-09e%7C%7C17'
    headers['Host'] = 'www.dianping.com'  # este es clave
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['referer']='http://www.dianping.com/search/category/1/10/r835'

    r = requests.get(url, headers=headers)

    x_rte = '//*[@id="shop-all-list"]//li/*[@class="txt"]'
    x_name = './/h4/text()'
    x_type = './/*[@class="tag"]/text()'
    x_address = './/*[@class="addr"]/text()'
    x_taste = './/*[@class="comment-list"]/span[1]/b//text()'
    x_enviroment = './/*[@class="comment-list"]/span[2]/b//text()'
    x_service = './/*[@class="comment-list"]/span[3]/b//text()'
    x_stars = ".//*[contains(@class, 'sml-rank-stars')]/@class"
    x_comments ='.//*[@class="comment"]/a[1]/b/text()'
    x_price ='.//*[@class="comment"]/a[2]/b/text()'

    tree = etree.HTML(r.text)
    rtes = tree.xpath(x_rte)
    print len(rtes)
    for rte in rtes:
        data = {}
        data['name'] = rte.xpath(x_name)[0]
        data['type'] = rte.xpath(x_type)[0]
        data['address']= rte.xpath(x_address)[0]
        data['taste'] = rte.xpath(x_taste)[0] if len(rte.xpath(x_taste)) >0 else ''
        data['enviro'] = rte.xpath(x_enviroment)[0] if len(rte.xpath(x_enviroment)) >0 else ''
        data['service'] = rte.xpath(x_service)[0] if len(rte.xpath(x_service)) >0 else ''
        data['stars'] = rte.xpath(x_stars)[0].replace('sml-rank-stars sml-str', '')[0]
        data['comments'] = rte.xpath(x_comments)[0]
        data['price'] = rte.xpath(x_price)[0].replace(u'\uffe5','') if len(rte.xpath(x_price))>0 else ''
        db.insert(data)

    n+=1
