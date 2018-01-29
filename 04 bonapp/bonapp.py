#http://www.bonapp.net/search/21-restaurant/----false/2/10?lang=en
'''
montar un listado de restaurantes

cojer los comentarios en tinydb


'''
import requests
from lxml import etree
import csv
import datetime
import demjson
import collections
import time
import os
import functools
import pprint
from googletrans import Translator
from tinydb import TinyDB, Query

pp= pprint.PrettyPrinter(indent=4)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def getList(n):
    '''
    :param n:
    :return:
    '''
    #url = 'http://www.mealbay.net/home/menu.php?shopid=%s' %(n)
    url ='http://www.bonapp.net/search/21-restaurant/----false/%s/10?lang=en' %(n)
    print url
    r = requests.get(url)
    if r.status_code==200:
        page = r.json()['resultData']
        return page
    else:
        return None


def getDataList():
    '''

    :return:
    '''
    return


def getRestaurant(id, name):
    '''

    :return:
    '''
    idd = str(id)+'-'+name
    url = 'http://www.bonapp.net/21-restaurant/%s?lang=en' %(idd)
    r = requests.get(url)
    print r.text
    return


def getComments(id, idx = 1):
    '''

    :param id:
    :return:
    '''
    #http://www.bonapp.net/21-restaurant/5273/comment/200/3?lang=en
    #http://www.bonapp.net/21-restaurant/5273/comment/2/20?lang=en
    url = 'http://www.bonapp.net/21-restaurant/%s/comment/%s/15?lang=en' %(id, idx)
    r = requests.get(url)

    to = r.json()['resultData']['totalSize']
    co = r.json()['resultData']['commentList']

    print to,len(co)
    if len(co)<15:
        return co
    else:
        return co+getComments(id, idx+1)

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
            return 1

def getLastId():
    id = getId()
    if id in (None, ''):
        return 1
    else:
        return int(id)

########################################

# db = TinyDB('db.json')
# co = getComments(5273)
#
# print len(co)
# for c in co:
#     print c
#     db.insert(c)


# User = Query()
# q = db.search(User.reviewId == 2671)
# print q
#
# for d in db.all():
#     print d.keys()
#     print d['reviewId'], d['isLiked'], d['feedType']


db = TinyDB('bonapp.json')
r =''
n = getLastId()
while r != None:
    r = getList(n)
    print len(r)
    if r != None:
        for rr in r:
            #print '----------------------------------------------------------------------------'
            id = rr['restaurantId']
            name = rr['cnName']
            db.insert(rr)
            #getRestaurant(id, name)
            #getComments(id)
    n+=1
    saveId(n)

##hacer el loop que coge los comments



