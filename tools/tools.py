#!/usr/bin/env python
import configparser
from bs4 import BeautifulSoup

# Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally
import datetime  # needed to create unique image file name
import time  # needed to create unique image file name
import mimetypes  # needed for download functionality
from googlesearch import search

urls_buffer = []  # program main url buffer
images_tags = []  # program main found url/link buffer

urls_links = []  # buffer
urls_visited = []  # visited_links
urls_extracted = []  # urls_session

image_urls = []

# keywords container for query and page content
content_keywords = []
query_keywords = []

# stop words and urls for blocking urls
stop_words = []
stop_urls = []

configuration = configparser.ConfigParser()
configuration.read('config.env')

RELAX_TIME = float(configuration.get('CONFIG', 'RELAX_TIME'))
CONTENT_QUALITY_SCORE = float(
    configuration.get('CONFIG', 'CONTENT_QUALITY_SCORE'))
MIN_LINK_LENGTH = int(configuration.get('CONFIG', 'MIN_LINK_LENGTH'))
MIN_KEYWORD_LENGTH = int(configuration.get('CONFIG', 'MIN_KEYWORD_LENGTH'))
MIN_KEYWORDS_IN_LINK = int(configuration.get('CONFIG', 'MIN_KEYWORDS_IN_LINK'))
DIFFICULTY_RATIO = int(configuration.get('CONFIG', 'DIFFICULTY_RATIO'))


def extract_frequency(text):

    list_words = []
    list_words_1 = []
    list_words_2 = []
    list_words_3 = []
    list_words_4 = []
    list_words_5 = []

    for i in text.splite(" "):
        if not i in list_words:
            list_words_1.append(i)
        else:
            if not i in list_words_2:
                list_words_2.append(i)
            else:
                if not i in list_words_3:
                    list_words_3.append(i)
                else:
                    if not i in list_words_4:
                        list_words_4.append(i)
                    else:
                        if not i in list_words_5:
                            list_words_5.append(i)

    print(" 1 - " + list_words_1)
    print(" 2 - " + list_words_2)
    print(" 3 - " + list_words_3)
    print(" 4 - " + list_words_4)
    print(" 5 - " + list_words_5)

def check_pattern(pattern, html):
    import re
    vidlinks = re.findall(pattern, html) #find all between the two parts in the data
    #print(vidlinks[0] + ".m3u8") #print the full link with extension

    if (len(vidlinks)>0):
        with open("patterns", "a") as file:
            for rc in vidlinks:
                x_print("VOD FOUND")
                x_print("data: " + rc)
                file.write("M3U-VOD : " + str(rc) + "\n")
                file.close()

def check_m3u8(html):
    check_pattern("src='(.*?).m3u8'/>", html)
  
def load_list_search_api(val):
    # PSEUDO CODE
    # Connect to search apiload_list_from_search_api
    # Bring back urls from search api
    print("Connecting to search api")

    # loop thru search api 5
    max_loop = [1, 2, 3, 4, 5]
    print("Building keywords list object")

    for loop in max_loop:
        response = connect_search_api(val, loop)
        relax(RELAX_TIME)

        # save found url to urls.txt file
        f = open("urls.txt", "a")

        for search_results in response["value"]:
            search_url = search_results["url"]
            # print("\n\n_____________________________________________________")
            #print("\nkeywords to memory content verification list")
            #print("\nAdding: " + search_results["title"])

            content_keywords.append(search_results["title"])

            #print("\nurl to the url buffer list")
            #print("\nurl: " + search_url)
            f.write(search_url + "\n")
            relax(RELAX_TIME)
        f.close()


# keywords container for query and page content
content_keywords = []
query_keywords = []


def clean_stop_list(word):
    # preformating word
    if word in stop_words:
        return ""
    return word

def clean_word_final(word):
    index = 0
    for char in word:
        # ^ is the references char
        if char in "()(){},.-:;|*/+\"\\~^–":
            word = word.replace(char, " ")
        index = index + 1

    word = trim(word)
    return word

def verify_link(link):
    global query_keywords
    global i_score

def relax(sec):
    time.sleep(sec)

