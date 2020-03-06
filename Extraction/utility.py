# This file is intended to store some globally used methods. For now it has the basic goose method to get article,
# methods to get time from three websites seperately, and a method to transform date to a string of number, in order to
# compare with other times to see which one is earlier. Their will be more methods here if other funtions are needed or
# other websites are given
#Following source do not have particular timestamp,use a default one
# "http://www.canberrahouse.com.au/",
# "https://www.anbg.gov.au/gardens/",
# "https://visitcanberra.com.au/",
# "https://www.library.act.gov.au/",
# "https://experienceais.com/",
# "https://llewellynhall.com.au/",
# "https://www.nccc.com.au/",
# "http://lovethephoenix.com/",
# "https://www.smithsalternative.com/",
# "http://www.cimf.org.au/",
# "https://www.canberraopera.org.au/",
# "http://www.actrsl.org.au/",
# "https://www.4lyfe.org.au/",
# "http://actwildlife.net/",
# "http://www.canberraconvention.com.au/",
# "https://canberraglassworks.com/",
# "http://clug.org.au/",
# "https://www.actlabor.org.au/",
# "http://www.events.act.gov.au/whats-on-in-canberra"
# "http://www.hansard.act.gov.au/hansard/qtime/default.htm",
# "https://www.nla.gov.au/"
# "https://www.portrait.gov.au/",
# "https://www.awm.gov.au/",
# "https://www.cdscc.nasa.gov/",
# "https://epetitions.act.gov.au/CurrentEPetitions.aspx"

from goose3 import Goose
from bs4 import BeautifulSoup
import datetime,time

from PythonFlask.Extraction import Catch_Canberra_WithoutRSS


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
def find_time_general(url):
    time1 = time.strftime("%Y-%m-%d ", time.localtime()).rstrip()
    time2 = 'T00:49:00+10:00'
    fulltime = time1 + time2
    return fulltime
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

def find_time_national_arboretum(url):
    # print('===find_time_nationalarboretum===')
    time1 = time.strftime("%Y-%m-%d ", time.localtime()).rstrip()
    time2 = 'T00:49:00+10:00'
    fulltime = time1 + time2
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


#This is text
def find_time_bom(url):
    # print('===find_time_bom===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    #print(soup)
    metas = soup.find_all('p')
    for meta in metas:
        if meta.get('id') != None:
            if 'timestamp' in meta.get('id'):
                time1 = meta.get_text()
                #time2='T10:49:00+10:00'
                #fulltime=time1+time2
    #This is text
    return time1

def find_time_multi_cultural_festival(url):
    # print('===find_time_multiculturalfestival===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        if meta.get('name') != None:
            if 'date' in meta.get('name'):
                time1 = meta.get('content')
                time2='T10:49:00+10:00'
                fulltime=time1+time2
    return fulltime


def find_time_nca(url):
    # print('===find_time_nca===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        if meta.get('name') != None:
            if 'date' in meta.get('name'):
                time1 = meta.get('content')
                time2 = ':00'
                fulltime =  + time2
    return fulltime

#This is text
def find_time_unsw(url):
    # print('===find_time_unsw===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('p')
    #This is text
    return (metas[-1].get_text())


#This is text
def find_time_iconwater(url):
    # print('===find_time_iconwater===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('p')
    for meta in metas:
        #print(meta)
        if meta.get('class') != None:
            if 'date' in meta.get('class'):
                fulltime = meta.get_text()
                break
    return fulltime

#Warn,this is without test
def find_time_greens(url):
    # print('===find_time_greens===')
    g = Goose()
    newslist=Catch_Canberra_WithoutRSS.catch_ACT_Greens()
    page = g.extract(url=newslist[0])
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        #print(meta)
        if meta.get('property') != None:
            if 'modified' in meta.get('property'):
                fulltime = meta.get('content')
                break
    F = list(fulltime)
    F.insert(22, ':')
    time = "".join(F)
    return time

#Warn,this is without test
def find_time_thestreet(url):
    # print('===find_time_thestreet===')
    g = Goose()
    newslist = Catch_Canberra_WithoutRSS.catch_The_Street_Theatre()
    page = g.extract(url=newslist[0])
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        #print(meta)
        if meta.get('property') != None:
            if 'modified' in meta.get('property'):
                fulltime = meta.get('content')
                break
    return fulltime

#Warn,this is without test
def find_time_anu(url):
    # print('===find_time_anu===')
    g = Goose()
    newslist = Catch_Canberra_WithoutRSS.catch_The_Australian_National_University()
    page = g.extract(url=newslist[0])
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        #print(meta)
        if meta.get('property') != None:
            if 'modified' in meta.get('property'):
                fulltime = meta.get('content')
                break
    return fulltime

def find_time_moadoph(url):
    # print('===find_time_moadoph===')
    g = Goose()
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    metas = soup.find_all('meta')
    for meta in metas:
        #print(meta)
        if meta.get('property') != None:
            if 'updated' in meta.get('property'):
                fulltime = meta.get('content')
                break
    #print(fulltime)
    return fulltime



def time_to_num(time):
    if '-' in time and 'T' in time and '+' in time:
        time = time[:-5].replace('-', '').replace(':', '').replace('T', '').replace('+', '')
        return time

# print('foo',time_to_num('2019-03-25T11:36:02+11:00'))

