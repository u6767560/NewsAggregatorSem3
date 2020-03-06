import feedparser
import requests
from bs4 import BeautifulSoup
import re
url = "https://www.canberra.edu.au/config/monitor-landing-page-assets/rss-feeds"
one_page_dict = feedparser.parse(url)
for k in range(len(one_page_dict["entries"])):
    link = (one_page_dict["entries"][k]["link"])
    page = requests.get(link)
    text = page.content.decode('utf-8')
    soup = BeautifulSoup(text, 'lxml')
    if soup.find_all(attrs={'id':re.compile('new_content_container.')})==[]:
        print(soup.find_all(attrs={'id':re.compile('new_content_container.')}))
        middle = soup.find(attrs={'id':re.compile('content_container.')}).get_text()
    else:
        middle = soup.find_all(attrs={'id':re.compile('new_content_container.')})
    cross = []
    right = []
    for i in range(len(middle)):
        if middle[i] == "#":
            cross.append(i)
        if middle[i] == "}":
            j = i
    if cross != []:
        final = middle[0:cross[0]]+middle[j+1:]
    else:
        final = middle
    dr = re.compile(r'<[^>]+>', re.S)
    final = dr.sub('', str(final))
    with open("result "+str(k)+" .txt", 'w',encoding= "utf-8") as f:
        f.write(final)