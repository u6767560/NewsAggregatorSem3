from goose3 import Goose
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re
import urllib.request
import platform

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time
import datetime
from urllib.parse import unquote


news_urls = ["https://www.canberra.edu.au/uncover",
"http://www.cmag.com.au/",
"https://www.tidbinbilla.act.gov.au/",
"https://www.anbg.gov.au/gardens/",
"https://www.nationalarboretum.act.gov.au/",
"http://www.canberrahouse.com.au/",
"https://visitcanberra.com.au/",
"http://www.bom.gov.au/act/forecasts/canberra.shtml?ref=hdr",
"https://www.multiculturalfestival.com.au/home",
"https://www.library.act.gov.au/",
"https://experienceais.com/",
"https://llewellynhall.com.au/",
"https://www.nccc.com.au/",
"http://lovethephoenix.com/",
"https://www.nca.gov.au/",
"https://www.smithsalternative.com/",
"http://www.cimf.org.au/",
"https://www.canberraopera.org.au/",
"https://www.unsw.adfa.edu.au/",
"http://www.actrsl.org.au/",
"https://www.4lyfe.org.au/",
"http://actwildlife.net/",
"http://www.canberraconvention.com.au/",
"https://canberraglassworks.com/",
"https://www.iconwater.com.au/Media-Centre/Media-Releases.aspx",
"http://clug.org.au/",
"https://www.actlabor.org.au/",
"https://greens.org.au/act/news",
"http://www.events.act.gov.au/whats-on-in-canberra",
"http://www.hansard.act.gov.au/hansard/qtime/default.htm",
"http://www.thestreet.org.au/",
"http://www.anu.edu.au/",
"https://www.nla.gov.au/",
"https://www.portrait.gov.au/",
"https://www.awm.gov.au/",
"https://www.moadoph.gov.au/",
"https://www.cdscc.nasa.gov/",
"https://epetitions.act.gov.au/CurrentEPetitions.aspx"
]
pltform = platform.platform()
if 'Windows' not in pltform:
    driver_url = 'chromedriver_linux64'
else:
    driver_url = 'chromedriver.exe'
    
chrome_option = Options()
chrome_option.add_argument('--headless')


