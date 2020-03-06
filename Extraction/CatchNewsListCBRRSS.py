

from goose3 import Goose
# import utility
from utility import goose_by_url
from bs4 import BeautifulSoup
import re
import feedparser
import time

# The first three digit of the keys of {rss_url} dictionary should always be capital letters
# If the length less than 3 digit, then use "_" to make the length=3(for ANU sources)
# Because the first three digit represents the short name of the media on website.
rss_url = {"A_Stylish_Moment": "http://astylishmoment.com/feed/",
           "ABC_News_Canberra": "https://www.abc.net.au/news/feed/8057234/rss.xml",
           "ACT_Civil_and_Administrative_Tribunal": "https://www.acat.act.gov.au/general/rss-feeds/judgments-rss",
           "ACT_Apple_Users_Group": "https://actapple.org.au/blog/?feed=rss2",
           "ACT_Deafness_Resource_Centre": "https://www.actdrc.org.au/feed/",
           "ACT_Emergency_Service_Agency": "http://esa.act.gov.au/feed",
           "Chief_Minister_Treasury_and_Economic_Development_Directorate": "https://www.cmtedd.act.gov.au/open_government/functions/functionality/media_release_rss_feeds/latest_directorate_media_releases_rss",
           "ACT_Legislative_Assembly_Calendar": "https://www.parliament.act.gov.au/functions/rss/calendar",
           "ACT_Legislative_Assembly_Daily_Program": "https://www.parliament.act.gov.au/functionality/rss/daily-program",
           "ACT_Legislative_Assembly_Matters_Of_Public_Importance": "https://www.parliament.act.gov.au/functionality/rss/matters_of_public_importance",
           "ACT_Legislative_Assembly_Minutes_Of_Proceedings": "https://www.parliament.act.gov.au/functionality/rss/minutes-of-proceedings",
           "ACT_Legislative_Assembly_Notice_Papers": "https://www.parliament.act.gov.au/functionality/rss/notice-papers",
           "ACT_Magistrates_Court_Judgements": "https://www.courts.act.gov.au/magistrates/rss/judgments-rss",
           "ACT_Magistrates_Court_Publications": "https://www.courts.act.gov.au/magistrates/rss/publications-rss",
           "ACT_Minister_Media_Release": "https://www.cmtedd.act.gov.au/open_government/functions/functionality/media_release_rss_feeds/latest_minister_media_releases_rss",
           "ACT_Police_Blog": "https://policenews.act.gov.au/feed/blog",
           "ACT_Police_Community_News": "https://policenews.act.gov.au/feed/community-news",
           "ACT_Police_Media_Releases": "https://policenews.act.gov.au/feed/media-releases",
           "ACT_Shelter": "http://www.actshelter.net.au/?format=feed&type=rss",
           "ACT_Supreme_Court_Judgments": "https://www.courts.act.gov.au/supreme/rss/judgments-rss",
           "ACT_Supreme_Court_Publications": "https://www.courts.act.gov.au/supreme/rss/publications-rss",
           "ANU_CHELT": "http://chelt.anu.edu.au/rss.xml",
           "ANU_CAEPR": "http://caepr.cass.anu.edu.au/rss.xml",
           "ANU_CASS": "https://cass.anu.edu.au/rss.xml",
           "ANU_CAP": "http://asiapacific.anu.edu.au/rss.xml",
           "ANU_CECS": "https://cecs.anu.edu.au/rss.xml",
           "ANU_CSSA": "http://cs.club.anu.edu.au/?q=rss.xml",
           "ANU_ECI": "https://energy.anu.edu.au/rss.xml",
           "ANU_LSS": "http://www.anulss.com/feed/",
           "ANU_MSI": "https://maths.anu.edu.au/rss.xml",
           "ANU_MS": "https://medicalschool.anu.edu.au/rss.xml",
           "ANU_MSS": "https://anumss.org/feed/",
           "ANU_O": "https://anuobserver.org/feed/",
           "ANU_P": "https://press.anu.edu.au/rss.xml",
           "ANU_RSES": "http://rses.anu.edu.au/rss.xml",
           "ANU_SAA": "http://archanth.cass.anu.edu.au/rss.xml",
           "ANU_SAD": "https://soad.cass.anu.edu.au/rss.xml",
           "ANU_SM": "https://music.cass.anu.edu.au/rss.xml",
           "ANU_SA": "https://anusa.com.au/news/rss/6013/",
           "ANU_U": "http://www.anuunion.com.au/feed/",
           "Ainslie_and_Gorman_Arts_Centres": "http://www.agac.com.au/feed/",
           "Band_of_Brothers": "https://www.bandofbros.com.au/feed/",
           "Beaver_Galleries": "https://www.beavergalleries.com.au/feed/",
           "CBR_Canberra": "https://canberra.com.au/feed/",
           "CIT_Student_Association": "http://www.citsa.com.au/feed/",
           "Canberra_Choral_Society": "https://canberrachoralsociety.org/feed/",
           "Canberra_Critics_Circle": "http://ccc-canberracriticscircle.blogspot.com/feeds/posts/default?alt=rss",
           "Canberra_Film_Blog": "https://canberrafilmblog.com/feed/",
           "Canberra_Foodies_Adventures": "https://foodpornjournal.com/feed/",
           "Canberra_Gay_and_Lesbian_Qwire": "https://www.canberraqwire.org.au/dbaction.php?action=rss&dbase=uploads",
           "CIN": "https://cbrin.com.au/feed/",
           "CIT": "https://cit.edu.au/cit_rss_feed",
           "Canberra_Jazz_Blogspot": "http://canberrajazz.blogspot.com/feeds/posts/default",
           "Canberra_Liberals": "https://canberraliberals.org.au/feed/",
           "Canberra_Philharmonic_Society": "http://philo.org.au/feed/",
           "Canberra_Quilters_Inc": "canberraquilters.org.au/feed",
           "Canberra_Symphony_Orchestra": "https://cso.org.au/feed/",
           "Canberra_Theatre_Centre": "https://canberratheatrecentre.com.au/feed/",
           "Capital_Football": "https://capitalfootball.com.au/feed/",
           "City_News": "https://citynews.com.au/feed/",
           "Cross_Fit_Canberra": "https://www.crossfitcanberra.net/feed.xml",
           "Eat_Canberra": "http://eatcanberra.com.au/feed/",
           "Eelighten_Festival": "https://enlightencanberra.com/feed/",
           "Floriade": "https://floriadeaustralia.com/feed/",
           "Griffin_Accelerator": "https://griffinaccelerator.com.au/feed/",
           "Her_Canberra": "https://hercanberra.com.au/feed/",
           "Kanga_Cup": "https://kangacup.com/feed/",
           "Life_In_Canberra": "https://lifeincanberra.com.au/feed/",
           "National_Museum_Australia": "https://www.nma.gov.au/audio/itunes-rss",
           "National_Zoo": "https://nationalzoo.com.au/feed/",
           "Outin_Canberra": "https://www.outincanberra.com.au/feed/",
           "SO_Frank": "http://www.sofrank.com.au/feed/",
           "Spilt_Milk": "https://spilt-milk.com.au/feed/",
           "Tennis_Canberra": "http://www.tenniscanberra.com.au/feed/",
           "The_Basement_Canberra": "https://www.thebasementcanberra.com.au/feed/",
           "Healing_Foundation": "https://healingfoundation.org.au/feed/",
           "The_Queanbeyan_Performing_Arts_Centre": "https://theq.net.au/home/feed/",
           "The_Queanbeyan_Age": "https://www.queanbeyanagechronicle.com.au/rss.xml",
           "Riot_ACT": "https://the-riotact.com/feed/",
           "The_Style_Side": "https://www.thestyleside.net/feed.xml",
           "Tourism_ACT": "https://tourism.act.gov.au/feed",
           "Traveland_Beyond": "https://travelandbeyond.org/feed",
           "Uni_House": "http://unihouse.anu.edu.au/feed/",
           "UC": "http://www.canberra.edu.au/config/monitor-landing-page-assets/rss-feeds",
           "Who_Shoots": "https://www.whoshoots.com/feed",
           "Woodland_and_Wetlands": "https://woodlandsandwetlands.org.au/feed/",
           "Woroni": "https://www.woroni.com.au/feed/",
           "Young_Music_Society": "http://youngmusicsociety.org.au/feed/"
           }

