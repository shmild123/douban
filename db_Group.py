#coding=utf-8
import requests,time
from queue import Queue
from bs4 import BeautifulSoup

DOWNLOAD_URL="https://www.douban.com/group/cat/"

def download_page(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36' }
    data = requests.get(url, headers=headers).content.decode('utf-8')
    return data

def prase_html(html):
    soup=BeautifulSoup(html)
    items=soup.find_all('td',attrs={'class':'title'})
    q=Queue()
    for item in items:
        temp=[item.find('a')['href'],item.find('a').getText()]
        q.put(temp)
    return q

def main():
    html=download_page(DOWNLOAD_URL)
    q=prase_html(html)
    while q.qsize():
        item=q.get(timeout=5)
        print(item[0])
        print(item[1])
    


if __name__ == '__main__':
    main()
