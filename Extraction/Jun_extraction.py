from goose3 import Goose
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re

"""
    Right Now, Please use get_selected_links() to get the news links
"""




'''
    Because wrap info into a class will drag the speed, and better manually delete the instance 
    I comment this part
'''
# class page_analysor:
#     __link_type__ = 'https'
#     __raw_list__ = []
#     __news_list__ = []
#     __base_domain__ = ''
#     __with_baseurl_begin__ = True
#     __with_slash_end__ = False
#     __with_baseurl_list__ = []
#     __with_relativeurl_list__ = []
#     __tail__ = ''
#     __tail_leat_length_ = 0
#
#
#     def __init__(self, url: str):
#         if 'https' not in url:
#             self.__link_type__ = 'http'
#         url_sections = url.split('/')
#         for section in url_sections:
#             if '.' in section:
#                 self.__base_domain__ = section
#                 break
#
#         links = get_links(url)
#         pattern = re.compile(r'([^-]+)-([^-]+)-([^-]+)((-[^-])*)')
#         if links is not None:
#             for link in links:
#                 if len(link) > 3 and '/' in link:
#                     #this will remove some obvious useless lines
#                     #if 'http' not in link and 'https' not in link:
#                     sections = link.split('/')
#                     tail_index = -1
#                     if '#' in sections[-1]:
#                         pos = link.find('#')
#                         # if end with #comment, then delete #comment,
#                         link = link[0 : pos]
#                         tail_index -= 1
#                     while abs(tail_index) <= len(sections):
#
#                         if re.match(pattern, str(sections[tail_index])) is not None:
#                             self.__raw_list__.append(link)
#                             break
#                         else:
#                             tail_index -= 1
#
#     def detecting(self):
#         '''
#             如果都用head，那么ratio又有head的个数决定
#             如果没有head，那么ratio由相对的url的个数决定
#         :return:
#         '''
#         max_length = 0
#         total_length = 0
#         empty_count = 0
#         head_count = 0
#         http_count = 0
#         empty_threshold = 0.6
#         head_threshold = 0.6
#         if len(self.__raw_list__) > 0:
#             for i in range(len(self.__raw_list__)):
#                 if '#' in self.__raw_list__[i]:
#                     # if end with #comment, then delete #comment,
#                     end_index = self.__raw_list__[i].find('#')
#                     if (self.__raw_list__[i])[end_index -1] == '/':
#                         #if the # is close to /, then delete / from the link
#                         end_index -= 1
#                     self.__raw_list__[i] = (self.__raw_list__[i])[0 : end_index]
#                     max_length = max(max_length, length_detector(self.__raw_list__[i]))
#                     total_length += length_detector(self.__raw_list__[i])
#                 sections = self.__raw_list__[i].split('/')
#                 #https://reneweconomy.com.au/mining-giant-looks-to-wind-and-solar-to-power-huge-nickel-project-83753/#disqus_thread
#
#                 if sections[-1] == '':
#                     empty_count += 1
#
#                 if self.__base_domain__ in self.__raw_list__[i]:
#
#                     # count how many links has the base_url
#                     head_count += 1
#                     self.__with_baseurl_list__.append(self.__raw_list__[i])
#                 if 'http' in self.__raw_list__[i]:
#                     # if not has base_url but has other http:// url, it could be other links which are useless
#                     http_count += 1
#                 else:
#                     self.__with_relativeurl_list__.append(self.__raw_list__[i])
#             if head_count / len(self.__raw_list__) > head_threshold:
#                 self.__with_baseurl_begin__ = True
#                 possible_news_count = head_count
#             else:
#                 self.__with_baseurl_begin__ = False
#                 possible_news_count = len(self.__raw_list__) - http_count
#             self.__with_slash_end__ = True if empty_count / possible_news_count > empty_threshold else False
#             print('av length:', total_length/ len(self.__raw_list__))
#             print('max length:', max_length)
#
#
#
#     def gen_newsList(self):
#         self.detecting()
#         if self.__with_baseurl_begin__:
#             return self.__with_baseurl_list__
#         else:
#             for i in range(len(self.__with_relativeurl_list__)):
#                 self.__with_relativeurl_list__[i] = self.__link_type__ + '://' + self.__base_domain__ + self.__with_relativeurl_list__[i]
#             return self.__with_relativeurl_list__


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


def write2files():
    '''
        Write the results to files, it's created for checking the result
    :return:
    '''
    note_file_url = 'Note.txt'
    if not os.path.isfile(note_file_url):
        note_file = open(note_file_url, 'x')
    else:
        note_file = open(note_file_url, 'w+')


    source_url = 'Canberra_Without_RSS'
    source_file = open(source_url)
    sources = source_file.readlines()
    source_file.close()
    base = 'Canberra_News'
    try:
        os.mkdir(base)
    except:
        pass
    id = 1
    for line in sources:
        sections = line.split('\t')
        name, url = sections[0], sections[1]
        if id < 10:
            id_str = '00' + str(id)
        elif id < 100:
            id_str = '0' + str(id)
        else:
            id_str = str(id)
        data_url = base + os.sep + id_str + name + '.txt'

        note_file.write(id_str + '*' + name + '*' + url + '*' + '*' + '\n')
        id += 1


        links = get_selected_links(url)
        if links is not None:
            if not os.path.isfile(data_url):
                data_file = open(data_url, 'x')
            else:
                data_file = open(data_url, 'w')
            for link in links:
                data_file.write(link + '\n')
        else:
            print(url, ' cannot get links')
        data_file.close()
    note_file.close()


def length_detector(line : str) -> int:
    """
        for any line in the url lists
        return the length
        for instance:
        1. http://www20.sbs.com.au/transmissions/, should return 1, after deleting www20.sbs.com.au, the length of rest part is one
        2. /story/6351760/socials-collapse-at-the-courtyard-studio/?cs=14262 return 4
        3. other invalid lines, return -1
    :param line: a line extracted from the web page
    :return: integer
    """
    if '/' not in line:
        return -1
    if re.match(r'https://(.+)', line):
        line = re.sub(r'https://([^/]+)', "/", line)
    sections = set(line.split('/'))
    if '' in sections:
        sections.remove('')
    return len(sections)



if __name__ == '__main__':
    # sources_file = open('Canberra_Without_RSS')
    # sources = sources_file.readlines()
    # sources_file.close()
    #
    # for line in sources:
    #     sections = line.split('\t')
    #     name, url = sections[0], sections[1]
    #     print('name: ', name, '  url: ', url)

    # url = 'https://www.abc.net.au/news/'
    # links = get_selected_links(url)
    # for link in links:
    #     print(link)
    write2files()
