# This file is intended to store some globally used methods. For now it has the basic goose method to get article,
# methods to get time from three websites seperately, and a method to transform date to a string of number, in order to
# compare with other times to see which one is earlier. Their will be more methods here if other funtions are needed or
# other websites are given


from goose3 import Goose
from bs4 import BeautifulSoup
import datetime,time

def goose_by_url(url):
    g = Goose()
    article = g.extract(url=url)
    return article

# <meta content="2019-08-23T14:08:16+1000" property="og:updated_time"/>
# <meta content="2019-08-23T10:45:44+1000" property="article:published_time"/>
def find_time_abc(url):
    #print('find_time_abc')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        #print(meta)
        if not meta.get('property') == None:
            if 'published_time' in meta.get('property'):
                return (meta.get('content'))


# <time class="signature__datetime" content="2019-08-23T12:00:00+10:00"
# datetime="2019-08-23T12:00:00+10:00" itemprop="datePublished">August 23 2019 - 12:00PM</time>
def find_time_cbt(url):
    # print('find_time_cbt')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('time')
    for meta in metas:
        # print(meta)
        time = meta.get('datetime')
        if '-' in time:
            return (time)
        # return '0-0-0T0:0:00+11:00'


# <meta content="2019-08-23T05:25:20+10:00" itemprop="datePublished"/>
def find_time_sbs(url):
    # print('===find_time_sbs===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        # print(meta)
        if not meta.get('itemprop') == None:
            if 'datePublished' in meta.get('itemprop'):
                time = meta.get('content')
                return (time)

# <meta content="2019-08-15T14:51:26+10:00" property="article:published_time"/>
# <meta content="2019-08-15T15:18:12+10:00" property="article:modified_time"/>
def find_time_uc(url):
    # print('===find_time_uc===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        # print(meta)
        if meta.get('property') != None:
            if 'published_time' in meta.get('property'):
                # print(meta.get('content'))
                time = meta.get('content')
                return time
        # else:
        #     print('none in uc')

# has no time stamp so currently hard coded as '0-0-0T0:0:00+11:00' '1990-01-01T12:00:00+10:00'
def find_time_hercbr(url):
    return '1990-01-01T01:00:00+11:00'
    # print('===find_time_hercbr===')
    # g = Goose()
    # page = g.extract(url=url)
    # soup = BeautifulSoup(page.raw_html, 'lxml')
    # metas = soup.find_all('meta')
    # for meta in metas:
    #     print(meta)
    #     if not meta.get('itemprop') == None:
    #         if 'datePublished' in meta.get('itemprop'):
    #             time = meta.get('content')
    #             return (time)

def find_time_tidbinbilla(url):
    # print('===find_time_uc===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        if meta.get('name') != None:
            if 'modified' in meta.get('name'):
                time1 = meta.get('content')
                time2='T10:49:00+10:00'
                fulltime=time1+time2
    return fulltime

def find_time_cmag(url):
    # print('===find_time_uc===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        # print(meta)
        if meta.get('property') != None:
            if 'og:updated_time' in meta.get('property'):
                # print(meta.get('content'))
                time = meta.get('content')
                return time


def time_to_num(time):
    if '-' in time and 'T' in time and '+' in time:
        time = time[:-5].replace('-', '').replace(':', '').replace('T', '').replace('+', '')
        return time

# print('foo',time_to_num('2019-03-25T11:36:02+11:00'))