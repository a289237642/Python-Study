# coding:utf-8
import threading, queue
import time
import csv
import urllib.parse
from lxml import etree
import subprocess
from bs4 import BeautifulSoup
from RedisQueue import RedisQueue
from datetime import date
import codecs


def download_data(url, num_retries=2):
    # print('download url ',url)
    print("消费url ", url)
    out_bytes = subprocess.check_output(['phantomjs', './code.js', str(url,encoding="utf-8")])
    out_text = out_bytes.decode('utf-8')
    dom_tree = etree.HTML(out_text)
    links = dom_tree.xpath('//div[@class="company_info_text"]/span/text()')
    name = dom_tree.xpath('//div[@class="baseinfo-module-content-value-fr baseinfo-module-content-value"]/a[@class="ng-binding ng-scope"]/text()')
    print("公司法人是%s" % name)
    company_name = dom_tree.xpath('//div[@class="company_info_text"]/p/text()')
    # print(name)
    # print(len(links))
    if (len(links) > 0 and len(name) > 0 and len(company_name) > 0):
        '''
        print('links[0] 的值是'+links[0])
        print('links[1] 的值是'+links[1])
        print('links[2] 的值是'+links[2])
        print('links[3] 的值是'+links[3])
        print('links[4] 的值是'+links[4])
        print('links[9] 的值是'+links[9])

        for i in links:
           print(i)
        '''
        print('公司的值是' + company_name[0])
        # print('公司的url是'+ company_url)
        print('电话的值是' + links[1])
        print('邮箱的值是' + links[3])
        # print('地址的值是' + links[9])
        filename=str(date.today())+'.csv'
        print("------------------------------我是分割线---------------------------------")
        csv_file = open(filename, 'a', newline='', encoding='GB18030')
        try:
            writer = csv.writer(csv_file)
            writer.writerow((company_name[0], name[0], links[1], links[3]))
        except Exception as e:
            if num_retries > 0:
                print("正在进行数据下载重试操作！！！", num_retries - 1)
                download_data(url, num_retries - 1)
            else:
                print("重试失败，把%s 重新放入队列" % url)
                url_queue.put(url)
        finally:
            csv_file.close()
    else:
        if num_retries > 0:
            print("正在进行数据下载重试操作！！！", num_retries - 1)
            download_data(url, num_retries - 1)


def download_url(company_name, num_retries=2):
    out_bytes = subprocess.check_output(['phantomjs', './url.js',
                                         "http://www.tianyancha.com/search?key=" + urllib.parse.quote(
                                             company_name) + "&checkFrom=searchBox"])
    out_text = out_bytes.decode('utf-8')
    html = BeautifulSoup(out_text, "lxml")
    soup = html.find("a", {"class": {"query_name", "search-new-color"}})
    try:
        company_url = soup.attrs['href']
        url_queue.put(company_url)
        print("生产url ", company_url)
    except Exception as e:
        print(e)
        if num_retries > 0:
            print("正在进行url下载重试操作！！！", num_retries - 1)
            download_url(company_name, num_retries - 1)
        else:
            print("重试失败，把%s 重新放入队列" % company_name)
            name_queue.put(company_name)
    time.sleep(2)


def url_consumer(url_queue):
    while True:
        company_url = url_queue.get()
        download_data(company_url, 5)
        time.sleep(2)
    url_queue.task_done()


def url_producer(name_queue, url_queue):
    while True:
        company_name = name_queue.get()
        download_url(company_name, 5)


#name_queue = queue.Queue()
i=0
name_queue=RedisQueue("name"+str(i+1))
csv_reader = csv.reader(open('./company.csv', encoding="utf8"))
for row in csv_reader:

    name_queue.put(row[0])
url_queue = RedisQueue("url"+str(i+1))
for n in range(4):
    producer_thread = threading.Thread(target=url_producer, args=(name_queue, url_queue,))
    producer_thread.start()
for n in range(5):
    consumer_thread = threading.Thread(target=url_consumer, args=(url_queue,))
    consumer_thread.start()
#url_queue.join()