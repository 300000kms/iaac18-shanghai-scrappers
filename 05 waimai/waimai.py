'''
http://waimai.meituan.com/home/wtw3sy6j4ndu
http://waimai.meituan.com/home/wtw3sn178upv
'''

import requests
import pprint
from tinydb import TinyDB, Query
import time

pp= pprint.PrettyPrinter(indent=4)

def getPois(n):
    url = "http://waimai.meituan.com/ajax/poilist?_token=eJxNkttyokAURf+FVyjpK037phA1XnAkipFUHgS8EEQUATVT8+/TDRMdiipW99l7n0PDbyV/jZQ2BOJimlJtcqWtwBZoUUVTiouoUIg54YQxamJNCR97FFLAqSFMQe7ZSvsDmpRqxGCfcscVGx+QI6BBYIJP7X9GRNxS9SpEyr4oTm1dv67jdB230k1clOtjK8xSfZ+lG/1aXPHlCJlZnioxklRfpPx6be2ybHfYtDYXXRFp6VymEWZqjHAupDVSAJ+In2jUyCSyJzY2QyBETyRPbGxUovlABJ/Y2LBE8sTGhiQ2NigQNzYgsbYZcjJMa5TdcK01ZC6ptYYMI/VbGDKM1LmGDCONVoZRIJHKMFrnUhlG63GoDKO1jcoEyh9oNFoZZmB5oIk8UPFcPw4WEa7Zr57QiX4a5lp3aq/+NUMA/NQA1pCYr1kRxjXxZzxW4tvznxrEYiV25Eo0Kn4aTsQ/KMqXeHcUtBnenK8Qjq6gs3AL9RCrt0tyPju9ZeCCE1/0OtAb9ZnFNrO0mlt+GrJwvbhvcbLvllU1JWEHJ7uzeWJZVQZhNrStZdZzk4G9TCp6fXNRwAaTMFp0LiA4vZBdl46B6Q8AGofh+7aK/Ix338vp2HZXaZ6juzV0QFyw8mythp0JgeXXywzNvLAPwxEJrCSc59FtSIm+17uo0pNfc9+epM5ivdp/393q4PRHznC1VJN+fzZ877x5Ix5svweUzVS6dXznWJz4cULGg2hvHUpcmaUdlWqOewjdZmpRsWk8cv17ovtedMjU6syWGTTRduklyp+/s8f5PQ=="

    ##
    headers = {}
    headers['user-agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
    headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'es-ES,es;q=0.8,ca;q=0.6,en;q=0.4,en-US;q=0.2'
    headers['Connection'] = 'keep-alive'
    headers['Content-Length'] = '298'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Cookie']  = 'w_uuid=e20dMGsPT6fqHA979JgXAabDSu6aIrX-HunrOEHrzIQxiFZ7QgQBcG1yd7qD5LEF; _lxsdk_cuid=15fe8a9e74fc8-084f16cccf69c1-38710357-1fa400-15fe8a9e74fc8; uuid=18411b2d35f0f14ce708.1511436967.0.0.0; oc=q64SELCp-w4Wsogs5zn9f94OUON62VTtEjJ3RNDDnpQnscyJAgAhKUD5ehXgA7zwoSfrYSt9SRmzKyImpyOwfoKTFxgWT4uaUktTyGbNRWCv8fCuBXByFzVgnCStv7W2EC1yDHFiqAvPQzw38izdLKwOLhC8UcSFI2-zIj-ysQQ; __utma=211559370.1590768404.1511436972.1511436972.1511436972.1; __utmz=211559370.1511436972.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=211559370.|1=city=beijing=1; rvct=10%2C1; iuuid=06F1CF955CEFDCC446070EBEEC4D14A35125EE4103F8ED913E1718D95B5EDEBA; ci=10; cityname=%E4%B8%8A%E6%B5%B7; _ga=GA1.2.2026437677.1511271623; __mta=250347449.1513608239659.1513608239659.1513759913842.2; w_cid=310101; w_cpy_cn="%E9%BB%84%E6%B5%A6%E5%8C%BA"; w_cpy=huangpuqu; waddrname=Tomatito; w_geoid=wtw3sn178upv; w_ah="31.234753970056772,121.46660294383764,Tomatito|31.236397996544838,121.50063883513212,El%2BWilly"; JSESSIONID=ofbg55a3oys6vkcrvyt4xa4t; _ga=GA1.3.2026437677.1511271623; _gid=GA1.3.932174163.1513949468; __mta=250347449.1513608239659.1513759913842.1513949477809.3; w_visitid=22962d40-bd49-46b4-b8c9-3121d126d2c6; w_utmz="utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)"'
    headers['Host']    = 'waimai.meituan.com'
    headers['Origin']  = 'http://waimai.meituan.com'
    headers['Referer'] = 'http://waimai.meituan.com/home/wtw3sn178upv'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    ##
    data={}
    data['classify_type']='cate_all'
    data['sort_type']='0'
    data['price_type']='0'
    data['support_online_pay']='0'
    data['support_invoice']='0'
    data['support_logistic']='0'
    data['page_offset']=str(n)
    data['page_size']='20'
    data['uuid']='e20dMGsPT6fqHA979JgXAabDSu6aIrX-HunrOEHrzIQxiFZ7QgQBcG1yd7qD5LEF'
    data['platform']='1'
    data['partner']='4'
    data['originUrl']='http%3A%2F%2Fwaimai.meituan.com%2Fhome%2Fwtw3sn178upv'

    ##
    r = requests.post(url, headers=headers,  data=data)
    return r.json()['data']['poiList']


db = TinyDB('waimay.json')
n=1
while True:
    try:
        pois = getPois(n)
        print len(pois)
        for p in pois:
            print p
            db.insert(p)
        n +=20
        time.sleep(1)
        print n
    except:
        print 'error on :', n




