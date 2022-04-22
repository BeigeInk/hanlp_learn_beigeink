import os, re
import requests
from bs4 import BeautifulSoup


def get_index(url, page):
    title = list()
    url_t = list()
    a = requests.get(url + page)
    soup = BeautifulSoup(a.content, 'html.parser')
    for i in soup.find_all(class_="SubImgIntroVerticalBox_verticalBox__1upWr"):
        title.append(i.text)
        url_t.append(eval(i['data-da'])["ext"]['url'])
        # print(i['url'])
    return title, url_t


def get_info(url):
    # print(url)
    a = requests.get(url)
    soup = BeautifulSoup(a.content, 'html.parser')
    # page_title=soup.find(class_="rich_media_title").text
    # print(page_title)
    get_soup = soup.find(class_="rich_media_content")
    return get_soup.text


def to_file(pagename, str_whole):
    with open('../data/' + pagename + '.txt', 'w+', encoding='utf-8') as f:
        f.write(str_whole)


if __name__ == '__main__':
    for k in range(3, 11):
        url = 'https://portal.dxy.cn/list/' + str(k) + '?page='
        for i in range(1, 10):
            title, t_url = get_index(url, str(i))
            print(i, '页')
            for j in range(len(title)):
                try:
                    str_temp = get_info(t_url[j])
                    to_file(title[j], str_temp)
                except:
                    print(t_url[j])
