import csv
from tinydb import TinyDB, Query

db = TinyDB('tripadvisor3.json')
urls=[]
with open('tripadvisor_shg.csv', 'r') as f:
    for r in f.readlines():
        d = eval(r)
        db.insert(d)