import threading
import time
import requests
from bs4 import BeautifulSoup
import urllib3


url1 = 'https://www.kay.com/rings/diamond-rings/c/9000000091?icid=MM:RINGS:DIAMOND&loadMore=2'
url2 = 'https://www.kay.com/rings/gemstone-rings/c/9000000092?icid=MM:RINGS:GEMSTONE'
url3 = 'https://www.kay.com/rings/lab-created-diamond-rings/c/9000001470?icid=MM:RINGS:LCD'
url4 = 'https://www.kay.com/rings/platinum-rings/c/9000000095?icid=MM:RINGS:PLATINUM'
url5 = 'https://www.kay.com/rings/pearl-rings/c/9000000093?icid=MM:RINGS:PEARL'
url6 = 'https://www.kay.com/rings/silver-rings/c/9000000096?icid=MM:RING:SILVER'
url7 = 'https://www.kay.com/rings/white-gold-rings/c/9000001472?icid=MM:RINGS:WHITEGOLD'
url8 = 'https://www.kay.com/rings/gold-rings/c/9000000094?icid=MM:RINGS:YELLOWGOLD'


class myThread (threading.Thread):
    def __init__(self, threadID, url, index):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.index = index
    def run(self):
        print ("开始线程：" + str(self.threadID))
        getData(self.url,self.index)
        print ("退出线程：" + str(self.threadID))

def getHtml(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        r = requests.get(url=url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        print('success')
        return r
    except Exception as e:
        print(r.status_code)
        print('faild')
        print(e)
        return ""
def getImg(url):
    try:
        urllib3.disable_warnings()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        r = requests.get(url=url, timeout=30, headers=headers,verify=False)
        r.raise_for_status()
        print(r.status_code)
        return r.content
    except Exception as e:
        print(e)
        return "-1"
def getData(url,index):
    info = []
    html = getHtml(url).text #获取网页html
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.find('ul', {'class', 'product-listing product-grid'}).select('li')
    for i in product_list:
        #print()
        price = i.find('div', {'class', 'price'}).text.strip('\n').strip(' ')
        pname = i.find('div', {'class', 'name'}).text.strip('\n').strip(' ')
        imgurl = 'https://www.kay.com' + i.find('img', {'class', 'img-responsive js-lazyload'}).get('data-original')
        img = getImg(imgurl)
        try:
            open('test'+str(index)+'.jpg','wb').write(img)
        except Exception as e:
            print(e)
        print(price)
        print(pname)
        print(imgurl)
        index += 1
# 创建新线程
thread1 = myThread(1,url1, 101)
thread2 = myThread(2,url2, 201)
thread3 = myThread(3,url3, 301)
thread4 = myThread(4,url4, 401)
thread5 = myThread(5,url6, 501)
thread6 = myThread(6,url6, 601)
thread7 = myThread(7,url7, 701)
thread8 = myThread(8,url8, 801)

# 开启新线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()

print ("退出主线程")
