#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
version 2.1
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


###############################################################################

def saveError(text):
    with open('tripadvisor_errors.txt', 'a') as f:
        f.write(text)

def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            job_func(*args, **kwargs)
        except Exception as e:
            i = datetime.datetime.now()
            m = i.strftime('%Y/%m/%d %H:%M:%S')+'  function: '+job_func.__name__+' ---> '+ str(e)+'\n'
            saveError(m)
            reporter.send(m)
            #import traceback
            #print(traceback.format_exc())
            #traceback.print_exc(file=sys.stdout) ###documentar
    return wrapper

###############################################################################


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8') ############################################
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data



def saveDictToCsv(data):
    filename = outputfile
    file_exists = os.path.isfile(filename)

    data = convert(data)
    keys = sorted(data[0].keys())

    with open(filename, 'a') as csvfile:
        w = csv.DictWriter(csvfile, keys)
        if not file_exists:
            w.writeheader()
        for d in data:
            w.writerow(d)

    print 'data saved'
    return


def saveToCsv(data):
    filename = outputfile
    file_exists = os.path.isfile(filename)
    with open(filename, 'a+') as csvfile:
        for d in data:
            csvfile.write(str(d))
            csvfile.write('\n')

    print 'data saved'
    return



def parseOfferJson(url):

    url = 'https://www.tripadvisor.es'+url
    r = getUrl(url)

    if r != None:
        page = r
    else:
        return None

    tree = etree.HTML(page)

    tr = tree.xpath("//script[contains(.,'\"@context\" : \"http://schema.org\"')]/text()")
    mp = tree.xpath("//script[contains(.,\"window.mapDivId = \'map0Div\';\")]/text()")

    if len(mp)>0:
        geo = mp[0].split('window.map0Div = ')[1].split('};')[0]+'}'
        geo = demjson.decode(geo)

    if len(tr)>0:
        jsonString = tr[0]
        try:
            js = demjson.decode(jsonString)
            if geo not in ('', None):
                js['lat'] = geo['lat']
                js['lng'] = geo['lng']
            return js

        except Exception as e:
            print '-----------------------------------------------------------'
            print jsonString
            print e
            return {}

    else:
        return {}



def getUrl(url):
    '''
    descarga y valida la web soicitada
    '''
    intentos = 1

    headers={}
    headers['user-agent'] = 'my-app/0.0.1'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'es,ca;q=0.8'

    url = url.lstrip('/')
    if url[0:7] != 'http://' and url[0:8] != 'https://' :
        url = 'http://'+url

    while intentos < 10:
        time.sleep(0.5)
        print '.',
        try:
            print
            print url
            r = requests.get( url, headers = headers, timeout = 10 )
        except:
            print 'error request :', url
            return None
        print len(r.text)
        if r.status_code == 200 and len(r.text) > 120000:
            print r.status_code,
            return r.text
        elif r.status_code == 200 and len(r.text) < 120000:
            print r.status_code, 'now waiting'
            time.sleep(intentos*intentos)
        else:
            print r.status_code, 'now waiting'
            time.sleep(1)
        intentos += 1
    print 'error on :',url
    return


def saveLast(x):
    with open('tripadvisor_log.txt', 'w') as f:
        f.write(str(x))
    return


def getLast():
    try:
        with open('tripadvisor_log.txt', 'r') as f:
            r = int( f.read() )
    except:
        r = 0
    return r


def findOffers():
    '''
    https://www.tripadvisor.es/Restaurants-g187514-Madrid.html
    https://www.tripadvisor.es/Restaurants-g187497-Barcelona_Catalonia.html

    '''
    rr = 28
    r = rr

    i = getLast()

    xp_offers = '//*[contains(@class ,"listing") and contains(@class ,"rebrand")]/div[2]/div[1]/h3/a/@href'
    xp_offers = '//*[contains(@class ,"listing") and contains(@class ,"rebrand")]//a[@class="property_title"]/@href'

    while r >= rr:

        #madrid
        #url = 'https://www.tripadvisor.es/RestaurantSearch?Action=PAGE&geo=187514&ajax=1&sortOrder=availability&o=a'+str(i)+'&availSearchEnabled=true'

        #barcelona
        #url = 'https://www.tripadvisor.es/RestaurantSearch?Action=PAGE&geo=187497&ajax=1&sortOrder=availability&o=a'+str(i)+'&availSearchEnabled=true'

        #shanghai https://www.tripadvisor.es/Restaurants-g308272-Shanghai.html
        #https://www.tripadvisor.es/RestaurantSearch?Action=FILTER&geo=308272&ajax=1&itags=10591&sortOrder=popularity&availSearchEnabled=false
        url = 'https://www.tripadvisor.es/RestaurantSearch?Action=PAGE&geo=308272&ajax=1&sortOrder=availability&o=a'+str(i)+'&availSearchEnabled=true'

        page = getUrl(url)
        print url


        tree = etree.HTML(page)
        offers = tree.xpath(xp_offers)
        print len(offers),':::::::::'

        data = []
        for o in offers:
            print o
            js = parseOfferJson(o)
            jsf = flatten(js)
            data.append( jsf )
            time.sleep(0.2)

        saveToCsv(data)

        #para salir del loop
        if len(offers) < rr:
            r = len(offers)
            print 'exit loop because no results'
        else:
            i += 30
            saveLast(i)

    return


###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

outputfile = 'tripadvisor_shg.csv'
a = None
while a is None:
    a = findOffers()
    time.sleep(1)