def get_links_dynamic(website_url, driver_url) -> list:
    links = set()
    driver = webdriver.Chrome(driver_url, chrome_options=chrome_option)
    driver.get(website_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for line in soup.find_all('a'):
        link = line.get('href')
        if link is not None:
            # very few start with empty space in the head, so delete it
            link = link.strip(' ')
            links.add(link)
    return list(links)


def get_links_via_option(website_url, driver_url, x_path, executioin_count) -> list:
    links = set()
    driver = webdriver.Chrome(driver_url, chrome_options=chrome_option)
    driver.get(website_url)

    for i in range(executioin_count):
        driver.find_element_by_xpath(x_path).click()
        time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    for line in soup.find_all('a'):
        link = line.get('href')
        if link is not None:
            # very few start with empty space in the head, so delete it
            link = link.strip(' ')
            links.add(link)
    return list(links)



def get_links(website_url : str) -> list:
    '''
        It used to get the links in a web page
    :param website_url: the URL of website that is going to be extracted
    :return: a link list, after a rough selection
    '''
    links = set()
    # create goose and bs4 instance,
    g = Goose()
    try:
        main_page = g.extract(url=website_url)
        soup = BeautifulSoup(main_page.raw_html, 'lxml')
        # Get the link
        for line in soup.find_all('a'):
            link = line.get('href')
            if link is not None:
                # very few start with empty space in the head, so delete it
                link = link.strip(' ')
                links.add(link)
        print('Extracted: ', website_url)
    except Exception as e:
        # Print the error message if failed to extract
        print('Fail to extract: ', website_url, '   Error:', str(e))
    if len(links) == 0:
        print('Warning! Function: get_links() output empty list when extracting ', website_url)
    return list(links)



def get_selected_links(website_url : str) -> list:
    '''
        Get better results, which means it will return the links that are very likely to be the article links
    :param website_url: The web page url
    :return: the article(very likely) links
    '''

    # Some use relative url, in order to return the full URL
    # Get the base_url first, if the link is relative, combine it with the base_url in front
    url_sections = website_url.split('/')
    base_url = website_url
    for part in url_sections:
        if 'www.' in part or '.au' in part or '.com' in part:
            base_url = url_sections[0] + '//' + part
            break

    # Get the basic urls for get_links() function
    links = get_links(website_url)
    selected_list = []

    # Indicates it could be an article link if this pattern matched in the last or second last level of the url
    #valid_pattern = re.compile(r'([^-]+)-([^-]+)-([^-]+)((-[^-])*)')
    valid_pattern = re.compile(r'([^-]+)(-([^-]+))+')

    # Indicates it could not be an article link if this pattern matched in the first or second level of the url
    invalid_pattern = re.compile(r'(contact).*|(author).*|(profile).*|(category).*|(about).*|(support).*|(terms).*', re.I)

    # Indicates it is not an article, not used now, might not work
    fobbiden_pool = {'facebook', 'linkedin', 'google', 'youtube', 'twitter'}

    if links is not None:
        for certain_link in links:
            if '?cs' not in certain_link and '?' in certain_link:
                # ?cs indicates an article link in some web page
                # ? only always indicates a link to the facebook, twitter, etc, so it's useless
                continue
            if len(certain_link) > 3 and '/' in certain_link:
                # remove the link that are obviously invalid
                with_base_url = False
                if 'www.' in certain_link or '.au' in certain_link or '.com' in certain_link:
                    # Detect a link whether it's a relative one
                    # If it's relative, attach the base_url in front of it
                    with_base_url = True
                sections = certain_link.split('/')
                detect_pos = 2 if with_base_url else 1 #Detect where to start to check the invalid pattern
                detect_targets = []
                detect_targets.append(sections[detect_pos])
                if detect_pos + 1 < len(sections): # Assure it will in the range
                    detect_targets.append(sections[detect_pos + 1])
                contain_invalid = False

                for target in detect_targets:
                    if re.match(invalid_pattern, target) is not None:
                        # if it matched the invalid pattern, record it and break
                        contain_invalid = True
                        break
                if contain_invalid:
                    # if contain_invalid, the this link should be skipped
                    continue

                if '.mp3' in sections[-1] or '.m4a' in sections[-1] or '.mp4' in sections[-1] or '.jpg' in sections[-1]:
                    # Skip the link if the last part of it contains .mp3 or such extension name
                    continue

                tail_index = -1
                if '#' in sections[-1]:
                    # if # in the last part, it always indicates it contains the comment part
                    pos = certain_link.find('#')
                    # if end with #comment, then delete #comment,
                    certain_link = certain_link[0: pos]
                while abs(tail_index) <= len(sections):
                    # It will detect pattern from the tail to the head
                    # Could limit it within last two or three level later, but not necessary
                    if re.match(valid_pattern, str(sections[tail_index])) is not None:
                        # The pattern matched
                        if not with_base_url:
                            # It's a relative URL
                            if certain_link[0] != '/':
                                # Very few cases, it does not contain / in the beginning
                                certain_link = '/' + certain_link
                            certain_link = base_url + certain_link # make it as a full URL
                        selected_list.append(certain_link)
                        break
                    else:
                        tail_index -= 1
        if len(links) == 0:
            print('Warning! Function: get_selected_links() output empty list when extracting ', website_url)
        return list(set(selected_list))
    print('Warning! Function: get_selected_links() output empty None ', website_url)
    return None


def catch_University_of_Canberra():
    url = 'https://www.canberra.edu.au/uncover'
    links = get_links(url)
    links_set = set()
    for link in links:
        key = 'https://www.canberra.edu.au/uncover/news-archive/20'
        pos = link.find(key)
        if pos != -1:
            links_set.add(link[pos:])
        print("john uc test :", len(links_set))
        for i in links_set:
            print(i)
    return list(links_set)


def catch_Canberra_Museum_and_Gallery():
    url = 'http://www.cmag.com.au/whats-on'
    links = get_links(url)
    links_set = set()
    if 'http://www.cmag.com.au/whats-on/page/2' in links:
        links.extend(get_links('http://www.cmag.com.au/whats-on/page/2'))
    for link in links:
        if 'events/' in link or 'exhibitions/' in link:
            links_set.add('http://www.cmag.com.au' + link)
    return list(links_set)


def catch_Tidbinbilla_Nature_Reserve():
    return ['https://www.tidbinbilla.act.gov.au/whats-on']


def catch_Australian_National_Botanical_Gardnes():
    url = 'https://parksaustralia.gov.au/botanic-gardens/do/whats-on/'
    url2 = 'https://parksaustralia.gov.au/botanic-gardens/do/whats-on/exhibitions/'
    links_set = set()
    for link in get_links(url):
        if '/botanic-gardens/do/whats-on/' in link and '?' not in link:
            links_set.add('https://parksaustralia.gov.au' + link)
    for link in get_links(url2):
        if '/botanic-gardens/do/whats-on/exhibitions/' in link and '?' not in link:
            links_set.add('https://parksaustralia.gov.au' + link)
    links_set.remove('https://parksaustralia.gov.au/botanic-gardens/do/whats-on/')
    links_set.remove('https://parksaustralia.gov.au/botanic-gardens/do/whats-on/exhibitions/')
    return list(links_set)


def catch_National_Aboretum_Canberra():
    url = 'https://www.nationalarboretum.act.gov.au/visit/whats_on'
    links = []
    for link in get_links(url):
        if 'https://www.nationalarboretum.act.gov.au/visit/whats_on/whatson-full-story/' in link:
            links.append(link)
    return links


def catch_Canberra_House():
    url = 'http://www.canberrahouse.com.au/'
    links = []
    for link in get_links(url):
        if 'houses' in link or 'people' in link:
            links.append('http://www.canberrahouse.com.au' + link)
    return links


def catch_Visit_Canberra():
    url = 'https://visitcanberra.com.au'
    links = []
    # Show More x_path
    x_path = '//*[@id="menu-pusher"]/div[1]/div/div[1]/div/div/div[1]/div/div[11]/a'
    for link in get_links_via_option(url, driver_url, x_path, 1):
        if 'https://visitcanberra.com.au/events' in link:
            links.append(link)
    return links


def catch_Canberra_Forecast():
    ''' Just return the link, it's the forecast, no warning message
    '''
    return ['http://www.bom.gov.au/act/forecasts/canberra.shtml?ref=hdr']


def catch_Multicultural_Festival():
    return ['https://www.multiculturalfestival.com.au/home']


# def catch_Libraries_ACT():
#     # it ends with https://www.library.act.gov.au/whats-on without /
#     # so with /, it must have following level
#     links = []
#     url = 'https://www.library.act.gov.au/whats-on/'
#     l1_links = get_links(url) # /whats-on/programs-for-families
#     for l1_link in l1_links:
#         if url in l1_link:
#             l1_link += l1_link + '/' # /whats-on/programs-for-families/
#             l2_links = get_links(l1_link)
#             for link in l2_links:
#                 if l1_link in link:
#                     links.append(link)
#     return links



def catch_Experience_AIS():
    url = 'https://experienceais.com'
    links = []
    for link in get_links(url):
        if '/whats-on/calendar/events/' in link:
            links.append('https://experienceais.com' + link)
    return links


def catch_Llewellyn_Hall():
    links = []
    url = 'http://llewellynhall.com.au/events?page='
    page = 0
    while True:
        # because it has many pages, it need to extract all events in all pages
        page_links = get_links(url + str(page))
        page += 1
        next_page = 'page=' + str(page)
        next_page_exist = False
        for link in page_links:
            if next_page in link:
                next_page_exist = True
            if '/events/' in link:
                links.append('http://llewellynhall.com.au' + link)
        if not next_page_exist:
            return links


def catch_National_Convention_Centre_Canberra():
    links = []
    url = 'https://www.nccc.com.au/'
    sub_urls = ['canberra-concerts-entertainment', 'whats-on-in-canberra']
    for sub_url in sub_urls:
        l2_url = url + sub_url
        for link in get_links(l2_url):
            if 'www.nccc.com.au/' in link:
                links.append(link)
    return links


def catch_The_Phoenix():
    # Nothing to show???
    return ['http://lovethephoenix.com/']


def catch_National_Capital_Authority():
    links = []
    url = 'https://www.nca.gov.au/about-the-nca/media-centre/media-releases'
    for link in get_links(url):
        sections = link.split('/')
        if len(sections) == 2 and sections[0] == '' and '-' in sections[1]:
            links.append('https://www.nca.gov.au' + link)
    links.remove('https://www.nca.gov.au/contact-us')
    return links


def catch_Smiths_Alternative():
    # requires dynamic extraction, webdriver
    url = 'https://www.smithsalternative.com/'

    links = []
    for link in get_links_dynamic(url, driver_url):
        if '/events/' in link:
            links.append('https://www.smithsalternative.com' + link)
    return links


def catch_Canberra_International_Music_Festival():
    links = set()
    date_year = str(datetime.datetime.now().year)
    url = 'http://www.cimf.org.au/' + date_year + '-whats-on'
    for link in get_links(url):
        if '/' + date_year + '-calendar/' in link:
            if '.au' not in link:
                link = 'http://www.cimf.org.au' + link
            links.add(link)
    return list(links)


def catch_Canberra_Opera():
    return ['https://www.canberraopera.org.au/events']


def catch_UNSW_Canberra():
    links = []
    url_news = 'https://www.unsw.adfa.edu.au/news'
    url_events = 'https://www.unsw.adfa.edu.au/events'
    x_path = '//*[@id="quickset-news"]/div/div[1]/div[2]/ul/li/a'
    execution_count = 5
    base_url = 'https://www.unsw.adfa.edu.au'
    try:
        for link in get_links_via_option(url_news, driver_url, x_path, execution_count):
            if base_url in link:
                count01 = link.count('/')
                if link[-1] == '/':
                    count01 -= 1
                if count01 == 3 and link.count('-') >= 1:
                    links.append(unquote(link))
    except Exception as e:
        pass
    for link in get_links(url_events):
        if base_url in link:
            count01 = link.count('/')
            if link[-1] == '/':
                count01 -= 1
            if count01 == 3 and link.count('-') >= 1:
                links.append(unquote(link))
    return links


def catch_RSL_ACT_Branch():
    links = []
    url1 = 'http://www.actrsl.org.au/meetings-and-events'
    # news have not been updated for a long time
    url2 = 'http://www.actrsl.org.au/news'
    base_url = 'http://www.actrsl.org.au'
    for link in get_links(url1):
        if '/meetings-and-events/' in link and '?format' not in link:
            links.append(base_url + link)
    return links


# def catch_4Lyfe_Rescue():
# I don't know what need to be extracted from this website
# def catch_ACT_Wildlife():
# ???????


def catch_Canberra_Convention_Bureau():
    links = []
    base_url = 'http://www.canberraconvention.com.au'
    url = 'http://www.canberraconvention.com.au/reports-and-media/'
    for link in get_links(url):
        if '?id' in link:
            links.append(base_url + link)
    return links


def catch_Canberra_Glassworks():
    return ['https://canberraglassworks.com/visit/exhibitions/future/', 'https://canberraglassworks.com/visit/exhibitions/current/', 'https://canberraglassworks.com/create/holidays/']


def catch_Icon_Water():
    links = []
    url = 'https://www.iconwater.com.au/Media-Centre/Media-Releases.aspx'
    for link in get_links(url):
        if 'Media-Releases/' in link:
            links.append(link)
    return links

def catch_Canberra_Linux_Users_Group():
    # no news or events, just a notification in the main page
    return ['http://clug.org.au/']


def catch_ACT_Labor():
    url = 'https://www.actlabor.org.au/events'
    links = []
    for link in get_links_dynamic(url, driver_url):
        if '/events/' in link and 'get-active' not in link and '.com' not in link and '.au' not in link and link.count('/') == 3:
            links.append('https://www.actlabor.org.au' + link)
    return links


def catch_ACT_Greens():
    links = []
    page = 0
    imcompelete_url = 'https://greens.org.au/act/news?page='
    while True:
        exist_next_page = False
        url = imcompelete_url + str(page)
        page += 1
        next_page = 'page=' + str(page)
        for link in get_links(url):
            if next_page in link:
                exist_next_page = True
            if '/act/news/' in link:
                links.append('https://greens.org.au' + link)
        if not exist_next_page:
            return links
        if page == 4:
            return links


def catch_Events_ACT():
    url = 'http://www.events.act.gov.au/whats-on-in-canberra'
    x_path = '//*[@id="find-limit"]/option[6]'
    links = []
    for link in get_links_via_option(url, driver_url, x_path, 1):
        if 'whats-on-in-canberra/event/' in link:
            links.append('http://www.events.act.gov.au' + link)
    return links


def catch_ACT_Legislative_Assembly_Question_Time():
    return ['http://www.hansard.act.gov.au/hansard/qtime/default.htm']


def catch_The_Street_Theatre():
    links = []
    for link in get_links('http://www.thestreet.org.au/whats-on'):
        if '/whats/' in link:
            links.append('http://www.thestreet.org.au' + link)
    return links


def catch_The_Australian_National_University():
    urls = ['https://www.anu.edu.au/news', 'https://www.anu.edu.au/events']
    links = []
    for url in urls:
        for link in get_links(url):
            if '/events/' in link or '/news/' in link:
                if '.au' not in link:
                    link = 'https://www.anu.edu.au' + link
                if link.count('/') == 4 and link.count('-') >= 2 and link not in links:
                    links.append(link)
    return links


def catch_National_Library_of_Australia():
    incomplete_url = 'https://www.nla.gov.au/whats-on?page='
    links = []
    page = 0

    while True:
        url = incomplete_url + str(page)
        page += 1
        next_page = 'page='+ str(page)
        next_page_exists = False
        for link in get_links(url):
            if next_page in link:
                next_page_exists = True
            if '/event/' in link:
                links.append('https://www.nla.gov.au' + link)
        if not next_page_exists:
            return links


def catch_National_Portrait_Gallery():
    links = []
    urls = ['https://www.portrait.gov.au/calendar/']
    for url in urls:
        for link in get_links(url):
            if 'exhibitions/' in link:
                links.append('https://www.portrait.gov.au' + link)
    return links


def catch_Australian_War_Memorial():
    url_events = 'https://www.awm.gov.au/visit/events?page='
    events_page = 0
    url_exhibitions = 'https://www.awm.gov.au/visit/exhibitions-current'
    url_articles = 'https://www.awm.gov.au/articles'
    links = []
    while True:
        url = url_events + str(events_page)
        events_page += 1
        next_page = 'page=' + str(events_page)
        next_page_exists = False
        for link in get_links(url):
            if next_page in link:
                next_page_exists = True
            if '/events/' in link:
                if '.au' not in link:
                    link = 'https://www.awm.gov.au' + link
                if link.count('/') == 5:
                    links.append(link)
        if not next_page_exists:
            break
        if events_page == 2:
            break

    for link in get_links(url_exhibitions):
        if '/exhibitions' in link:
            if '.au' not in link:
                link = 'https://www.awm.gov.au' + link
            if link.count('/') == 5:
                links.append(link)

    for link in get_links(url_articles):
        if '/articles/blog/' in link:
            if '.au' not in link:
                link = 'https://www.awm.gov.au' + link
            if link.count('/') == 5:
                links.append(link)
    return links


def catch_Museum_of_Australian_Democracy():
    links = []
    for link in get_links('https://www.moadoph.gov.au/'):
        if ('/events/' in link and len('/events/') < len(link) ) or ('/exhibitions/' in link and len('/exhibitions/') < len(link) ) or ('/blog/' in link and len('/blog/') < len(link) ):
            if '.au' not in link:
                link = 'https://www.moadoph.gov.au' + link
            links.append(link)
    return links


# def catch_Canberra_Deep_Space_Communication_Complex():
#     #??? what to extract
#     links = []
#     for link in get_links('https://www.cdscc.nasa.gov/'):
#         links.append(link)
#     return ['https://www.cdscc.nasa.gov/']


def catch_ACT_Legislative_Assembly_ePetitions():
    links = []
    for link in get_links('https://epetitions.act.gov.au/CurrentEPetitions.aspx'):
        if 'PetId=' in link:
            links.append('https://epetitions.act.gov.au/' + link)
    return links


