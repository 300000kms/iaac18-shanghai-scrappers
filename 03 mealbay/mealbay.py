'''
'''
#http://www.mealbay.net/home/restaurant.php
import requests
from lxml import etree
import csv
import datetime
import demjson
import collections
import time
import os
import functools
import geocoder
from tinydb import TinyDB, Query

'''
>>> g = geocoder.google('Mountain View, CA')
>>> g.geojson
>>> g.json
>>> g.wkt
>>> g.osm
'''

def clean(s):
    s = s.replace('\r','').replace('\n','').replace('\t','')
    return s


def getRestaurant(n):
    '''

    '''
    url = 'http://www.mealbay.net/home/menu.php?shopid=%s' %(n)
    print url
    session = requests.Session()
    session.max_redirects=1
    r = session.get(url)
    page = r.text
    tree = etree.HTML(page)

    t = clean(tree.xpath('//h3/text()[2]')[0])
    type = ' '.join( tree.xpath('//*[@class="label label-success"]/text()') )
    ad =  clean(tree.xpath('//*[@class="panel panel-default"]/div[1]/div[1]/div[2]/text()')[2]).replace('Restaurant Address: ','')
    charge = clean(tree.xpath('//*[@class="col-md-3 col-xs-6 col-sm-4"][2]//*[@class="panel-body"]/text()[1]')[0])

    menu =[]
    dishes = tree.xpath('//a[@class = "list-group-item"]')
    for d in dishes:
        id = d.xpath('.//*[@class="col-xs-2 col-md-1"]/text()')[0]

        name = d.xpath('.//p[@class="list-group-item-heading"]/text()')[0]
        desc = d.xpath('.//p[@class="list-group-item-text"]/small/text()')
        desc = desc[0] if len(desc)>0 else ''
        price = d.xpath('.//div[@class="col-md-2 text-right"]/strong/text()')[0]
        menu.append({'name':name, 'desc':desc, 'price':price, 'id':id })

    result = {'name':t, 'address':ad, 'type':type, 'charge':charge, 'menu':menu, 'url':url}
    return result

########################################

def saveId(id):
    with open('log', 'w') as f:
        f.write(str(id))
    return

def getId():
    try:
        with open('log', 'r') as f:
            n = f.read()
            return n
    except:
        with open('log', 'w') as f:
            return 0

def getLastId():
    id = getId()
    if id in (None, ''):
        return 0
    else:
        return int(id)

########################################

id = getLastId()
db = TinyDB('mealbay3.json')
for r in range (id+1,2000):
    print '>>> go :', r
    try:
        result = getRestaurant(r)
        db.insert(result)
        saveId(r)

    except Exception as e:
        print e
        saveId(r)