def build_keywords_lists(val):

    # Quality score used to decide if the url matches keywords of query
    global CONTENT_QUALITY_SCORE
    global content_keywords
    global query_keywords

    print("Building query keywords list object ")
    relax(RELAX_TIME)

    for keywords in val.split():
        keywords = keywords.lower()
        keywords = trim(keywords)
        keywords = str(keywords)
        keywords = clean_word_final(keywords)
        keywords = clean_stop_list(keywords)

        if not keywords in query_keywords:
            if (len(keywords) > MIN_KEYWORD_LENGTH):
                query_keywords.append(keywords)
                content_keywords.append(keywords)
                # ADDING WORD WITHOUT S AT THE END
                if (keywords[len(keywords)-1] == "s"):
                    query_keywords.append(keywords[0:len(keywords)-1])
                    content_keywords.append(keywords[0:len(keywords)-1])
                # ADDING WORD ROOT FOR BETTER MATCHING
                if (len(keywords) >= 6):
                    query_keywords.append(keywords[0:3])
                    content_keywords.append(keywords[0:3])
                # add root of the word
                if (len(keywords) >= 12):
                    query_keywords.append(keywords[0:6])

    # adding images keywords for searching site with image content
    query_keywords.append("photo")
    query_keywords.append("photograph")
    query_keywords.append("image")
    query_keywords.append("pictures")
    query_keywords.append("gallery")
    query_keywords.append("wallpaper")

    # adding images keywords for searching site with image content
    content_keywords.append("photo")
    content_keywords.append("photograph")
    content_keywords.append("image")
    content_keywords.append("picture")
    content_keywords.append("gallery")
    content_keywords.append("wallpaper")

    print("Calculation query quality limit score")
    CONTENT_QUALITY_SCORE = CONTENT_QUALITY_SCORE * \
        (len(query_keywords)/DIFFICULTY_RATIO)
    print("CONTENT_QUALITY_SCORE is " + str(CONTENT_QUALITY_SCORE) + "\n")

def connect_search_api(query, page_number):

    URL = "https://rapidapi.p.rapidapi.com/api/Search/WebSearchAPI"
    HEADERS = {
        'x-rapidapi-key': "e2c4e6deabmsh054a7dd9082d6f9p1dddc2jsn9fa43d149a24",
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }

    query = query
    page_number = page_number
    page_size = 100
    auto_correct = True
    safe_search = False

    # val = input("Is this the query: " + query)

    querystring = {"q": query,
                   "pageNumber": page_number,
                   "pageSize": page_size,
                   "autoCorrect": auto_correct,
                   "safeSearch": safe_search}

    response = requests.get(URL, headers=HEADERS, params=querystring).json()

    total_count = response["totalCount"]

    for web_page in response["value"]:

        url = web_page["url"]
        title = web_page["title"]
        description = web_page["description"]
        body = web_page["body"]
        date_published = web_page["datePublished"]
        language = web_page["language"]
        is_safe = web_page["isSafe"]
        provider = web_page["provider"]["name"]

        #print("title: {}".format(title))
        #print("Url: {}...".format(url))

    return response


def trim(text_section):

    relax(RELAX_TIME)

    text_section = text_section.strip()
    text_section = text_section.lstrip()
    return text_section

dic = []


def load_stop_urls():

    relax(RELAX_TIME)

    global stop_urls
    x_print("LOADING STOPLIST")

    with open("stop_urls.txt", "r") as file:
        # reading each line"
        for line in file:
            line = line.replace("\n", "")
            line = trim(line)
            stop_urls.append(line)

def x_print(data):
    # Special printt
    # consol, log file and interface
    print(data)
    debug_info(data)

def debug_info(info):
    # print to screen
    from datetime import datetime
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = open("debug.txt", "a")
    f.write("\n" + str(time) + " : ")
    f.write(str(info))
    f.close()

knowldge = []

def knowledge():
    relax(RELAX_TIME)
    global knowledge
    
    x_print("LOADING - Query History")

    with open("learned_knowledge.txt", "r") as file:
        # reading each line"
        for line in file:
            line = line.replace("\n", "")
            line = trim(line)
            knowledge.append(line)
        file.close()
    return knowledge

query_history = []

def load_profile():
    relax(RELAX_TIME)
    global query_history
    
    x_print("LOADING - Query History")

    with open("stop_urls.txt", "r") as file:
        # reading each line"
        for line in file:
            line = line.replace("\n", "")
            line = trim(line)
            query_history.append(line)
        file.close()
    return query_history

def system_profile():
    query_history = load_profile()
    return query_history

def trim(text_section):
    relax(RELAX_TIME)
    text_section = text_section.strip()
    text_section = text_section.lstrip()
    return text_section
    
def add_to_dic(i):
    global dic
    if i not in dic:
        dic.append(i)

def load_dic():
    global dic
    with open("dic", "r") as file:
        # reading each line"
        for word in file:
            word = clean_word_final(word)
            stop_words.append(word.strip())

def save_dic():
    global dic
    with open("dic", "w") as file:
        for word in dic:
            # reading each line"
            word = clean_word_final(word)
            file.write(word)
        file.close()