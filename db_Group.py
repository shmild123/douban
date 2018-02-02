#coding=utf-8
import requests,time,os
from queue import Queue
from bs4 import BeautifulSoup

DOWNLOAD_URL="https://www.douban.com/group/cat/"

def download_page(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36' }
    data = requests.get(url, headers=headers).content.decode('utf-8')
    time.sleep(10)
    return data

def prase_html(html):
    soup=BeautifulSoup(html,"lxml")
    items=soup.find_all('td',attrs={'class':'title'})
    q=Queue()
    for item in items:
        temp=[item.find('a')['href'],item.find('a').getText()]
        q.put(temp)
    return q

def crawler(items):
    ROOT_DIR = "E:\Gabriel\PythonProject\Crawler\\"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    olditem_f=ROOT_DIR+"db"
    with open(olditem_f,"r") as f:
        olditems=[]
        for i in f:
            if i == "\n":
                break
            olditems.append(i)
    while items.qsize():
        try:
            item=items.get(timeout=5)
        except:
            break
        url=item[0]
        url_id=url.split("/")[-2]
        if url_id in olditems:
            continue
        else:
            olditems.append(url_id)
            download_dir=ROOT_DIR+"dbpic\\"+item[1]
            try:
                os.mkdir(download_dir)
            except:
                pass
            html=download_page(url)
            soup=BeautifulSoup(html,"lxml")
            pics=soup.find_all("div",attrs={"class":"topic-figure cc"})
            if pics==[]:
                try:
                    os.rmdir(download_dir)
                except:
                    pass
                continue
            else:
                n=0
                for i in pics:
                    print(i)
                    data_url=i.find("img")["src"]
                    with open(download_dir+"\\%03d."%n+data_url.split(".")[-1],"wb") as f:
                        f.write(requests.get(data_url,headers=headers).content)
                        n+=1
                        time.sleep(10)
    with open(olditem_f,"w") as f:
        olditems=set(olditems)
        for i in olditems:
            f.write(i)

def main():
    html=download_page(DOWNLOAD_URL)
    items=prase_html(html)
    crawler(items)
    


if __name__ == '__main__':
    main()
