import requests
import pprint
from tinydb import TinyDB, Query

pp= pprint.PrettyPrinter(indent=4)

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
db = TinyDB('meituan_rest2.json')
n = getLastId()
while n != False:
    url ='http://sh.meituan.com/meishi/api/poi/getPoiList?cityName=%E4%B8%8A%E6%B5%B7'
    url += '&cateId=0'
    url += '&areaId=0'
    url += '&sort='
    url += '&dinnerCountAttrId='
    url += '&page=%s' %(n)

    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'es-ES,es;q=0.8,ca;q=0.6,en;q=0.4,en-US;q=0.2'
    headers['Connection'] = 'keep-alive'
    #headers['Content-Length'] = '298'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Cookie'] = '_lxsdk_cuid=15fe8a9e74fc8-084f16cccf69c1-38710357-1fa400-15fe8a9e74fc8; uuid=18411b2d35f0f14ce708.1511436967.0.0.0; oc=q64SELCp-w4Wsogs5zn9f94OUON62VTtEjJ3RNDDnpQnscyJAgAhKUD5ehXgA7zwoSfrYSt9SRmzKyImpyOwfoKTFxgWT4uaUktTyGbNRWCv8fCuBXByFzVgnCStv7W2EC1yDHFiqAvPQzw38izdLKwOLhC8UcSFI2-zIj-ysQQ; __utma=211559370.1590768404.1511436972.1511436972.1511436972.1; __utmz=211559370.1511436972.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=211559370.|1=city=beijing=1; rvct=10%2C1; iuuid=06F1CF955CEFDCC446070EBEEC4D14A35125EE4103F8ED913E1718D95B5EDEBA; ci=10; cityname=%E4%B8%8A%E6%B5%B7; _ga=GA1.2.2026437677.1511271623; _gid=GA1.2.1073776190.1513702216; __mta=250347449.1513608239659.1513608239659.1513759913842.2; lat=31.27045; lng=121.41127; _lxsdk_s=160731e03a4-aea-6bd-65d%7C%7C30; __mta=250347449.1513608239659.1513759913842.1513760498476.3; client-id=6d2de50e-a444-4239-b870-402fc495af10'
    headers['Host'] = 'sh.meituan.com' #este es clave
    #headers['Origin'] = 'http://waimai.meituan.com'
    #headers['Referer'] = 'http://waimai.meituan.com/home/wtw3sy6j4ndu'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    print url
    r = requests.get(url, headers=headers)
    print r.status_code, len(r.json()['data']['poiInfos'])

    #pp.pprint(r.json())
    js =r.json()
    print js
    for j in js['data']['poiInfos']:
        print j
        db.insert(j)

    n += 1
    saveId(n)
    if len(r.json()['data']['poiInfos'])==0:
        n = False



