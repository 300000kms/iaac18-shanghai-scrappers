#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinydb import TinyDB, Query
import sqlite3
import pprint
from flatten_dict import flatten

################################################################
################################################################

def underscore_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return k1 + "__" + k2

def tostr(n):
    if type(n)==list:
        return str(n)
    else:
        return n

pp= pprint.PrettyPrinter(indent=4)

################################################################
################################################################



sdb = "meituan.sqlite"
tdb = TinyDB("06 resto_meituan/meituan_rest.json")

sdb = "bonapp.sqlite"
tdb = TinyDB("04 bonapp/restaurants.json")

sdb = "dianping.sqlite"
tdb = TinyDB("07 dianping_food/dianping.json")

sdb = "mealbay.sqlite"
tdb = TinyDB("03 mealbay/mealbay.json")

sdb = "waimay.sqlite"
tdb = TinyDB("05 waimai/waimay_4.json")

sdb = "tripadvisor.sqlite"
tdb = TinyDB("02 tripadvisor/tripadvisor.json")

################################################################
################################################################

table = sdb.split('/')[-1].split('.')[0]

print '>rows :',len(tdb)

keys=[]
for d in tdb:
    k = flatten(d, reducer=underscore_reducer).keys()
    keys= keys+k

sk = set(keys)

print '>fields :', sk
print '>nfields :', len(sk)

conn = sqlite3.connect(sdb)
c = conn.cursor()
c.execute('''create table if not exists %s (%s)''' %(sdb.split('/')[-1].split('.')[0], ', '.join(sk).replace('@', '')) )
conn.commit()

for d in tdb:
    d = flatten(d, reducer=underscore_reducer)
    keys   = ', '.join(d.keys()).replace('@', '')
    values = ', '.join(['?' for dd in d.values()])
    sql =  '''insert into %s (%s) values (%s)''' %(table, keys, values)
    print sql
    print tuple(d.values())
    c.execute(sql,  tuple([tostr(dd) for dd in d.values()]) )

conn.commit()


