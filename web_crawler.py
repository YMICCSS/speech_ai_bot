import requests
from bs4 import  BeautifulSoup
import datetime

def craw():
    get_datetime = datetime.datetime.now()
    month = get_datetime.month
    year = get_datetime.year
    headers =  {
        "Host":"這裡要輸入host name",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip,deflate,br",
        "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
        "Origin":"null",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "Cache-Control":"max-age=0",
        "Content-Length":"76",
        "Cookie": "PHPSESSID=b0e10710426bc0997b9bede42d8ae55e;TawkConnectionTime=0"
    }
    my_data = {'srh_area': 'all', 'srh_ptype': 'all',"srh_gid":"all","srh_time":"all","srh_time":'all',"srh_quota":"all",
               "y":str(year),"m":str(month)}
    response = requests.post("這裡輸入爬蟲網址",headers=headers,data = my_data)
    soup = BeautifulSoup(response.text, "lxml")
    result = soup.find_all(class_="m-show")
    # find的型態是<class 'bs4.element.Tag'>
    # find_all後list中的子物件的型態也是<class 'bs4.element.Tag'>，所以可以用find的方法找到屬性或文字
    lessions=[]
    for item in result:
        date = item.find(class_="date").text
        c_d = item.find_all(class_="c_d")
        for item in c_d:
            data = []
            data.append(date)
            data.append(item.text)
            lessions.append(data)
    return lessions