g_root = Goose()


def get_news_list_rss(rss_url):
    news_list = {}
    time_list = {}
    for rss in rss_url:
        one_page_dict = feedparser.parse(rss_url[rss])
        temp = []
        for i in range(len(one_page_dict["entries"])):
            link = (one_page_dict["entries"][i]["link"])
            temp.append(link)
            # print(one_page_dict["entries"][i]['published_parsed'])
            one_time = one_page_dict["entries"][i]['published_parsed']
            time_list[link] = one_time
            # timestamp = time.mktime(one_time)

        news_list[rss] = temp
    return news_list, time_list


# print(get_news_list_rss(rss_url))

g = Goose()


# the find author methods are not used now
def find_author_abc(url):
    match_name = []
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    divs = soup.find_all('div')
    for div in divs:

        if div.get('class') == None:
            continue
        if 'byline' == div.get('class')[0]:
            if div.parent.name == 'figcaption':
                continue

            match_name = re.findall(r'title="">([^></]*)</a>', str(div))
            if match_name == []:
                match_name = re.findall(r'<div class="byline">([^></]*)</div>', str(div))
            if match_name == []:
                for content in div.contents:
                    findAu = re.findall(r'By([^></]*)', str(content))
                    if findAu != []:
                        match_name = match_name + findAu
            if '</a> for <a' in str(div):
                match_name.pop()
            spans = div.find_all('span')
            if not spans == None:
                for span in spans:
                    match_name.append(span.get_text())
        if match_name != []:
            for name in match_name:
                nameindex = match_name.index(name)

                name = name.replace('(', '').replace(')', '')
                name = name.strip()
                if ':' in name:
                    match_name = name.split(':')[1].split(',')
                    break
                if re.findall(r'[A-Za-z]+', name) == []:
                    match_name[nameindex] = ''
                    continue
                if 'By' in name:
                    name = re.findall(r'By([^></]*)', name)[0]
                match_name[nameindex] = name
            if '' in match_name:
                match_name.remove('')

            return (match_name)
            break


def find_author_sbs(url):
    match_name = []
    page = g.extract(url=url)
    soup = BeautifulSoup(page.raw_html, 'lxml')
    scripts = soup.find_all('script')
    for script in scripts:
        if script.get('data-module') != None and 'data-layer_module' in script.get('data-module'):
            # print(script.get_text)
            # print(type(script.get_text))
            authorsraw = re.findall(r'"author":([^123]*)"subject"', str(script.get_text))[0].replace('[', '').replace(
                ']', '').split(',')
            for author in authorsraw:
                author = author.strip().replace('"', '').replace('"', '')
                if author != '':
                    match_name.append(author)
            print(match_name)
