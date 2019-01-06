from bs4 import BeautifulSoup
import requests
import threading
import datetime
import time

__author__ = 'JrD'

headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36"
           }


def get_proxy():
    of = open('proxy.txt', 'w+')
    for page in range(1, 10):
        html_doc = requests.get('http://www.xici.net.co/nn/' + str(page), headers=headers).text
        html_doc = html_doc.replace("\r\n", "").replace("\t", "").replace("\n", "")
        soup = BeautifulSoup(html_doc, "html.parser")
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            protocol = tds[5].text.strip()
            if protocol == 'HTTP' or protocol == 'HTTPS':
                of.write("%s\t%s\t%s" % (protocol.lower(), ip, port))
                of.write("\n")
    of.close()

def run(self):
    print(threading.current_thread().getName())
    with open('proxy_checked.txt', 'a+') as of:
        while b1:
            # lock.acquire()
            if len(b1) == 0:
                print('Finished')
                print(datetime.datetime.now())
                # lock.release()
                exit()
            c1 = b1.pop(0)
            c2 = b2.pop(0)
            c3 = b3.pop(0)
            # lock.release()
            proxies = {c1: 'http://%s:%s' % (c2,c3)}
            ip = '%s\t%s\t%s' % (c1,c2,c3)
            try:
                c = requests.get('http://www.baidu.com',proxies=proxies,timeout=1)
            except:
                print('%s connect failed' % ip)
            else:
                if  c.ok:
                    print ('%s connect success .......' % ip)
                    of.write(ip+'\n')
                else:
                    print ('%s connect failed' % ip)

if __name__ == "__main__":
    print(datetime.datetime.now())
    get_proxy()

    b1 = []
    b2 = []
    b3 = []
    with open('proxy.txt', 'r') as f:
        for a in f.readlines():
            b = a.split()
            b1.append(b[0])
            b2.append(b[1])
            b3.append(b[2])
    # for x in range(100):
    #     mythread = MyThread()
    #     mythread.start()

    #多线程另一种写法
    threads = []
    for i in range(100):
        t = threading.Thread(target=run, args=(i,))
        threads.append(t)
        t.start()