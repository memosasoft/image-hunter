# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import configparser
import mimetypes  # needed for download functionality
import os
import shutil  # to save it locally
import time
# Importing Necessary Modules
import urllib.request
import uuid
from distutils.command.config import dump_file
from platform import python_branch
from random import random
from re import I
from sqlite3 import Error

import nltk
import requests  # to get image from the web
from bs4 import BeautifulSoup
from googlesearch import search
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nturl2path import url2pathname
from selenium import webdriver as driver

# Session url and img global_memory
urls_global_session_memory = []
images_session_memory = []

current_root_url = ""
current_url = ""
current_title = ""
current_html = ""
current_text = ""
current_preview = ""
current_img_keywords = ""
current_http_src = ""
current_img_src = ""
current_query = ""
current_patterns_hits = ""
current_freq = []
current_img_size = 0
current_description = ""
current_image_alt_text_test = ""
current_long_keywords = ""
current_query_preview = ""
current_frequency_score = 0
current_nb_words_in_text = 0
current_logo = "http://thewowstyle.com/wp-content/uploads/2014/10/2620.jpg"

proxies = {
    'http': '192.168.0.58:8080',
    'https': '192.168.0.58:443',
}

media_files = "psd,apng,avif,bmp,gif,ico,cur,tif,tiff,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp,webm,ogg,tiff,ico,jpg,gif,png,bmp"

html_file_name = str(uuid.uuid4())
html_img_counter = 0

img_count = 0
url_count = 0
save_count = 0
spidered_site_count = 0
approch_counter = 0

query_size = 0
current_quality_score = 0
spam_score = 0
bonus_score = 0

# Program url buffers
urls_buffer = []  # long-term buffer =
urls_visited = []  # visited_links
urls_images = []

urls_problems = []
proxies_list = []
proxy_good = False

# search urls from google
search_urls = []

# SORRY STILL WORKING
# IN DEVELOPPEMENT
# Ideas to cheat intelligence
# adding specific keywords under the hood
# to get better searching and matching
search_boost_data = "photo image picture gallery wallpaper art digital svg jpg jpeg"
match_boost_data = "account capture image art blowup canvas capture film cartoon close-up design doodle drawing duplicate icon illustrate impression lens lookalike microfilm mug negative painting panorama photoengrave photograph pic picture pix portrait print replica image picture gallery pic art digital svg jpg jpeg web ogg gif png bmp camera capture carousel close-up digital camera zoom enlarge enlarger exposure filter fisheye focal image holographic holography kinetoscope low-resolution microfiche microfilm optical overexpose panorama pap paparazzi paparazzo photobomb photobombing photocall photogenic photograph photographer photographic photographically photography photojournalism photojournalist photoshoot pin-up snapshot retrovectors typeslab picsplosion debzebooks designschool.canva generatepress images.google inkscape openclipart pixabay pixnio pngtree publicdomainvectors rachelrofe unsplash visualhunt vwo wordmark cleanpng clipartmax dafont fontsquirrel instagram myfonts photopea pixsy"

search_boost = []
match_boost = []

match_boost_with_query = ""
pattern_memory = []

# keywords container for query
query_history = []

# Learning component
dictionary = []
synonyms = []
learned_relations = []

phrase_dictionary = []

spam_filter = []
code_filter = []
# Learning array for text the system reads
learned_keywords = []

from fake_useragent import UserAgent
# ua = UserAgent()
# Fake user agent

user_profil = []

# stop words and urls
stop_words = []
stop_urls = []

spidered_site_count = 0

configuration = configparser.ConfigParser()
configuration.read('config.env')

CLEAN_START = str(configuration.get('CONFIG', 'CLEAN_START'))
TIME_LOCK = float(configuration.get('CONFIG', 'TIME_LOCK'))

QUALITY_SCORE = float(configuration.get('CONFIG', 'QUALITY_SCORE'))
FREQ_SCORE = float(configuration.get('CONFIG', 'FREQ_SCORE'))

KEYWORDS_IN_LINK = str(configuration.get('CONFIG', 'KEYWORDS_IN_LINK'))
NUMBER_OF_KEYWORDS_IN_LINK = int(configuration.get(
    'CONFIG', 'NUMBER_OF_KEYWORDS_IN_LINK'))
MIN_URL_SIZE = int(configuration.get('CONFIG', 'MIN_URL_SIZE'))
MAX_URL_SIZE = int(configuration.get('CONFIG', 'MAX_URL_SIZE'))
MAX_WORD_SIZE = int(configuration.get('CONFIG', 'MAX_WORD_SIZE'))
MIN_WORD_SIZE = int(configuration.get('CONFIG', 'MIN_WORD_SIZE'))
MIN_STEM_SIZE = int(configuration.get('CONFIG', 'MIN_STEM_SIZE'))
LONG_KEYWORD_SIZE = int(configuration.get('CONFIG', 'LONG_KEYWORD_SIZE'))
MIN_PATTERN_SIZE = int(configuration.get('CONFIG', 'MIN_PATTERN_SIZE'))

FREQUENCY_MIN_WORDS = int(configuration.get('CONFIG', 'FREQUENCY_MIN_WORDS'))
NB_OF_SITE_TO_SPIDER = int(configuration.get('CONFIG', 'NB_OF_SITE_TO_SPIDER'))
IMG_ALT_VERIFICATION = str(configuration.get('CONFIG', 'IMG_ALT_VERIFICATION'))
IMG_ALT_QS = int(configuration.get('CONFIG', 'IMG_ALT_QS'))
STEP_SCAN = int(configuration.get('CONFIG', 'STEP_SCAN'))
LEARNING_TFQST = int(configuration.get('CONFIG', 'LEARNING_TFQST'))
LEARN_TO_BLOCK_URL = int(configuration.get('CONFIG', 'LEARN_TO_BLOCK_URL'))
DOWNLOAD_EVERYTHING = str(configuration.get('CONFIG', 'DOWNLOAD_EVERYTHING'))
DEEP_ANALYSIS = str(configuration.get('CONFIG', 'DEEP_ANALYSIS'))
ANALYSIS_MAX_WORDS = int(configuration.get('CONFIG', 'ANALYSIS_MAX_WORDS'))
SPIDER_ALL_IMAGES = str(configuration.get('CONFIG', 'SPIDER_ALL_IMAGES'))
SEARCH_BOOST = str(configuration.get('CONFIG', 'SEARCH_BOOST'))
MATCH_BOOST = str(configuration.get('CONFIG', 'MATCH_BOOST'))
QUERY_BOOST = str(configuration.get('CONFIG', 'QUERY_BOOST'))
PREVIEW_SIZE = int(configuration.get('CONFIG', 'PREVIEW_SIZE'))
DOWNLOAD_HTML = str(configuration.get('CONFIG', 'DOWNLOAD_HTML'))
HTML_IMAGE_PER_PAGE = int(configuration.get('CONFIG', 'HTML_IMAGE_PER_PAGE'))
SAVE_CYCLE = int(configuration.get('CONFIG', 'SAVE_CYCLE'))
MIN_IMAGE_SIZE = int(configuration.get('CONFIG', 'MIN_IMAGE_SIZE'))
MAX_FILE_NAME_SIZE = int(configuration.get('CONFIG', 'MAX_FILE_NAME_SIZE'))
DEBUG_CONSOLE = str(configuration.get('CONFIG', 'DEBUG_CONSOLE'))
DEBUG_LOG = str(configuration.get('CONFIG', 'DEBUG_LOG'))
MAX_WORKSPACE_SIZE = int(configuration.get('CONFIG', 'MAX_WORKSPACE_SIZE'))
MIN_QUALITY_IMAGE_SIZE = int(configuration.get(
    'CONFIG', 'MIN_QUALITY_IMAGE_SIZE'))
URL_LIMIT_CLEANING = int(configuration.get('CONFIG', 'URL_LIMIT_CLEANING'))
SAVE_SUBJECT_KEYWORDS = str(configuration.get(
    'CONFIG', 'SAVE_SUBJECT_KEYWORDS'))

RANDOM_START = int(configuration.get('CONFIG', 'RANDOM_START'))
DIG_FOR_URLS = str(configuration.get('CONFIG', 'DIG_FOR_URLS'))
FREELY_GRAB_URLS = str(configuration.get('CONFIG', 'FREELY_GRAB_URLS'))
PROXY_ACTIVATED = 'OFF'

PROGRAM_PATH = str(configuration.get('CONFIG', 'PROGRAM_PATH'))


def init_program(query):

    global query_size
    global query_history
    global current_query

    # Query global_memory self-learning object
    load_memory()

    # User system-interaction
    x_print("WELCOME TO Image-Miner")
    x_print("Powered by Python")
    #x_print("In memory of META-CRAWLER 1990")
    x_print("Image-Miner is connected to Google, Yahoo and Bing")
    x_print("Thank you for using Image-Miner")

    user_input = 'n'

    # clean urls lists
    if (CLEAN_START == 'ON'):
        #user_input = input("\nClean start? (y/n)")
        user_input = 'y'

    save_media()
    # User system-interaction
    x_print("SETUP PROCESS")
    x_print("Starting setup process and cleanup")
    setup_process(user_input)

    if (query == ""):
        query = input("What type of images you want to spider?")

    query_size = str(len(query.split(" ")))

    # THIS IS A PERSONAL CHOICE AND A TRICK TO GET
    # MORE IMAGES IN THE SEARCH ITS NOT COMPLICATED
    current_query = query
    query = process_boost(query)
    
    #Create HTML interface files 
    first_dump(current_query)

    query_history = load_list("./intelligence/query_history", query_history)
    query_history.insert(0, query)
    query_history = save_list(query_history, "./intelligence/query_history")

    x_print("\nSEARCH MODULE\n")
    x_print("Connecting to Google, Yahoo and Bing")
    x_print("This may take a while")

    # MULTIPLE QUERIES & QUERY BOOST
    if QUERY_BOOST == "ON":
        search_urls = multiple_search_prototype(query)
    else:
        search_urls = get_search_urls(query)

    search_urls = insert_in_buffer(search_urls)

def save_media():

    global query_history
    global current_query

    try:

        query_foler = current_query.replace(" ", "-")

        if len(query_foler) < MIN_WORD_SIZE:
            return None

        MAX_FOLDER_LENGHT = 200

        if len(query_foler) > MAX_FOLDER_LENGHT:
            query_foler = query_foler[0:MAX_WORD_SIZE*3]

        # Directory
        directory = query_foler

        # Parent Directory path
        parent_dir = "./archives/media/"

        # Path
        path = os.path.join(parent_dir, directory)

        # Create the directory
        # 'GeeksForGeeks' in
        isFile = os.path.isdir(path)
        print(isFile)

        if isFile == False:
            os.mkdir(path)

    except Exception as e:
        print(e)
        print("Exception saving archive")
        pass

    try:
        save_to_archive("./media/", "./archives/media/" +
                        str(query_foler) + "/")
        save_to_archive("./interface/", "./archives/interface/")
    except Exception as e:
        print(e)
        print("Exception saving archive")
        pass

    print("SAVING IMAGES")
    x_print("Images and media saved\n")


def extract_info_from_url(url):
    x_print("\nSTARTING URL EXTRACTION PROCESS\n")
    info = ""
    url_clean = url.replace(".", " ")
    url_clean = url_clean.replace("_", " ")
    url_clean = url_clean.replace(",", "_")
    url_clean = clean_url_html_tags(url_clean)
    url_clean = clean_url(url_clean)

    for i in url_clean.split("/"):
        if len(i) == 0:
            continue

        i = clean_word(i)
        i = clean_numbers(i)
        i = check_stop_words(i)

        info = info + " " + i

    info = clean_text(info)
    info = str(trim(info))

    x_print("Concepts found in url ")
    x_print(info)

    return info


def process_boost(query):

    global current_query
    global match_boost
    global search_boost
    global match_boost_data
    global search_boost_data

    if SEARCH_BOOST == "ON":
        query = query + " " + clean_text(search_boost_data)
        search_boost.append(query)
        search_boost = save_list(search_boost, "./intelligence/search_boost")
        print("Just added search boost")

    if MATCH_BOOST == "ON":
        # CRITICAL ELEMENT FOR MATCHING
        global match_boost_with_query
        match_boost_data = clean_text(match_boost_data)
        match_boost_with_query = query + " " + match_boost_data
        match_boost.append(match_boost_with_query)
        match_boost = save_list(match_boost, "./intelligence/match_boost")
        print("Just added match boost")

    print("Cleaning query")
    query = clean_text(query)

    return query


def clean_query(query):

    items = ["  ", ",", ".",
             "-", "+", "{", "}", "[", "]", "(", ")"]

    for item in items:
        while query.find(item) >= 0:
            query = query.replace(item, " ")

    clean_query = ""
    for word in query.split(" "):
        word = clean_word(word)
        clean_query = clean_query + " " + word

    return clean_query

# EXPERIMENTAL MULTIPLE SEARCH_BOOST
# ADDING IMAGE RELATED GENERAL KEYWORDS
# TO GET MORE SEARCH RESULTS


def multiple_search_prototype(query):

    # UNDER 
    # STILL NOT READY
    # CURRENTLY TESTING AND DEBUGING

    # The code is not optimize yet

    # It dirty code so please dont
    # be to hard on me...

    # Normalize the query string
    original_q = query.lower()
    prototype_rq = query.lower()
    query = query.lower()

    # Prepare query with extra image termes
    query = clean_query(query)

    x_print("\nQUERY_BOOST ACTIVATED\n")
    x_print("\nSending multiple queries")
    x_print("with additional general image keywors\n")

    x_print("THIS IS A LONG PROCESS")
    x_print("PLEASE BE PATIENT\n")

    # PROTOTYPE EXTRA Random QUERY 1 and 2
    prototype_rq1 = " digital picture "
    prototype_t = str(prototype_rq1).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    memory = []
    for i in prototype_t:
        if (not i in memory):
            prototype_x = prototype_x + " " + i
            memory.append(i)

    prototype_rq1 = prototype_x + " " + query
    query_history.append(prototype_rq1)

    prototype_rq2 = " image "
    prototype_t = str(prototype_rq2).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    memory = []
    for i in prototype_t:
        if (not i in memory):
            prototype_x = prototype_x + " " + i
            memory.append(i)

    prototype_rq2 = query + " " + prototype_x
    query_history.append(prototype_rq2)

    prototype_rq3 = " picture "
    prototype_t = str(prototype_rq3).split(' ')

    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    memory = []
    for i in prototype_t:
        if (not i in memory):
            prototype_x = prototype_x + " " + i
            memory.append(i)

    prototype_rq3 = prototype_x + " " + query
    query_history.append(prototype_rq3)
    prototype_rq4 = " photo "

    prototype_t = str(prototype_rq4).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    memory = []
    for i in prototype_t:
        if (not i in memory):
            prototype_x = prototype_x + " " + i
            memory.append(i)

    prototype_rq4 = query + " " + prototype_x
    query_history.append(prototype_rq4)
    # Add extra image related search terms to enhance
    # the search results the list is in config.env

    query = prepare_query(query)

    search_urls = get_search_urls(trim_url(query))
    print("QUERY: " + str(query))

    query = prepare_query(prototype_rq1)
    search_urls = get_search_urls(trim(prototype_rq1))
    print("QUERY 2: " + str(prototype_rq1))

    query = prepare_query(prototype_rq2)
    search_urls = get_search_urls(trim(prototype_rq2))
    print("QUERY 3: " + str(prototype_rq2))

    query = prepare_query(prototype_rq3)
    search_urls = get_search_urls(trim(prototype_rq3))
    print("QUERY 4: " + str(prototype_rq3))

    query = prepare_query(prototype_rq4)
    search_urls = get_search_urls(trim(prototype_rq4))
    print("QUERY 5: " + str(prototype_rq4))

    # need to be properly programmed
    original_q = original_q + " wallpaper"
    query = prepare_query(original_q)

    search_urls = get_search_urls(trim(original_q))
    print("LAST QUERY: " + str(original_q))
    relax(TIME_LOCK*5)

    memory = []

    #list_rq1 = check_search_urls(list_rq1)
    #list_rq2 = check_search_urls(list_rq2)
    #list_rq3 = check_search_urls(list_rq3)
    #list_rq4 = check_search_urls(list_rq4)
    #list_original = check_search_urls(list_original)
    search_urls = check_search_urls(search_urls)

    # for i in list_rq1:
    #    i = urllib.parse.unquote(i)
    #    insert_search_urls(i, prototype_rq1)
    #    print("inserting in DB: " + str(i))

    # for i in list_rq2:
    #    i = urllib.parse.unquote(i)
    #    insert_search_urls(i, prototype_rq2)
    #    print("inserting in DB: " + str(i))

    # for i in list_rq3:
    #    i = urllib.parse.unquote(i)
    #    insert_search_urls(i, prototype_rq3)
    #    print("inserting in DB: " + str(i))

    # for i in list_rq4:
    #    i = urllib.parse.unquote(i)
    #    insert_search_urls(i, prototype_rq4)
    #    print("inserting in DB: " + str(i))

    for i in search_urls:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, original_q)
        print("inserting in DB: " + str(i))

    #print("Adding to search buffer")
    #earch_urls = add_list_to_list(search_urls, list_rq1)
    #search_urls = add_list_to_list(search_urls, list_rq2)
    #search_urls = add_list_to_list(search_urls, list_rq3)
    #search_urls = add_list_to_list(search_urls, list_rq4)
    #search_urls = add_list_to_list(search_urls, list_original)
    #print("Urls added to search buffer")

    # System interaction with user
    x_print("We got: " + str(len(search_urls)) + " urls to mine\n")
    x_print("Thank you Google, Yahoo and Bing...")
    # Inserting urls at the beginning of the url list
    x_print("\nAdding the search urls to the begining of search buffer...")

    #import random
    # random.shuffle(search_urls)
    # random.shuffle(search_urls)
    return search_urls


def prepare_query(query):
    query = query.replace(" ", "+")
    return query


def check_critical_amount_of_urls(list_of_urls):

    for url in list_of_urls:
        result = verify_keywords_in_link(url)
        if result == False:
            list_of_urls.remove(url)
            print("removing url: " + str(url))

    return list_of_urls


def check_search_urls(list_of_urls):

    for url in list_of_urls:
        result = first_check(url)

        if result == False:
            list_of_urls.remove(url)
            print("removing url: " + str(url))

    return list_of_urls


def add_list_to_list(list_to_grow, list_to_add):
    result_counter = 0
    for i in list_to_add:
        if not i in list_to_grow:
            list_to_grow.append(i)
            print(str(result_counter) + " : " + i)
            result_counter = result_counter + 1
    return list_to_grow


def insert_in_buffer(urls):
    # Main url buffer
    global urls_buffer

    for i in urls:
        if (len(i) < MIN_URL_SIZE):
            continue
        if (len(i) > MAX_URL_SIZE):
            continue
        if not i.find("http") >= 0:
            continue

        if not i in urls_buffer:
            urls_buffer.insert(0, str(i))

    urls_buffer = save_list(urls_buffer, "./intelligence/data/urls")
    return urls_buffer
    # save_memory()

# Self learning object to gain ai from
# user interaction - Prototype


def save_memory():
    global urls_buffer
    global urls_visited
    global urls_images

    global stop_urls
    global dictionary

    # shuffle_list(urls_buffer)
    x_print("Saving memory")
    urls_buffer = save_list(urls_buffer, "./intelligence/data/urls")
    
    x_print("Visited sites memory saved")
    urls_visited = save_list(urls_visited, "./intelligence/data/urls_visited")

    x_print("Visited downloaded images memory saved")
    urls_images = save_list(urls_images, "./intelligence/data/urls_images")

    stop_urls = save_list(stop_urls, "./intelligence/stop_urls")
    
    x_print("stop_urls saved")
    x_print("dictionary saved")
    x_print("learned_relations saved")

def load_memory():

    global urls_buffer
    global urls_images

    global urls_visited
    global query_history
    global search_boost
    global dictionary
    global learned_relations
    global learned_keywords, phrase_dictionary
    global stop_urls

    x_print("Loading memory")
    urls_buffer = load_list("./intelligence/data/urls", urls_buffer)
    x_print("Url memory loaded")

    urls_visited = load_list("./intelligence/data/urls_visited", urls_visited)
    x_print("Visited sites memory loaded")

    urls_images = load_list("./intelligence/data/urls_images", urls_images)
    x_print("Downloaded images memory loaded")

    stop_urls = load_list("./intelligence/stop_urls", stop_urls)
    dictionary = load_list("./intelligence/dictionary", dictionary)
    
    learned_relations = load_list("./intelligence/learned_relations", learned_relations)
    learned_keywords = load_list("./intelligence/learned_keywords", learned_keywords)
    phrase_dictionary = load_list("./intelligence/phrase_dictionary", phrase_dictionary)

    x_print("stop_urls loaded")
    x_print("dictionary loaded")
    x_print("learned_relations loaded")
    x_print("learned_keywords loaded")
    x_print("phrase_dictionary loaded")

def insert_url(url):
    import sqlite3
    conn = sqlite3.connect("./archives/data/data-miner.db")
    c = conn.cursor()
    c.execute("INSERT INTO urls (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

def insert_search_urls(url, query):
    try:

        import sqlite3
        db_file = "./archives/data/data-miner.db"
        conn = sqlite3.connect(db_file)

        c = conn.cursor()
        c.execute("INSERT INTO search (url, query) VALUES (?,?)",
                  (url, query))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


def check_keywords_in_urls(url):
    global query_history

    for key in query_history[0].split(" "):
        key = str(key).lower()
        url = str(url).lower()
        if len(key) >= MIN_WORD_SIZE:
            if url.find(key) >= 0:
                return True
    return False


def insert_url_data(url, title, short_text):

    global current_query
    title = clean_text(title)
    short_text = clean_text(short_text)

    # To be able to search in the memory the
    # query will be the key for the data
    x_print("Learning keywords in the TITLE")
    # key -> data
    try:
        db_file = "./archives/data/data-miner.db"

        import sqlite3
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("INSERT INTO url (url, title, text) VALUES (?,?,?)",
                  (url, title, short_text))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)


def check_url(url):
    if (url == None):
        return False
    if url.find(str(".html")) >= 0:
        return True
    if url.find(str(".pdf")) >= 0:
        return False
    if url.find(str(".php")) >= 0:
        return True
    if url.find(str(".asp")) >= 0:
        return True
    if url.find(str(".aspx")) >= 0:
        return True
    if url.find(str(".xml")) >= 0:
        #download(url)
        return False
    if url.find(str(".xls")) >= 0:
        #download(url)
        return False
    if url.find(str(".htm")) >= 0:
        return True
    if url.find(str(".zip")) >= 0:
        #download(url)
        return False
    if url.find(str(".js")) >= 0:
        return False

    # Download intresting files
    if url.find(str(".mp3")) >= 0:
        #download(url)
        return False
    if url.find(str(".mp4")) >= 0:
        # download_x(url)
        return False
    if url.find(str(".m3u")) >= 0:
        # download_x(url)
        return False
    if url.find(str(".mkv")) >= 0:
        # download_x(url)
        return False
    return True


def check_url_img(url):
    if (url == None):
        return False
    if url.find(str(".html")) >= 0:
        return False
    if url.find(str(".pdf")) >= 0:
        return False
    if url.find(str(".php")) >= 0:
        return False
    if url.find(str(".asp")) >= 0:
        return False
    if url.find(str(".aspx")) >= 0:
        return False
    if url.find(str(".xml")) >= 0:
        return False
    if url.find(str(".xls")) >= 0:
        return False
    if url.find(str(".htm")) >= 0:
        return False
    if url.find(str(".zip")) >= 0:
        return False
    if url.find(str(".js")) >= 0:
        return False
    if url.find(str(".mp3")) >= 0:
        download(url)
        return False
    return True


def check_media(url):
    if url == None:
        return False
    check_url = url.lower()
    if check_url.find(str(".html")) >= 0:
        return False
    if check_url.find(str(".pdf")) >= 0:
        return False
    if check_url.find(str(".php")) >= 0:
        return False
    if check_url.find(str(".asp")) >= 0:
        return False
    if check_url.find(str(".aspx")) >= 0:
        return False
    if check_url.find(str(".xml")) >= 0:
        return False
    if check_url.find(str(".xls")) >= 0:
        return False
    if check_url.find(str(".htm")) >= 0:
        return False
    if check_url.find(str(".zip")) >= 0:
        return False
    if check_url.find(str(".docx")) >= 0:
        return False
    if check_url.find(str(".doc")) >= 0:
        return False
    # There is a small bug with the end of the file
    # this function should clean de url
    for media_ext in media_files.split(","):
        if check_url.find(str("."+media_ext.strip())) >= 0:
            download(url)
            return True
    if DOWNLOAD_EVERYTHING == 'ON':
        download(url)
    return False


def clean_filename(file_name):
    if (file_name.find("?") >= 0):
        end = file_name.find("?")
        file_name = file_name[0:end]
    return file_name


def download(url):

    global urls_global_session_memory
    global img_count
    global url_count
    global current_quality_score
    global current_url
    global current_img_src
    global current_img_keywords
    global current_patterns_hits

    save_path = './media/'
    ext = url.split(".")[-1]
    file = url.split("/")[-1]
    file = clean_filename(file)

    target = str(save_path) + str(file)

    if url not in urls_global_session_memory:

        current_url = url

        try:
            current_quality_score = 0
            current_img_keywords = ""
            current_patterns_hits = ""
            x_print("First test the image URL")
            x_print("Url: " + current_url)
            result = url__img_verification(url)

            if (result):
                x_print("VERIFICATION PASSED...")
                x_print("Second url test for image source")

                #result = verify_keywords_in_link(url)
                # if (not result):
                #    x_print("VERIFICATION Failed...")
                #    return None

            x_print("Second test for image URL")
            x_print("VERIFICATION PASSED...")
            # NEED TO VERIFY KEYWORDS

            if (result):

                try:
                    target = get_image(url)
                except Exception as e:
                    x_print(e)
                    try:
                        relax(TIME_LOCK)
                        import wget
                        wget.download(str(url), str(target))
                    except Exception as e:
                        x_print(e)
                        print("Exception with the requests...")
                        x_print("Download ERROR...\n")
                        return None

                # Set the image source
                current_img_src = url
                x_print("For security reasons pacing at \n" +
                        str(TIME_LOCK) + " secondes...")
                relax(TIME_LOCK)
            else:
                x_print("DOWNLOAD AI TESTS FAILED...\n")
                return None

        except Exception as e:
            x_print(e)
            x_print("Exception downloading")
            x_print("URL causing error is: " + str(url) + "\n")
            x_print("File download location: " + str(target) + "\n")
            relax(TIME_LOCK)

            if(1 < img_count):
                img_count = img_count - 1

            return None

    # What ever site must be
    # inserted in the images buffer
    if (url in urls_buffer):
        urls_buffer.remove(url)

    img_count = img_count + 1

    verify_image_size(str(target), str(url))
    
    return True


def download_x(url):
    save_path = './downloads/'
    file = url.split("/")[-1]
    file = clean_filename(file)
    target = str(save_path) + str(file)
    try:
        target = get_image(url)
    except Exception as e:
        print(e)
        x_print("Requests error...")
        try:
            import wget
            wget.download(str(url), str(target))
        except Exception as e:
            x_print(e)
            x_print("Exception backup wget downloading")
            return False

    return True


def extract_keywords(filename):

    if filename == None:
        return None

    keywords = filename.replace("-", " ")
    keywords = keywords.replace("/", " ")
    keywords = keywords.replace(".", " ")
    keywords = keywords.replace("http:", " ")

    items = ["  ", "+", "%", "&", "*", "_", "!", "@", "#", "$",
             "(", ")", ".", "-", ".", "[", "]", "jpg", "jpeg", "gif", "bmp", "svg", "png"]

    for item in items:
        while keywords.find(item) >= 0:
            keywords = keywords.replace(item, " ")

    buffer = ""
    for word in keywords.split(" "):

        if word == None:
            continue

        if len(word) > MAX_WORD_SIZE:
            continue

        if len(word) < MIN_WORD_SIZE:
            continue

        if (word.isnumeric()):
            continue

        buffer = buffer + " " + word
        buffer = clean_text(buffer)
     
    keywords = str(buffer)

    return keywords


def get_image(url):

    if first_check(url) == False:
        return None

    # file name creating with timestamp
    global current_img_keywords

    print("STARTING IMAGE DOWNLOAD PROCESS")
    print("url: " + str(url))

    try:
        r = get_img_request_url(url)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.

            current_img_keywords = extract_keywords(url)
            current_img_keywords = clean_url_html_tags(current_img_keywords)
            
            filename = generate_img_file_name(r, url, current_img_keywords)

            with open("./media/" + filename, 'wb') as f:
                import os
                shutil.copyfileobj(r.raw, f)

            target = "./media/" + filename
            return target
    except:
        pass

def generate_img_file_name(r, url, current_img_keywords):

    ext_guess = url.split(".")[-1]
    file_guess = url.split("/")[-1]

    ext = get_extension(r)
    filename = str(uuid.uuid4())

    if (current_img_keywords != None) and (current_img_keywords != " ") and (current_img_keywords != "") and (len(current_img_keywords) > MIN_WORD_SIZE):
        print("Image keywords: " + current_img_keywords)
        new_file_name = current_img_keywords.replace(" ", "-")
        new_file_name = new_file_name.replace("_", "-")
        new_file_name = new_file_name.replace("+", "-")
        new_file_name = new_file_name.replace("https", "")
        new_file_name = new_file_name.replace("http", "")
        new_file_name = new_file_name.replace("com", "")
        new_file_name = clean_file_name(new_file_name)

        if len(new_file_name) >= MIN_WORD_SIZE:
            if len(new_file_name) <= MAX_FILE_NAME_SIZE:
                filename = new_file_name + "-" + filename[0:4] + "." + ext
            else:
                filename = new_file_name[0:int(
                    MAX_FILE_NAME_SIZE/2)] + "-" + filename[0:4] + "." + ext
        else:
            filename = filename[0:4] + "." + ext
    else:
        filename = filename[0:4] + "." + ext

    return filename


def get_img_request_url(url):
    try:
        if PROXY_ACTIVATED == 'ON':
            global proxies
            r = requests.get(url, stream=True)
            return r
        else:
            r = requests.get(url, stream=True, timeout=10)
            return r
    except:
        print("ERROR - get_img_request_url")
        try:
            r = requests.get("https://www.google.com", stream=True)
            r = requests.get(url, stream=True)
            return r
        except:
            print("ERROR - cant recover get_img_request_url")
            return None
        
        


def verify_image_size(target, web_src):
    print("Verification of image...")
    print("Before transfer to depot...")
    try:
        image_size_check(target, web_src)
    except Exception as e:
        print(e)
        print("Exception in get_size_img_check")


def clean_file_name(file_name):

    file_name = file_name.replace("--", "")      
    file_name = file_name.replace("picture-", "")
    file_name = file_name.replace("photo-", "")
    file_name = file_name.replace("image-", "")
    file_name = file_name.replace("-com", "")
    file_name = file_name.replace("-www", "")
    file_name = file_name.replace("-v1", "")
    file_name = file_name.replace("-v2", "")
    file_name = file_name.replace("-net", "")
    file_name = file_name.replace("com-", "")
    file_name = file_name.replace("www-", "")
    file_name = file_name.replace("v1-", "")
    file_name = file_name.replace("v2-", "")
    file_name = file_name.replace("net-", "")
    file_name = file_name.replace("image-", "")
    file_name = file_name.replace("-wikipedia", "")
    
    if "-" == file_name[0]:
        file_name = file_name[1:len(file_name)-1]
    
    return file_name

def image_size_check(img_file, img_src):

    if (img_file == None):
        return None
    if (img_src == None):
        return None

    if (img_file == 'None'):
        return None
    if (img_src == 'None'):
        return None

    if (img_file == ''):
        return None
    if (img_src == ''):
        return None

    import os
    import shutil

    global images_session_memory
    global current_image_alt_text_test

    file_size = os.path.getsize(img_file)

    # fix file_name bug
    file_name = img_file.replace("--","")

    print("Image Name: " + str(file_name))
    print("Image size: " + str(file_size))
    global current_img_size
    current_img_size = file_size
    try:
        if (file_size > MAX_WORKSPACE_SIZE):
            if not img_file in images_session_memory:
                shutil.copy2(str(img_file), './archives/workspace/')
                images_session_memory.append(img_file)

                file = img_file.split("/")[-1]
                file = clean_filename(file)
                file_name = './archives/workspace/' + file

                print("Image is very large should be verified by the user")
                print("Path: " + file_name)

        if (file_size < MIN_IMAGE_SIZE):
            if not img_file in images_session_memory:
                shutil.copy2(str(img_file), './archives/workspace/')
                images_session_memory.append(img_file)

                file = img_file.split("/")[-1]
                file = clean_filename(file)
                file_name = './archives/workspace/' + file

                print("Image is very small it is an Icon")
                print("Path: " + file_name)

        global current_url

        print("Image is perfect")
        print("Path: " + file_name)

        # INTERFACE HTML DUMP
        dump_html(str(file_name), str(img_src))
    
    except Exception as e:
        print(e)
        print("Exception in get_size_img_check()")
        print("Path: " + file_name)
        pass


def format_url(url):
    try:
        from urllib.parse import urlparse
        url = urllib.parse.unquote(url)
    except Exception as e:
        print(e)
    return url

def refresh_web():
    global driver
    driver.refresh()

def init_web():
    global driver
    
    try:
        from selenium import webdriver
        driver = webdriver.Firefox(executable_path="./tools/geckodriver")
        driver.maximize_window()
        driver.get(PROGRAM_PATH)
        driver.refresh()        
    except:
        pass

def refresh_web():  # first import the module
    try:
        driver.refresh()
    except:
        pass

def get_DB_search_results(query):

    import search_history as se_history
    my_results = []
    try:
        import search_history as se
        my_results = se.search_database(query)
        print("Found in history: " + str(len(my_results)))

        # clean all noise
        my_results = clean_up_buffer(my_results)
        print("After buffer cleanup - clean_up_buffer(results)" + str(my_results))
        
        my_results = check_search_urls(my_results)
        print("After more cleanup - check_search_urls(results)" + str(my_results))
        
        my_results = check_critical_amount_of_urls(my_results)
        print("After still more cleanup - check_critical_amount_of_urls(results)" + str(my_results))
        print("That's all the cleaning we can do for now...")
    except:
        pass

    return my_results

def get_search_urls(query):

    search_urls = []
    google_results = []
    yahoo_results = []
    bing_results = []
    yandex_results = []
    duck_results = []
    
    if query == None:
        return search_urls

    import search_engine as search_interface

    try:
        google_results = search_interface.search_google(query)
    except:
        pass

    try:
        yahoo_results = search_interface.search_yahoo(query)
    except:
        pass

    try:
        bing_results = search_interface.search_bing(query)
    except:
        pass

    try:
        duck_results = search_interface.search_duck(query)
    except:
        pass

    try:
        yandex_results = search_interface.search_yandex(query)
    except:
        pass

    search_urls = insert_in_buffer(yandex_results)
    search_urls = insert_in_buffer(duck_results)
    search_urls = insert_in_buffer(yahoo_results)
    search_urls = insert_in_buffer(bing_results)
    search_urls = insert_in_buffer(google_results)
    search_urls = check_search_urls(search_urls)

    for i in search_urls:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, query)
        print("inserting in DB: " + str(i))

    print("Results found: " + str(len(search_urls)))

    return search_urls

# starting list will be save to urls.txt
# each spiders url will verify html content and extract new urls to the file
# the urls.txt are the full for the spider

def setup_process(user_input):
    # x_print("STARTING SETUP PROCESS")
    if (user_input == "y"):
        clean_memory()

        # clean images folders
        delete_folder('./media')
        delete_folder('./interface')
        delete_folder('./html')

        global urls_visited
        global urls_buffer

        import pickle

        # open a file, where you ant to store the data
        file = open('urls_data', 'wb')
        pickle.dump(urls_visited, file)

        file.close()
        import pickle
        with open('urls_data', 'rb') as f:
            newlist = pickle.load(f)
        
        urls_memory = insert_in_buffer(urls_visited)
        urls_memory = insert_in_buffer(urls_buffer)
        urls_memory = save_urls_memory(urls_memory, "./intelligence/urls_memory")
        urls_memory.sort()
        
        urls_visited.clear()
        urls_buffer.clear()

        # Stats
        x_print(str(len(urls_buffer)) + " In the main buffer")
        x_print(str(len(urls_visited)) + " In the visited websites")
    
    else:
    
        # Load image-miner url global_memory
        load_memory()

def clean_memory():
    with open("./intelligence/data/urls", "w", encoding="utf-8") as file:
        file.write("")

    with open("./intelligence/data/urls_visited", "w", encoding="utf-8") as file:
        file.write("")

    with open("./intelligence/data/urls_images", "w", encoding="utf-8") as file:
        file.write("")


def delete_folder(my_path):
    import os
    import os.path

    for root, dirs, files in os.walk(my_path):
        for file in files:
            os.remove(os.path.join(root, file))

def clean_url_html_tags(url_keywords):
    url_keywords = url_keywords.replace("https", "")
    url_keywords = url_keywords.replace("http", "")
    url_keywords = url_keywords.replace("html", "")
    url_keywords = url_keywords.replace("php", "")
    url_keywords = url_keywords.replace("www", "")
    url_keywords = url_keywords.replace("com", "")
    return url_keywords

def learn(text):

    global synonyms
    global dictionary
    global phrase_dictionary
    global learned_relations
    global learned_keywords
    
    try:

        index = 0

        # Insert some word in the system dictionary
        text = clean_text(str(text))
 
        for i in text.split("."):
            # Insert the phrase in 
            # learned relation buffer
            phrase_dictionary.append(i)
            
            index = index + 1
            
            list_words = i.split(" ")

            # Iterate thru the phrase
            for word_in_phrase in list_words:
                
                # clean the word
                word_in_phrase = clean_word(str(word_in_phrase))
                
                # copy the word for to 
                # find the synonym later
                word_for_syn = word_in_phrase

                import nlp_tools as n
                
                try:
                    # find the word definition in wordnet 
                    # for system specific learned keywords
                    # for futur boost match and boost search
                    definition = n.definition(word_in_phrase)

                    if len(definition) == 0:
                        continue
                        
                    # add the definition to the dictionary
                    for defi in definition:
                        word_in_phrase = word_in_phrase + " : " +str(defi)
                    
                    
                    dictionary.append(word_in_phrase)
                
                except:
                    pass
                
                try:
                    synonyms_definitions = n.synonyms(word_for_syn)
                    all_synonyms = ""
                    for synonym in synonyms_definitions:
                        all_synonyms = all_synonyms + ":" + synonym

                    word_for_syn = word_for_syn + ":" + all_synonyms
                    synonyms.append(word_for_syn)
                except:
                    pass

        learned_relations = save_list(
            learned_relations, "./intelligence/learned_relations")
            
        phrase_dictionary = save_list(
            phrase_dictionary, "./intelligence/phrase_dictionary")

        dictionary = save_list(dictionary, "./intelligence/dictionary")
        synonyms = save_list(synonyms, "./intelligence/synonyms")

        learned_relations.sort()
        phrase_dictionary.sort()
        dictionary.sort()
        synonyms.sort()

    except:
        input("Exception in Learn...")
        pass

    # cleans doubles in 
    # dictionary and sysnonyms
    check_for_double_dic_syn()

    # Related words research and exploration
    related_words_research()

    pass

def related_words_research():

    # The frequency depends on the size of the text
    # need to calculatr de frequency ratio
    # for 1000 words what is the frenquency
    
    size_group = 1
    token_group = tokenize_by_group(size_group)
    nlp_freq_special_group(token_group, 10)

    size_group = 2
    token_group = tokenize_by_group(size_group)
    nlp_freq_special_group(token_group, 5)

    size_group = 3
    token_group = tokenize_by_group(size_group)
    nlp_freq_special_group(token_group, 3)

    size_group = 4
    token_group = tokenize_by_group(size_group)
    nlp_freq_special_group(token_group, 2)

    size_group = 5
    token_group = tokenize_by_group(size_group)
    nlp_freq_special_group(token_group, 2)

def tokenize_by_group(size_group):
    
    global current_preview
    
    index = 1
    preview_temp = ""

    for word in current_preview.split():
        
        if (size_group==index):
            preview_temp = preview_temp + " " + word + " ^ "
            index = 0

        preview_temp = preview_temp + " " + word  
        index = index + 1
    
    tokenized_text = preview_temp.split("^")
    return tokenized_text
    
def load_list(file_name, urls_list):

    # read url file
    with open(file_name, "r") as file:
        # reading each line"
        for line in file:
            url = clean_url(line)
            urls_list.append(str(url))

    clean_list = []
    for i in urls_list:
        if i == None:
            continue

        if not i in clean_list:
            clean_list.append(i)

    urls_list = []

    for i in clean_list:
        if i not in urls_list:
            urls_list.append(i)

    return urls_list


def dump_email_data(file_name, data):
    with open(file_name, "a") as file:
        x_print("filename: " + file_name)
        x_print("data: " + data)
        file.write(data + "\n")
        file.close()


def check_email(url):
    if (url == None):
        return None
    # EMAIL Extraction intelligence to be developped
    if (url.find("mailto:") >= 0):
        dump_email_data("./intelligence/email", url)
        url = urls_buffer[0]
        x_print("Email found adding to email list...")


def relax(sec):
    time.sleep(sec)

# Special print
# consol, log file and interface


def x_print(data):
    print(data)
    debug_info(data)


def debug_info(info):
    # print to screen
    if DEBUG_LOG == 1:
        from datetime import datetime
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f = open("debug", "a")
        f.write("\n" + str(time) + " : ")
        f.write(str(info))
        f.close()


def save_to_archive(src, trg):
    # importing required packages
    import os
    import shutil
    from pathlib import Path

    files = os.listdir(src)

    # iterating over all the files in
    # the source directory
    for fname in files:
        # copying the files to the
        # destination directory
        if (fname.find(".") >= 0):
            shutil.copy2(os.path.join(src, fname), trg)


def get_text(the_page):

    soup = BeautifulSoup(the_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'style',
        'script',
        'css',
        'link',
        'javascript',
        # there may be more elements you don't want, such as "style", etc.
    ]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    output = clean_text(output)
    return output


def load_stop_words():
    global stop_words
    file = open("./intelligence/stop_words", "r")
    stop_words = file.readlines()


def word_size(text, size):
    rebuild_text = ""
    # preformating word
    for word in text.split():
        if len(word) < size:
            rebuild_text = rebuild_text
        else:
            rebuild_text = rebuild_text + " " + word

    return rebuild_text


def clean_url(url):
    url = url.replace("\n", "")
    return url.strip()


def check_stop_words(word):
    if (word == '') or (word == None):
        return None

    if (len(word) <= MIN_WORD_SIZE):
        return None

    # preformating word
    for i in stop_words:
        stop_words.remove(i)
        i = i.replace("\n", "")
        stop_words.append(str(i))

    if word in stop_words:
        return ""
    return word


def clean_word(word):
    if word == None:
        return None
    # Normalize the string
    word = word.lower()
    for char in word:
        # String character cleansing
        if char in "…[]#&\':–(){};|*#/+\"\\~^–":
            word = word.replace(char, " ")
    return word


def clean_pattern(pattern):
    if (pattern == None):
        return None
    # pattern pre-processing
    pattern = clean_word(pattern)

    for char in pattern:
        # Only permitted characters in patterns
        if not char in "qazwsxedcrfvtgbyhnujmikolp1234567890":
            pattern = pattern.replace(char, " ")
    return pattern


def verify_keywords_in_link(link):
    if KEYWORDS_IN_LINK == 'OFF':
        return True

    x_print("LINK VERIFICATION")
    global current_quality_score
    current_quality_score = 0
    score = 0

    for pattern in query_history[0].split(" "):
        link = link.lower()
        pattern = pattern.lower()
        pattern = pattern.replace("s", "")

        # FIRST CONTACT WITH INTELLIGENCE
        # Look for mathematical stem or root of word
        if (len(pattern) < MIN_STEM_SIZE):
            stem = pattern[0:len(pattern)]
        else:
            stem = pattern[0:MIN_STEM_SIZE]

        # x_print("Needed stem for partial match: " + stem)

        if (link.find(stem) >= 0):

            x_print("MATCH pattern is " + str(pattern) +
                    "with stem: " + str(stem))

            if (len(pattern) >= MIN_WORD_SIZE):
                score = score + 1

                if score >= NUMBER_OF_KEYWORDS_IN_LINK:

                    x_print("ACCEPTED LINK - PATTERN MATCH SCORE : " +
                            str(current_quality_score))
                    x_print("PATTERN: " + str(pattern))
                    x_print("URL: " + str(link))
                    x_print("SCORE: " + str(score))
                    x_print("MATCHING KEYWORDS FOUND IN LINK - PASSED")
                    current_quality_score = current_quality_score + score
                    return True
            else:
                x_print("MATCH is canceled pattern is to small: MIN_WORD_SIZE")
        else:
            x_print("NO MATCH")
            x_print("URL: " + link)

    x_print("\nNO MATCHING KEYWORDS FOUND IN LINK - FAILED")
    x_print("URL: " + link)
    x_print("WE SHOULD NO FOLLOW THIS ROAD\n")
    return False


def verify_url_with_query(url):
    for word in str(query_history[0]).split(" "):
        if url.find(word) >= 0:
            return True
    return False


def is_pattern_in_spam_filter(pattern, q_bonus):
    global spam_score
    global pattern_memory
    global current_patterns_hits
    global current_query
    global spam_filter
    
    if pattern == "" or pattern == " ":
        print("Invalid pattern")
        return spam_score

    try:
        # if not pattern in pattern_memory:
        if is_pattern_spam(pattern, 1):
            pass
            #print("NEGATIVE SPAM Match: " + str(pattern) + " spam_score="+str(spam_score))
            #spam_score = spam_score - 1
    except Exception as e:
        print(e)
        print("ERROR in is_pattern_in_query")
        return spam_score

    return spam_score


def is_pattern_spam(pattern, q_bonus):
    global spam_score
    global spam_filter
    global current_patterns_hits

    for line in spam_filter:
        try:
            if not pattern in pattern_memory:
                if line.find(pattern) >= 0:
                    spam_score = spam_score - q_bonus
                    print("SPAM: " + str(pattern) +
                          " spam_score="+str(spam_score))
                    pattern_memory.append(pattern)
                    current_patterns_hits = str(current_patterns_hits) + " - " + str(pattern)

        except Exception as e:
            print(e)
            print("ERROR in is_pattern_spam")
            return spam_score

    return spam_score


def is_pattern_in_query(pattern, q_bonus):
    global current_quality_score
    global pattern_memory
    global current_patterns_hits
    global match_boost_with_query

    if pattern == "" or pattern == " ":
        print("ERROR invalid pattern")
        return current_quality_score

    if MATCH_BOOST == 'ON':
        temp_query = current_query + match_boost[0]
    else:
        temp_query = current_query
    
    try:
        #if not pattern in pattern_memory:
        if temp_query.find(pattern) >= 0:
            temp_query = temp_query.replace(pattern, "")
            current_quality_score = current_quality_score + q_bonus
            print("Match: " + str(pattern) + " QS="+str(current_quality_score))
            current_patterns_hits = current_patterns_hits + " - " + pattern

    except Exception as e:
        print(e)
        print("ERROR in is_pattern_in_query")

    return current_quality_score

def clean_code_noise(text):
    global code_filter
    for element in code_filter:
        text = text.replace(" " + element + " ", "")
    return text

def prepare_query(query):
    query = clean_text(query)
    query = query.replace("-", " ")
    query = query.replace(",", "")
    return query

def prepare_preview(text):

    if (text==None) or (text==""):
        return None

    global current_quality_score
    global current_preview, current_query
    
    current_quality_score = 0
    current_preview = ""

    current_query = prepare_query(current_query)
    list_keywords = current_query.split()

    mark = 0
    text = text.replace("google noscript manage", "")          

    SEARCH_CHUNK_SIZE = 250

    for keyword in list_keywords:    
        from nltk.stem import PorterStemmer
        stemmer = PorterStemmer()
        stem = stemmer.stem(keyword)       
        stem = stem.lower()

        try:
            while (mark<len(text)):
                start = text.find(stem, mark + 5)
                if (start==-1):
                    mark = len(text)
                if start >= 0:
                    str1 = 0 
                    end = 0
                    
                    if (mark-SEARCH_CHUNK_SIZE<0):
                        str1 = 0 
                    
                    end = mark+SEARCH_CHUNK_SIZE
                    
                    if (mark+SEARCH_CHUNK_SIZE>len(text)):
                        end = len(text)-1
                    
                    current_preview = current_preview.strip().capitalize() + "[...]" + str(text[str1:end]).capitalize() 
                    mark = start + SEARCH_CHUNK_SIZE

                    # If the keyword is in the html text 
                    # extra point for quality of the web pasge
                    current_quality_score = current_quality_score + 1

                    if (len(current_preview) > 500):
                        break
                else:
                    current_quality_score = current_quality_score - 1
        except:
            pass

    current_preview = clean_text(current_preview.capitalize())
    current_preview = current_preview.capitalize()
    current_preview = str(text[0:PREVIEW_SIZE]).capitalize() + current_preview.capitalize()
    
    x_print("PREVIEW: " + str(current_preview.capitalize())) 

    return current_preview

def calculate_quality_score(short_text):

    if short_text == None or short_text == MIN_WORD_SIZE:
        return 0

    try:
        global query_history
        global current_quality_score
        global pattern_memory

        pattern = ""
        patterns = populate_patterns(short_text)
        print("MATRIX: " + str(patterns))
        meter = 0
        pattern_memory = []
        for pattern in patterns:
            if meter < ANALYSIS_MAX_WORDS:
                #if(pattern_first_check(pattern)):
                if len(pattern) > MIN_STEM_SIZE:
                    current_quality_score = is_pattern_in_query(pattern, 10)
            meter = meter + 1
        return current_quality_score
    except Exception as e:
        print(e)
        print("Exception in calculate_quality_score")
        return current_quality_score  
              
def special_bonus(short_text):
    # BONUS POINTS
    global current_quality_score
    bonus = len(short_text)
    current_quality_score = current_quality_score + int(bonus/10)

    print("quality score=" + str(current_quality_score))
    return current_quality_score

def spam_check(short_text, score):

    if short_text == None or short_text == MIN_WORD_SIZE:
        return 0

    global spam_score
    spam_score = score

    try:
        global query_history
        global current_quality_score
        global pattern_memory

        pattern = ""
        patterns = populate_patterns(short_text)
        print("MATRIX: " + str(patterns))
        meter = 0
        pattern_memory = []
        for pattern in patterns:
            if meter < ANALYSIS_MAX_WORDS:
                # if(pattern_first_check(pattern)):
                if len(pattern) > MIN_STEM_SIZE:
                    spam_score = is_pattern_in_spam_filter(pattern, 1)
            meter = meter + 1
    except Exception as e:
        print(e)

    print("spam_score=" + str(spam_score))
    return spam_score

def verify_content(url, title, text):
    try:            
        if (title == None) or (text == None) or (url == None):
            return False

        if (title == "") or (text == "") or (url == ""):
            return False
    
        x_print("\n\nSTARTING PAGE TEXTUAL") 
        x_print("CONTENT VERIFICATION CHECKLIST\n")

        url, title, text \
            = prepare_strings(url, title, text)

        global current_preview
        preview = current_preview

        global current_nb_words_in_text
        current_nb_words_in_text = len(text.split(" "))
        
        global current_quality_score
        current_quality_score = 0

        global current_freq_score
        current_freq_score = 0 

        x_print("TITLE: " + str(title))
        x_print("url: " + str(url))
        x_print("PREVIEW: " + str(current_preview))
        x_print("WORDS IN TEXT: " + str(current_nb_words_in_text))
         
        # TESTING FREQUENCY ANALYSYS THINKING OF COMBINING
        # DIFFERENT STRATEGIES TO ANALYSE DE QUALITY OF THE
        # INFORMATION BEFORE STARTING FULL ANALYSIS
        try:        
            x_print("PRILIMINARY KEYWORD")
            x_print("DISTRIBUTION VERIFICATION TEST")

            full_concepts_string = ""
            
            # calculate de frequency needed depending on the size 
            # of the text - THIS CALCULATION NEEDS TO BE TESTED
            fst = (current_nb_words_in_text / 1000) * 5 
            if fst > 15 : fst = 15

            # calculate frencency of keywords in full text
            current_freq_score, freq, concepts  = nlp_freq_special(text, fst)
        
            # concatanate concepts
            for i in concepts:
                full_concepts_string = full_concepts_string + " " + i

            # QS quick calculation
            current_quality_score = calculate_quality_score(full_concepts_string)

            x_print("FREQUENCY MATRIX: " + str(freq))
            x_print("MAIN CONCEPTS: " + str(full_concepts_string))
            x_print("FREQUENCY SCORE: " + str(current_freq_score))
            x_print("MAIN CONCEPT QUALITY SCORE: " + str(current_quality_score))

        except:
            print("Error in nlp_freq_special")

        # START VERIFYING URL, TITLE AND TEXT
        url, title, preview, text, current_quality_score \
            = process_web_content(url, title, preview, text)
        
        save_keywords_to_disk(title,preview)
    
        result = Compare_and_flush_results(url, title, preview, text)
    
        return result
    
    except:
        print("ERROR")

    return False

def prepare_strings(url, title, text):
    url = str(trim(url))
    title = str(trim(title))
    text = str(trim(text))
    title = title.capitalize()
    text = text.capitalize()
    return url, title, text

def check_for_double_dic_syn():

    global dictionary
    global synonyms

    dictionary = load_list("./intelligence/dictionary", dictionary)
    synonyms = load_list("./intelligence/synonyms", synonyms)

    dictionary = save_list(dictionary, "./intelligence/dictionary")
    synonyms = save_list(synonyms, "./intelligence/synonyms")

def process_web_content(url, title, preview, text):
    global current_quality_score
    global current_query_preview

    if (title != None):
        words_in_title = len(title.split(" "))
        MIN_WORDS_NEEDED = 1

        if (words_in_title>MIN_WORDS_NEEDED):
            try:  
                current_quality_score = 0
                current_quality_score = calculate_quality_score(title)
                x_print("QS in TITLE is = " + str(current_quality_score))
            except:
                print("Error quality score title")    
            
            try:
                spam_score = spam_check(title, 0)
                x_print("SPAM in TITLE is = " + str(spam_score))
            except:
                print("Error spam score title")    
            
            current_quality_score = current_quality_score + spam_score
            x_print("QS in TITLE less spam score is= " + str(current_quality_score))

    if (preview != None):

        words_in_preview = len(preview.split(" "))
        MIN_WORDS_NEEDED = 15

        if (words_in_preview>MIN_WORDS_NEEDED):
            try:
                current_quality_score = calculate_quality_score(current_preview)
                x_print("QS in PREVIEW is = " + str(current_quality_score))
            except:
                print("Error quality score current_query_related_full_text")    
            
            try:
                spam_score = spam_check(current_preview, 0)
                x_print("SPAM in PREVIEW is = " + str(spam_score))
            except:
                print("Error quality score PREVIEW")    
            
            current_quality_score = current_quality_score + spam_score
            x_print("QS TOTAL SCORE less new spam score is= " + str(current_quality_score))
        
            x_print("QS is now = " + str(current_quality_score))

    x_print("QS is now = " + str(current_quality_score))

    if DEEP_ANALYSIS == 'ON':
        text = clean_text(text)
        current_quality_score = calculate_quality_score(text)
        x_print("QS in FULL TEXT WITH THRESHHOLD is = " + str(current_quality_score))
        
        spam_score = 0
        spam_score = spam_check(current_query_preview, spam_score)
        x_print("SPAM in PREVIEW is = " + str(spam_score))
            
        current_quality_score = current_quality_score + spam_score
        x_print("QS TOTAL SCORE less new spam score is= " + str(current_quality_score))
    
    print_loop_info(url)
    
    return url, title, preview, text, current_quality_score 

def calculate_freq(section_of_text):
    global current_freq
    # TEST THE FREQUENCY FOR MORE
    # INFO TO PASS OR FAIL THE SITE

    print("STARTING FREQUENCY TEST")
    # EXTRACT SECTION OF TEXT 
    # RELATED TO THE QUERY
    # TEST DE QUALITY OF VOCABULARY     
    print("FREQUENCY INFO:")
    print("Wordnet thank you NLTK")
    print("Python is beautiful...")

    current_freq = nlp_freq(section_of_text)

    print(current_freq)

def get_long_keywords(text):
    nb_keywords = 0
    long_keywords = ""
    for word in text.split(" "):
        if len(word)>=MAX_WORD_SIZE:
            nb_keywords = nb_keywords + 1
            long_keywords = long_keywords + ", " + word
    return nb_keywords, long_keywords

def final_textual_analsys(current_query, url, title, preview, text):
    global query_size
    global current_text
    global current_preview
    global current_description
    global current_frequency_score
    global current_long_keywords
    global query_history
    global current_quality_score
    
    x_print("QUERY: " + str(query_history[0].capitalize()))
    x_print("TITLE: " + str(title.capitalize()))
    x_print("URL: " + str(url))
    x_print("DB CONTENT: " + str(preview.capitalize()))
    x_print("FINAL QUALITY SCORE (QS) " + str(current_quality_score))

    words_in_text = len(preview.split(' '))
    x_print("TOTAL NUMBER WORDS in preview: " + str(words_in_text))
    words_in_text = len(text.split(' '))
    x_print("TOTAL NUMBER WORDS in text: " + str(words_in_text))
    
    nb_keywords, long_keywords = get_long_keywords(text)
    x_print("Number of LONG KEYWORDS: " + str(nb_keywords))
    x_print("LONG KEYWORDS: " + str(long_keywords))
    
    print_loop_info(current_root_url)
    
    current_long_keywords = long_keywords

    freq_score = 0 
    
    try:
        x_print("KEYWORD DISTRIBUTION")
        freq_score, freq  = nlp_freq(text)
    except:
        print("Error in nlp_freq")

    current_frequency_score = freq_score
    
    x_print("FREQUENCY SCORE: " + str(freq_score))
    x_print("FREQUENCY MATRIX: " + str(freq))
    
    spam_score = 0
    spam_score = spam_check(text, spam_score)
    x_print("RAW DOCUMENT SPAM SCORE: " + str(spam_score))

    current_quality_score = 0
    text = calculate_quality_score(text)
    x_print("RAW DOCUMENT QUALITY SCORE: " + str(current_quality_score))
    
    current_quality_score = current_quality_score + spam_score
    x_print("FINAL QUALITY SCORE: " + str(current_quality_score))
    x_print("FREQUENCY SCORE: " + str(freq_score))
    x_print("SPAM SCORE: " + str(spam_score))

    print_loop_info(url)


def Compare_and_flush_results(url, title, preview, text):
        
    global query_size
    global current_query
    global current_text
    global current_preview
    global current_description
    global query_history
    global current_quality_score
    global current_frequency_score

    try:

        try:
            final_textual_analsys(current_query, url, title, preview, text)
        except:
            print("Error in final_textual_analsys")

        if preview != None:   
            
            final_score = current_quality_score+current_frequency_score

            x_print("PREPARING THE RESULTS...")
            x_print("QUERY: " + str(query_history[0].capitalize()))
            x_print("TITLE: " + str(title.capitalize()))
            x_print("URL: " + str(url))
            x_print("DB CONTENT: " + str(preview.capitalize()))
            x_print("QUALITY SCORE (QS) " + str(current_quality_score))
            x_print("FREQUENCY SCORE (FS) " + str(current_frequency_score))
            x_print("FINAL SCORE (QS) " + str(final_score))
            
            if (final_score <= LEARN_TO_BLOCK_URL):
                block_url(current_url)
                print("BLOCKING : " + str(current_url))
                return False
            
            if final_score >= QUALITY_SCORE:
                print("QUALITY SCORE (QS) TEST PASSED...")
                # Experimental and with feedback
                # from the user for now
                print("STARTING LEARNING...")
                
                # Sub learning program
                learning_cycle()

                print("FINISHED LEARNING CYCLE...")

            insert_data_in_DB(url, title, preview)
    
            if current_frequency_score > FREQ_SCORE:
                print("FREQUENCY SCORE (QS) TEST PASSED...")
                return True
    
            if current_frequency_score > QUALITY_SCORE:
                print("FREQUENCY SCORE (QS) TEST PASSED...")
                return True

        print_loop_info(current_root_url)
        return True
    except:
        print("ERROR")
        pass

def save_keywords_to_disk(title,preview):
    global current_quality_score
    if SAVE_SUBJECT_KEYWORDS == 'ON':
        if current_quality_score > int(QUALITY_SCORE/2):
            data = title + "\n"
            data = data + "\n" + preview + "\n"
            import uuid

            global file_name_keywords
            save_data("./intelligence/keywords_memory/" +
                    file_name_keywords, data)

def test_freq(y,i):
    score = 0
    if match_boost_with_query.find(i):
        score = score * y
        print("OUR RELATED SCORE IS: " + score)
    return score

def insert_data_in_DB(url, title, preview):
    global current_root_url
    x_print("URL PASSES THE QUALITY SCORE TEST: " + str(current_quality_score))
    x_print("INSERTING DATA IN DB")
    insert_url_data(str(url), str(title), str(preview))
    dump_url_html(current_root_url)


def learning_cycle():

    global current_preview
    # Add website root to be spidered

    # Add root URL to spider other
    # pages in the domain 
    # related to the query
    root = get_root(current_url)
    if not root in urls_buffer:
        urls_buffer.append(root)

    # Add the domain to site_of_interst file
    file = open("./intelligence/sites_of_intrest", "a")
    file.write(root + "\n")
    file.close()

    # dump keywords for query boost
    x_print("Learning")
    
    # LEARNING PROCESS
    learn(current_preview)

    # add the TITLE to the learned_keywords 
    # list for learning relation between keywords 
    learned_keywords.append(current_title)

    # Save and reload
    save_list(learned_keywords, "./intelligence/learned_keywords")


def block_url(url):
    #blocked_domain = get_root(url)
    stop_urls.append(url)
    x_print("WILL FOR SOME TIME BLOCK THE SITE")
    # Save block site
    save_list(stop_urls, "./intelligence/stop_urls")


def save_data(file_name, data):
    global current_url
    if (len(file_name) > MAX_FILE_NAME_SIZE):
        file_name = file_name[0:MAX_FILE_NAME_SIZE]

    with open(file_name, "a") as file:
        file.write(str(data))
        file.close()


def clear():
    try:
        if os.name == "posix":
            os.system("clear")
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            os.system("cls")
    except Exception as e:
        print(e)


def populate_patterns(short_text):
    patterns = []
    short_text = clean_text(short_text)
    pattern_counter = 0
    # build patterns
    for pattern in short_text.split(" "):
        if(pattern_first_check(pattern)):
            if (pattern_counter<ANALYSIS_MAX_WORDS):
                pattern_counter = pattern_counter + 1

                if not pattern in patterns:
                    STEP = STEP_SCAN
                    ADJ = 0
                    STEP = STEP_SCAN
                    patterns.append(pattern)
                    print("Adding: " + pattern)

                    while (ADJ < len(pattern)):

                        try:
                            pat = pattern[ADJ:MIN_PATTERN_SIZE+ADJ]
                            if (len(pat) >= MIN_PATTERN_SIZE):
                                pat = clean_word(pat)
                                if not pat in patterns:
                                    patterns.append(pat)
                                    
                                    print("Adding: " + pattern[ADJ:MIN_PATTERN_SIZE+ADJ])

                            ADJ = ADJ + STEP
                        except Exception as e:
                            x_print(e)
                            pass

    return patterns

def eliminate_double(short_text):
    short_text = clean_text(short_text)
    clean_string = ""
    memory = []
    for word in short_text.split(" "):
        if not word in memory:
            clean_string = clean_string + " " + word
            memory.append(word)
    return clean_string


def clean_options(word, clean_option):

    if (clean_option == 1):
        word = clean_word(word)

    if (clean_option == 2):
        word = clean_pattern(word)

    if (clean_option == 3):
        word = clean_word(word)
        word = clean_pattern(word)

    return word

# STILL IN DEVELOPMENT
# This function is not ready and in development
def calculate_CQS(query_size, words_in_text):
    if query_size or words_in_text == None:
        return 1

    MIN_WORDS_FOR_ANALYSES = 10
    if (words_in_text < MIN_WORDS_FOR_ANALYSES):
        return None

    LESS_DIFFICULT = 2
    MORE_DIFFICULT = 1

    cqs = 0.0
    wit = (words_in_text / 300) + 0.1

    tmp_score = int(query_size)*MORE_DIFFICULT/LESS_DIFFICULT * \
        QUALITY_SCORE*MORE_DIFFICULT/LESS_DIFFICULT
    cqs = float(tmp_score) * float(wit)
    return cqs

def pattern_first_check(pattern):
    if (pattern == None):
        return False
    if (pattern == ""):
        return False
    if (pattern == " "):
        return False
    if (pattern == "  "):
        return False
    if len(pattern) < MIN_WORD_SIZE:
        return False
    if len(pattern) > MAX_WORD_SIZE:
        return False
    if len(pattern) < MIN_PATTERN_SIZE:
        return False
    #if len(pattern) > LONG_KEYWORD_SIZE:
    #    return False
    return True


def prepare_pattern(pattern):
    if len(pattern) < MIN_WORD_SIZE:
        return False
    if len(pattern) > MAX_WORD_SIZE:
        return False
    if len(pattern) < MIN_PATTERN_SIZE:
        return False
    #if len(pattern) > LONG_KEYWORD_SIZE:
    #    return False
    pattern = clean_word(pattern)
    #pattern = check_stop_words(pattern)
    return pattern


def clean_numbers(text):
    text_temp = text
    for i in text:
        if(i.isnumeric()):
            text_temp = text_temp.replace(i, "")
            text_temp = text_temp.replace("  ", " ")
    return text_temp

# this function extract urls or img from a url
# it returns a list of urls or images tags
def extract_urls(url, html):
    # Query global_memory self-learning object
    global query_history
    global urls_buffer
    global urls_visited
    global dictionary
    global learned_relations
    global save_count
    global current_quality_score
    global url_count
    global img_count
    global spidered_site_count
    
    extract_meta_content_tags(html)

    x_print("\nPROCESSING url extraction process\nurl: " + url)
    soup = BeautifulSoup(html, "html.parser")
    
    for link in soup.find_all("a"):
        try:
            link = link.get("href")
            link = fix_link(link, url)

            print(link)

            # Checking for email information
            x_print("email information check")
            check_email(link)

            # if (verify_url_with_query(link)):
            if not link in urls_buffer:
                keywords = extract_keywords(link)
                current_quality_score = 0
                current_quality_score = calculate_quality_score(keywords)

                x_print("Quality Score = " + current_quality_score)

                if current_quality_score > QUALITY_SCORE:
                    urls_buffer.append(link)

                if (FREELY_GRAB_URLS == 'ON'):
                    urls_buffer.append(link)

        except Exception as e:
            x_print(e)

    return urls_buffer

def extract_meta_content_tags(html):

    global current_description

    soup = BeautifulSoup(html, "html.parser")
    
    # check_media(url)
    global current_description
    description = soup.find("meta", attrs={'property': 'description'})

    if description != None:
        current_description = description["content"]

def download_website_html_page(html):

    global current_query
    MAX_QUERY_NAME_LENGHT = 20

    import uuid
    filename = str(uuid.uuid4())
    current_query = query_history[0]

    formated_query_string = current_query.replace(" ", "-")
    if (len(formated_query_string) > MAX_QUERY_NAME_LENGHT):
        end = MAX_QUERY_NAME_LENGHT
    else:
        end = len(formated_query_string)

    filename = formated_query_string[0:end] + "-" + filename[0:10]

    with open("./archives/web_content/"+filename+".html", "w") as file:
        x_print("Saving HTML to local disk")
        file.write(str(html))
        file.close()


def check_pattern(pattern, html):
    import re

    # find all between the two parts in the data
    vid_links = re.findall(pattern, html)
    # print(vid_links[0] + ".m3u8") #print the full link with extension

    if (len(vid_links) > 0):
        with open("keywords", "a") as file:
            for rc in vid_links:
                x_print("VOD FOUND")
                x_print("data: " + rc)
                file.write("M3U-VOD : " + str(rc) + "\n")
                file.close()


def fix_link(link, root_url):
    if link == None:
        return None

    if link.find("#") >= 0:
        return None

    root = get_root(root_url)

    if (link.find("http") >= 0):
        return link

    if(link[0:3] == "../"):
        # Dont try this without
        # adult supervision :)
        if (root_url == root):
            return root_url

        folder = root_url.split("/")[-1]
        new_guess = folder + link
        return new_guess

    if(link[0:2] == "//"):

        if(len(link) == 2):
            link = root_url
        link = "https:" + str(link)
        return link

    if(link[0:1] == "/"):
        link = root + str(link)
        return link

    if(link[0:2] == "./"):
        link = root_url + str(link[1:len(link)-1])
        return link

    link = root_url + str(link)
    return link
    
def get_root(url):
    end_of_url = url.find('/', 12)
    root = url[0:end_of_url]
    return root

def clean_text(text):
    # Defensive programming and error handeling
    if (text == False) or (text == True):
        print("Huston we have a problem")
        return None

    if (text == "") or (text == " "):
        print("Huston we have a problem")
        return text

    items = ["\xa0", "|", "(", ")", "[", "]", "{", "}", "  ", "…", "[", "]", "?", "",
             "»", "#", ":", "–", "©", ",", "\t", "#", "*", "/", "\\", "~", "^", "–", "\'", "\"", "=", "<", ">"]
    text = text.lower()

    for filter in items:
        text = text.replace(filter, " ")

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")

    while "  " in text:
        text = text.replace("  ", " ")
    return text

def verify_clean_text(text):

    text = clean_text(text) 

    for i in text.split():
        if len(i) > MAX_WORD_SIZE:
            text = text.replace(" " + str(i) + " ", " ")
            continue
        if len(i) < MIN_PATTERN_SIZE:
            text = text.replace(" " + str(i) + " ", " ")
            continue
        if len(i) > LONG_KEYWORD_SIZE:
            text = text.replace(" " + str(i) + " ", " ")
            continue
    return text

# this function extract urls or img from a url
# it returns a list of urls or images tags


def extract_images(url, html_file):

    global urls_images

    # Images stats
    if (url == None):
        return urls_images

    # Images stats
    if (html_file == None):
        return urls_images

    global img_count
    global current_img_src
    global current_url

    x_print("\nPROCESSING image tags extraction: \nURL: " + url + "\n")
    x_print("Creating soup object...")

    soup = BeautifulSoup(html_file, "html.parser")
    numLink = 0

    x_print("STARTING IMAGE EXTRACTION")
    #soup_memory = soup.find_all("img")
    for link in soup.find_all("img"):

        try:
            # Extracting ATL image info
            # alt information to decode what
            # the images is about
            numLink = numLink + 1
            img_info = link.get("alt")

            result = verify_image_alt_tag(img_info)

            if(result):
                print("verify_image_alt_tag ALT TEST PASSED")

            result = full_img_verification(link, img_info)

            if(result):
                print("full_img_verification TEST PASSED")

            extract_img(link, url)

        except Exception as e:
            x_print(e)
            print("Exception in IMAGE EXTRACTION MAIN FRAME")

    # Double TIME_LOCK
    return urls_images


def full_img_verification(link, img_info):

    print("link : " + str(link))
    if img_info != None:
        print("img_info : " + img_info)

    global current_img_keywords
    current_img_keywords = current_img_keywords.strip()

    print("current_img_keywords : " + current_img_keywords.upper())

    qa = calculate_quality_score(current_img_keywords)
    print("QA: " + str(qa))

    if qa > IMG_ALT_QS:
        return True
    return False

def extract_img(link, url):
    global urls_images
    link = link.get("src")
    if (link != None):
        link = fix_link(link, url)
        if not link in urls_images:
            try:
                result = verify_url_basic_check(link)
            except Exception as e:
                x_print(e)
                return False
            try:
                if result:
                    result = check_media(link)

                    if result == None:
                        return False

                    # Slow down or we will
                    if not link in urls_visited:
                        urls_visited.append(link)
                    if not link in urls_images:
                        urls_images.append(link)
                else:
                    print("Url failed basic test...")
                    return False

            except Exception as e:
                x_print(e)
                return False
    return True

def verify_image_alt_tag(img_tag_text_info):
    global current_quality_score
    global current_image_alt_text_test
    global pattern_memory
    global current_img_keywords

    pattern_memory = []
    current_quality_score = 0
    if img_tag_text_info != None: 
        if (IMG_ALT_VERIFICATION == "ON"):
            if img_tag_text_info != "" or img_tag_text_info != " ":
                print("image the info: ")
                print(img_tag_text_info)
                current_quality_score = calculate_quality_score(img_tag_text_info)
                current_img_keywords = clean_url_html_tags(current_img_keywords.lower()) + " " + \
                    img_tag_text_info.lower()
                print("QA: " + str(current_quality_score))

        if (IMG_ALT_VERIFICATION == "ON"):
            if current_quality_score < IMG_ALT_QS:
                print("IMAGE FAILED ALT VERIFICATION")
                current_image_alt_text_test = False
            else:
                print("IMAGE PASSED ALT VERIFICATION")
                print("EXCELLENTE MATCH...")
                current_image_alt_text_test = True
    return True


def save_list(urls_list_x, file_name_x):
    # write url in visited site file
    if urls_list_x == None:
        return False

    try:
        str_formated_urls = "\n"
        str_formated_urls = str_formated_urls.join(urls_list_x)
        # print(str_formated_urls)
    except:
        pass

    with open(file_name_x, "w", encoding="utf-8") as file:
        file.writelines(str_formated_urls)
        file.close()
    return urls_list_x


def save_urls_memory(urls_list_x, file_name_x):
    # write url in visited site file
    if urls_list_x == None:
        return False

    try:
        str_formated_urls = "\n"
        str_formated_urls = str_formated_urls.join(urls_list_x)
        # print(str_formated_urls)
    except:
        pass

    with open(file_name_x, "a", encoding="utf-8") as file:
        file.writelines(str_formated_urls)
        file.close()
    return urls_list_x


def get_extension(response):
    m_type = response.headers.get("Content-Type", "image/jpeg")
    m_type = m_type.partition(";")[0]

    if "/" not in m_type:
        m_type = "image/" + m_type

    if m_type in MIMETYPE_MAP:
        return MIMETYPE_MAP[m_type]

    exts = mimetypes.guess_all_extensions(m_type, strict=False)
    if exts:
        exts.sort()
        return exts[-1][1:]
    return "txt"


MIMETYPE_MAP = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/x-bmp": "bmp",
    "image/x-ms-bmp": "bmp",
    "image/webp": "webp",
    "image/svg+xml": "svg",
    "image/vnd.adobe.photoshop": "psd",
    "image/x-photoshop": "psd",
    "application/x-photoshop": "psd",
    "video/webm": "webm",
    "video/ogg": "ogg",
    "video/mp4": "mp4",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/webm": "webm",
    "audio/ogg": "ogg",
    "audio/mpeg": "mp3",
    "application/zip": "zip",
    "application/x-zip": "zip",
    "application/x-zip-compressed": "zip",
    "application/rar": "rar",
    "application/x-rar": "rar",
    "application/x-rar-compressed": "rar",
    "application/x-7z-compressed": "7z",
    "application/ogg": "ogg",
    "application/octet-stream": "bin",
}


def check_stop_words_in_urls(url):
    print("Checking url for stop words...")
    print("URL: " + str(url))
    if (url == None):
        return False
    if (len(url) < MIN_URL_SIZE):
        return False
    if (len(url) > MAX_URL_SIZE):
        return False
    for stop_url_keyword in stop_urls:
        try:
            stop_url_keyword = stop_url_keyword.replace("\n", "")
            #print("Checking: " + str(stop_url_keyword))
            if (len(stop_url_keyword) > 1):
                if (url.find(str(stop_url_keyword)) >= 0):
                    print("URL STOP KEYWORD FOUND: " + str(stop_url_keyword))
                    return False
        except Exception as e:
            return False
    return True


def verify_url_basic_check(url):
    if (url == None):
        return False
    if (len(url) < MIN_URL_SIZE):
        return False
    if (len(url) > MAX_URL_SIZE):
        return False
    else:
        return True


def x_print(data):
    # consol, log file and interface
    if DEBUG_CONSOLE == "ON":
        print(data)
    if DEBUG_LOG == "ON":
        debug_info(data)


def debug_info(info):
    # print to screen
    from datetime import datetime
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = open("debug", "a")
    f.write("\n" + str(time))
    f.write(str(info))
    f.close()


def is_valid_img_url(url):
    if (url == None):
        return False
    if (len(url) < MIN_URL_SIZE):
        return False
    if (len(url) > MAX_URL_SIZE):
        return False
    return check_media(url)


def first_dump(current_query):    
    global current_logo

    html_code = '<!DOCTYPE html><html lang="en"><head><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous"></head><body><center><h1>Image-Hunter</h1></center><center><h4>Playing around for educational purposes<br>with AI, NLP, Searching algorithms and Images</h4></center><CENTER><br>CURRENT QUERY IS:<br> ' + current_query + '<br></CENTER><CENTER><img src="'+ current_logo + '" style="display:inline-block;width:20%;height:20%;object-fit:contain;" border="1"><p>The page will refresh when results are ready.</p></CENTER><CENTER><p>Or follow this <a href="../interface/">link </a><p><a href="image-hunter-img-view.html">Image view</a>, <a href="image-hunter.html">View details</a>, <a href="image-hunter-every-image-view.html">View every image</a> or <a href="image-hunter-search.html">Search Results</p></form></center></body></html>'
    f = open("./dev/image-hunter.html", "w")
    f.write(str(html_code))
    f.close()
    
    html_code = '<!DOCTYPE html><html lang="en"><head><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous"></head><body><center><h1>Image-Hunter</h1></center><center><h4>Playing around for educational purposes<br>with AI, NLP, Searching algorithms and Images</h4></center><CENTER><br>CURRENT QUERY IS:<br> ' + current_query + '<br></CENTER><CENTER><img src="'+ current_logo + '" style="display:inline-block;width:20%;height:20%;object-fit:contain;" border="1"><p>The page will refresh when results are ready.</p></CENTER><CENTER><p>Or follow this <a href="../interface/">link </a><p><a href="image-hunter-img-view.html">Image view</a>, <a href="image-hunter.html">View details</a>, <a href="image-hunter-every-image-view.html">View every image</a> or <a href="image-hunter-search.html">Search Results</p></form></center></body></html>'
    f = open("./dev/image-hunter-search.html", "w")
    f.write(str(html_code))
    f.close()

    html_code = '<!DOCTYPE html><html lang="en"><head><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous"></head><body><center><h1>Image-Hunter</h1></center><center><h4>Playing around for educational purposes<br>with AI, NLP, Searching algorithms and Images</h4></center><CENTER><br>CURRENT QUERY IS:<br> ' + current_query + '<br></CENTER><CENTER><img src="'+ current_logo + '" style="display:inline-block;width:20%;height:20%;object-fit:contain;" border="1"><p>The page will refresh when results are ready.</p></CENTER><CENTER><p>Or follow this <a href="../interface/">link </a><p><a href="image-hunter-img-view.html">Image view</a>, <a href="image-hunter.html">View details</a>, <a href="image-hunter-every-image-view.html">View every image</a> or <a href="image-hunter-search.html">Search Results</p></form></center></body></html>'
    f = open("./dev/image-hunter-img-view.html", "w")
    f.write(str(html_code))
    f.close()

    html_code = '<!DOCTYPE html><html lang="en"><head><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous"></head><body><center><h1>Image-Hunter</h1></center><center><h4>Playing around for educational purposes<br>with AI, NLP, Searching algorithms and Images</h4></center><CENTER><br>CURRENT QUERY IS:<br> ' + current_query + '<br></CENTER><CENTER><img src="'+ current_logo + '" style="display:inline-block;width:20%;height:20%;object-fit:contain;" border="1"><p>The page will refresh when results are ready.</p></CENTER><CENTER><p>Or follow this <a href="../interface/">link </a><p><a href="image-hunter-img-view.html">Image view</a>, <a href="image-hunter.html">View details</a>, <a href="image-hunter-every-image-view.html">View every image</a> or <a href="image-hunter-search.html">Search Results</p></form></center></body></html>'
    f = open("./dev/image-hunter-every-image-view.html", "w")
    f.write(str(html_code))
    f.close()

    
    f = open("./dev/image-hunter-feed-" + html_file_name + ".html", "w")
    f.write(str(""))
    f.close()

    init_web()

html_blog_views = []
html_every_views = []

def dump_html(img, img_src):
    
    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_keywords
    global current_img_size
    global current_query
    global current_query_preview
    global current_root_url
    global html_file_name
    global html_img_counter
    global current_patterns_hits

    query_foler = current_query.replace(" ", "-")

    if HTML_IMAGE_PER_PAGE < html_img_counter:
        first_dump(current_query)
        html_img_counter = 0
        html_file_name = str(uuid.uuid4())
        current_query = query_history[0]
        query_foler = current_query.replace(" ", "-")
        refresh_web()
    
    html_img_counter = html_img_counter + 1
    process_html_dump(img_src, current_url)

    global current_image_alt_text_test
    hit = False

    if (current_image_alt_text_test == True) and (MIN_QUALITY_IMAGE_SIZE < current_img_size):
        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-BEST-IMG-SIZE-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (current_image_alt_text_test == True):
        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (MIN_QUALITY_IMAGE_SIZE < current_img_size):
        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BIG-SIZE-"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if current_quality_score > IMG_ALT_QS and MIN_QUALITY_IMAGE_SIZE < current_img_size:
        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BIG-SIZE-TEXT-ALT-MATCH-QS-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if current_quality_score > IMG_ALT_QS:
        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-QS"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if current_quality_score > IMG_ALT_QS and current_image_alt_text_test == True and MIN_QUALITY_IMAGE_SIZE < current_img_size:
        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/SIZE-TEXT-ALT-MATCH-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()
        hit = True

    if (hit == True):

        html = '<a href="' + img_src + '"><img  border="1" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BEST-RESULTS-" + query_foler +
                 "-" + html_file_name + ".html", "a")
        f.write(str(html))
        f.close()

    import random
    x = random.randint(1,8)
    if x == 4:
        if img.find(".jpg") >= 0:
            global current_logo
            current_logo = img
            refresh_web()
           
    import datetime
    current_date = datetime.date.today()
    
    view = '<div class="card flex-md-row mb-4 box-shadow h-md-250"><div class="card-body d-flex flex-column align-items-start"><strong class="d-inline-block mb-1 text-success">'+current_query+'</strong><br><img class="card-img-right flex-auto d-none d-md-block" alt="'+current_preview+'" style="max-width:350px;max-width:auto;height:auto;object-fit:contain;" src="'+img_src+'" data-holder-rendered="true"><h3 class="mb-0"><a class="text-dark" href="'+current_root_url+'">'+current_title+'</a></h3><br><a href="'+current_root_url+'">'+current_root_url+'</a><div>[...] '+current_preview+' [...]</div>' + current_img_keywords.upper() + '<div class="mb-1 text-muted">'+str(current_date)+'</div><p class="card-text mb-auto"></p><a href="'+current_root_url+'">Continuer la lecture</a></div></div>'
    view_every_img = '<a href="'+current_root_url+'"><img class="card-img-right flex-auto d-none d-md-block" alt="'+current_preview+'" style="max-width:300px;width:auto;height:auto;object-fit:contain;" src="'+img_src+'" data-holder-rendered="true"></a>'

    global old_mem
    if (old_mem != current_root_url):
        html_blog_views.append(view)
        html_every_views.append(view_every_img)
        generate_blog_view(html_blog_views)
        generate_everything_view(html_every_views)
        dynamic_interface_dump()

    old_mem = current_root_url

    if HTML_IMAGE_PER_PAGE < html_img_counter:
        dynamic_interface_first_dump(current_query)
        html_img_counter=0
        # html_views.clear()
    else:
        dynamic_img_dump()

flag = True
def dynamic_interface_first_dump(current_query):
    first_dump(current_query)

def dynamic_interface_dump():
    global flag
    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_size
    global current_query
    global current_root_url
    global html_file_name
    global html_img_counter
    global current_patterns_hits

    html_code = '</center><br><center><a href="' + current_img_src + '" ><img border="1" src="' + current_img_src + '" style="align:center;display:inline-block;width:100px;height:60px;object-fit:contain;" /></a></center><center>'
    f = open("./dev/image-hunter-img-view.html", "a")
    f.write(str(html_code))
    f.close()

    html_code = '</center><br><center><a href="' + current_root_url + '" ><img border="1" src="' + current_img_src + \
        '" style="display:inline-block;width:390px;height:290px;object-fit:contain;" /></a></center>'
    html_code = html_code + '<center><b>TITLE: ' + current_title.capitalize() + '</b></center>'
    html_code = html_code + '<center><b>PREVIEW: ' + current_preview.capitalize() + '</b></center>'
    html_code = html_code + '<center><a href="' + current_root_url + '">' + current_root_url + '</a></center>'
    html_code = html_code + '<center><b>IMAGE KEYWORDS:</b>' + current_img_keywords.upper() + " [...] " + '</center><center>'
    f = open("./dev/image-hunter.html", "a")
    f.write(str(html_code))
    f.close()

    html_code = '</center><br><center><a href="' + current_root_url + '" style="center"><img border="3" src="' + current_img_src + \
            '" style="display:inline-block;width:290px;height:200px;object-fit:contain;" /></a></center><center>'
    html_code = html_code + '<center><b>TITLE: ' + current_title.capitalize() + \
        '</b></center><center><a href="' + current_root_url + \
        '">' + current_root_url + '</a></center>'
    f = open("./dev/image-hunter-search.html", "a")
    f.write(str(html_code))
    f.close()


def dynamic_img_dump():
    global flag
    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_size
    global current_query
    global current_root_url
    global html_file_name
    global html_img_counter
    global current_patterns_hits

    html_code = '<a  align="center" href="' + current_img_src + '" ><img  align="center" border="1" src="' + current_img_src + '" style="align:center;display:inline-block;width:100px;height:60px;object-fit:contain;" /></a>'
    f = open("./dev/image-hunter-img-view.html", "a")
    f.write(str(html_code))
    f.close()

    html_code = '<a  align="center" href="' + current_root_url + '" ><img border="1"  align="center" src="' + current_img_src + \
        '" style="display:inline-block;width:100px;height:60px;object-fit:contain;" /></a>'
    f = open("./dev/image-hunter.html", "a")
    f.write(str(html_code))
    f.close()

    html_code = '<a href="' + current_root_url + '" align="center"><img border="3"  align="center" src="' + current_img_src + \
            '" style="align:center;display:inline-block;width:100px;height:60px;object-fit:contain;" /></a>'
    f = open("./dev/image-hunter-search.html", "a")
    f.write(str(html_code))
    f.close()


def process_html_dump(img_src, url):

    global current_title
    global current_url
    global current_root_url
    global current_query
    global current_text
    global current_img_src
    global current_img_keywords
    global current_patterns_hits
    global current_quality_score

    if (current_title == None):
        current_title = "Website has no title"
    
    # GLOBAL THUMBNAIL VIEW
    html = '<br><center><a href="' + img_src + '"><img border="1" src="' + img_src + \
        '" style="display:inline-block;width:400px;height:320px;object-fit:contain;" /></a></center>'
 
    f = open("./interface/global-view-" + html_file_name+".html", "a")
    f.write(str(html))
    f.close()

    f = open("./dev/image-hunter-every-image-view.html", "a")
    f.write(str(html))
    f.close()

    html = '<br><center><a href="' + current_root_url + '"><img border="1" src="' + img_src + \
        '" style="display:inline-block;width:490px;height:380px;object-fit:contain;" /></a></center>'
    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + \
        current_root_url + '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + current_img_keywords.capitalize() + " [...] " + '</center><center><b>PREVIEW:</b>' + current_preview.capitalize() + " [...] " + '</center><center><a href="' + \
        img_src + '">' + img_src + '</a></center><br>QUALITY SCORE: ' + str(current_quality_score) + '<br>QUERY: ' + str(
            current_query) + ' <br>IMAGE Keywords: ' + str(current_img_keywords) + ' <br>PATTERNS: ' + str(current_patterns_hits) + '<div><hr>'
    f = open("./interface/main-" + html_file_name + ".html", "a")
    f.write(str(html_code))
    f.close()

file = str(uuid.uuid4())

def dump_url_html(url):
    global file
    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_keywords
    global html_file_name
    global html_img_counter
    global current_patterns_hits
    global current_quality_score

    html = '<br><center><center><b>' + current_title.capitalize() + ' QS SCORE: ' + \
        str(current_quality_score) + ' </b></center>'
    html_code = html + '<center><a href="' + \
        str(url) + '">' + url + '</a></center><br>'
    #html_code = html + '<center> ' + current_text + '</center>'
    f = open("./interface/URLS-" + file + ".html", "a")
    f.write(str(html_code))
    f.close()

old_mem = []
def generate_blog_view(html_views):
    html_views_code=""
    for view in html_views:
        html_views_code = html_views_code + str(view)

    start_html = '<!doctypehtml><html><head><metacharset="utf-8"><metaname="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no"><metaname="description" content=""><metaname="author" content=""><title>Image-Hunter</title><!--CSSonly--></head><body><center>'
    end_html = '</center></body></html>'
    html = start_html + html_views_code + end_html 
    f = open("./dev/image-hunter-feed-" + html_file_name + ".html", "w")
    f.write(str(html))
    f.close()


def generate_everything_view(html_views):
    html_views_code=""
    for view in html_views:
        html_views_code = html_views_code + str(view)

    start_html = '<!doctypehtml><html><head></head><body><center>'
    end_html = '</center></body></html>'
    html = start_html + html_views_code + end_html 
    f = open("./dev/image-hunter-every-image-view.html", "a")
    f.write(str(html))
    f.close()

def trim(text_section):
    if text_section == None:
        return None
    #text_section = clean_word(text_section)
    text_section = text_section.strip()
    return text_section


def trim_url(url):
    if url == None:
        return None
    if not url.find("http") >= 0:
        return None

    url = url.lstrip()
    url = url.rstrip()
    url = url.strip()
    return url


def prepare_keywords_for_database(title):
    if (title == None):
        return False
    if (len(title) < MIN_WORD_SIZE):
        return False

    keywords = ""
    keywords = title.lower()
    keywords = clean_text(keywords)

    for ix in stop_words:
        for iy in keywords.split(" "):
            if ix == iy:
                keywords = keywords.replace(ix, " ")
    return keywords


def clean_up_buffer(urls):
    clean = []
    for url in urls:
        if verify_url_basic_check(url):
            if check_stop_words_in_urls(url):
                if url == None:
                    continue
                if not url in clean:
                    try:
                        url = trim_url(url)
                        url = url.replace("\n", "")
                        clean.append(url)
                    except:
                        pass
    return clean


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title != None:
        title = soup.title.get_text()
        return title
    return None


def format_for_pattern_check(url, title, text):
    if (title==None) or (text==None):
        return None
    global current_quality_score
    url = format_url(url)

    if (title == None):
        title = ""

    if (text == None):
        text = ""
    
    return url, title, text

def get_html_textual_content(html):
    text_in_html = ""
    try:
        text_in_html = get_text(html)
    except:
        pass
    return text_in_html


def shuffle_list(list):
    import random

    # Random URL search path
    # We may hit the jackpot
    random.shuffle(list)


def url_verification(url):
    x_print("STARTING URL VERIFICATION")
    if url == None:
        return False
    if not url.find("http") >= 0:
        return False
    if not url.find("://") >= 0:
        return False
    print("url: "+str(url))

    if url.find("captcha" or "unusual traffic") >= 0:
        block_url(url)
        return False
    result = check_url(url)
    if (not result):
        return False

    result = verify_url_basic_check(url)

    if (result == True):
        result = check_stop_words_in_urls(url)
    else:
        x_print("URL VERIFICATION FAILED - IN BASIC CHECK")
        x_print("URL: " + str(url))
        pass
    return result

def url__img_verification(url):
    x_print("STARTING URL IMAGE VERIFICATION")
    result = check_url_img(url)
    if (not result):
        return False

    result = verify_url_basic_check(url)

    if (result == True):
        result = check_stop_words_in_urls(url)
    else:
        x_print("URL VERIFICATION FAILED - IN BASIC CHECK")
        x_print("URL: " + str(url))
        pass
    return result

def insert_url_db_sub(i):
    global urls_global_session_memory
    if i not in urls_global_session_memory:
        insert_url(i)
        relax(TIME_LOCK)
        urls_global_session_memory.append(i)

def close_loop():
    global save_count
    global url_count
    global img_count
    global urls_buffer
    global current_query
    global query_history
    global stop_urls
    global dictionary
    
    print("SAVE COUNTER IS AT " + str(save_count))
    print("IMAGES " + str(img_count))
    print("URLS SPIDERED " + str(url_count))
    print("URLS TO SPIDERED " + str(len(urls_buffer)))
    
    relax(TIME_LOCK)

    if (SAVE_CYCLE < save_count):
        print("SAVE COUNTER IS AT THE LIMIT")
        print("CLEANING BUFFERS")

        urls_buffer = clean_up_buffer(urls_buffer)
        urls_buffer = check_search_urls(urls_buffer)

        if (len(urls_buffer) > URL_LIMIT_CLEANING):
            urls_buffer = check_critical_amount_of_urls(urls_buffer)

        print("SAVE URLS")

        save_memory()
        save_media()

        save_count = 0

        x_print("SAVING DATA")
        
        stop_urls = save_list(stop_urls, "./intelligence/stop_urls")
        query_history = save_list(
            query_history, "./intelligence/query_history")

def first_check(url):
    global urls_buffer
    global current_url
    global save_count
    global spidered_site_count
    global approch_counter

    current_url = url  # = format_url(url)
    save_count = save_count + 1
    result = url_verification(url)

    if (result == False):
        x_print("\nURL VERIFICATION FAILED - STOP WORD in URL")
        x_print("URL: " + str(url))
        x_print("FIRST CHECK FAILED...")
        # relax(TIME_LOCK)
        return result

    x_print("\nFIRST URL VERIFICATION PASSED...")

    #result = verify_keywords_in_link(url)

    if (result):
        x_print("FIRST CHECK SUCCESS...\n")
    else:    
        x_print("SECOND URL VERIFICATION FAILED...")
        x_print("FIRST CHECK FAILED...\n")
        
    # relax(TIME_LOCK)
        
    if (RANDOM_START > approch_counter):
        approch_counter = 0
        x_print("Random approche pattern...")
        shuffle_list(urls_buffer)

    approch_counter = approch_counter + 1

    return result

def read_evaluate_learn(url, html):

    global current_url
    global current_title
    global current_text
    global current_preview
    global url_count
    global img_count

    x_print("\n\nENTERING READ AND EVALUATE...\n\n")
    
    x_print("URL count : " + str(url_count))
    x_print("Image count :" + str(img_count))
    x_print("Current URL :" + str(url))

    result = True
    title, preview, text = format_text(url, html)

    try :
        result = verify_content(url, title, text)
    except:
        pass

    if (DOWNLOAD_EVERYTHING == 'ON'):
        x_print("DOWNLOAD_EVERYTHING is activated")
        x_print("the scraper will download every image")
        result = True

    if (result):
        current_url = url
        current_title = title
        current_text = text
        current_preview = preview

    if (DOWNLOAD_HTML == "ON"):
        x_print("downloading html to disk")
        download_website_html_page(html)

    return result

def format_text(url, html):
    
    title = get_title(html)

    global current_title
    current_title = title

    text = get_html_textual_content(html)

    preview = prepare_preview(text)
    
    url, title, text = format_for_pattern_check(url, title, text)

    return title, preview, text

def spider(url, html):

    global urls_buffer
    global urls_visited
    global urls_images

    print_loop_info(url)

    urls_buffer = extract_urls(url, html)
    urls_images = extract_images(url, html)

    if (url in urls_buffer):
        urls_buffer.remove(url)

    if (not url in urls_buffer):
        urls_visited.append(url)

    return True


i_proxy = 0


def get_web_page(url):
    global url_count, i_proxy, proxies_list, proxy_good
    if not proxy_good:
        page = find_a_working_proxy(url, proxies_list)
        if (page == None):
            global urls_problems
            urls_problems.append(url)
            return page
    try:
        if page.status_code == 200:
            proxy_good = True
            url_count = url_count + 1
            if (url in urls_buffer):
                urls_buffer.remove(url)
    except:
        pass

    return page


i_proxy = 0

def open_url_proxy(url, id_proxy):
    global proxies_list  # https://openproxy.space/list
    global proxies

    proxies = {
        'http': proxies_list[id_proxy],
        'https': proxies_list[id_proxy],
    }

    try:
        page = requests.get(str(url), timeout=10)
        if page.status_code == 200:
            global proxy_good, i_proxy
            i_proxy = id_proxy
            proxy_good = True
            return page
        return None
    except:
        return None

def open_url_no_proxy(url):
    try:
        page = requests.get(str(url), timeout=10)
        if page.status_code == 200:
            return page
        else:
            return None
    except:
        return None

def open_url_with_proxy(url):
    global proxies_list  # https://openproxy.space/list
    global proxies
    global proxy_good, i_proxy

    try:
        page = requests.get(str(url), timeout=30)
        proxies = proxies
        proxy_good = True
        return page
    except:
        i_proxy = i_proxy + 1
        proxy_good = False
        open_url_proxy(url, i_proxy)
        pass

    return None

def find_a_working_proxy(url, proxies_list):
    global i_proxy

    index = 0
    error = 0
    proxy = ""
    MAX_NB_RETRIES = 10

    for i in proxies_list:
        print("Trying to connect to proxy...")
        print("PROXY: " + str(proxies))
        page = open_url_proxy(url, index)
        error = error + 1

        if error > MAX_NB_RETRIES:
            return None

        print("Searching for a working proxy...")
        if page == None:
            proxies_list.remove(i)
            index = index + 1
            continue
        else:
            i_proxy = index
            proxies_list = save_list(proxies_list, "./tools/proxies")
            print("Found proxy : " + str(proxy))
            global proxy_good
            proxy_good = True
            return page


def print_loop_info(url):
    # Connect memory buffers
    global save_count
    global img_count
    global url_count
    global urls_buffer
    global current_root_url
    global current_query
    global current_quality_score
    global current_frequency_score

    print("STARTING A NEW LOOP")
    print("URL: " + str(url))
    print("NUMBER OF URLS LEFT TO MINE: " + str(len(urls_buffer)))
    print("Url count: " + str(url_count))
    print("BASE URL: " + str(current_root_url))
    print("Query: " + str(current_query))
    print("Save count: " + str(save_count))              
    print("Image count: " + str(img_count))
    print("Url count: " + str(url_count))
    print("QS: " + str(current_quality_score))
    print("FS: " + str(current_frequency_score))
    print("URLS LEFT: " + str(len(urls_buffer)))

def start_image_miner():

    # Connect memory buffers
    global save_count
    global img_count
    global url_count
    global urls_buffer
    global urls_images
    global urls_visited
    global dictionary
    global learned_relations
    global learned_keywords
    global query_history
    global search_boost
    global match_boost
    global user_profil
    global current_query
    global current_url
    global current_title
    global current_text
    global current_html
    global current_query
    global current_root_url
    global proxy_good
    global proxies_list
    global spam_filter
    global code_filter

    print("Load memory")
    load_memory()

    print("Cleaning buffers")
    # Pro-active clean up process
    urls_buffer = clean_up_buffer(urls_buffer)
    
    global file_name_keywords
    file_name_keywords = str(query_history[0]).replace(
        " ", "-") + "-keywords-" + str(uuid.uuid4())

    # loading intelligence
    dictionary = load_list("./intelligence/dictionary", dictionary)

    learned_keywords = load_list(
        "./intelligence/learned_keywords", learned_keywords)

    query_history = load_list("./intelligence/query_history", query_history)
    #user_profil = load_list("./intelligence/user_profil", user_profil)
    proxies_list = load_list("./tools/proxies", proxies_list)
    spam_filter = load_list("./intelligence/spam_filter", spam_filter)
    code_filter = load_list("./intelligence/code_filter", code_filter)

    search_boost = load_list("./intelligence/search_boost", search_boost)
    match_boost = load_list("./intelligence/match_boost", match_boost)
    
    x_print("Starting image mining process...\n")
    x_print("Loading the memory...\n")

    #import random
    #random.shuffle(urls_buffer)
    for url in urls_buffer:
        
        x_print("Starting LOOP...\n")
        x_print("URL is:\n")
        x_print(str(url))
        
        new_turn()

        current_root_url = url
        current_url = url
        url_count = url_count + 1

        # Todo VERIFICATION in history 
        # and other ressource de quality of the site 
        x_print("COULD MAKE A VERIFICATION BEFORE VISITING THE SITE")
        result = first_check(url)

        if (result):
            try:
                x_print("DOWNLOADING URL: " + url)
                page = get_request_url(url)

                if page == None:
                    continue

                if page.status_code == 200:
                    result = read_evaluate_learn(url, page.text)
                
                if result == False:
                    close_loop()
                    continue
            except Exception as e:
                x_print(e)
                close_loop()
                continue

            try:
                if SPIDER_ALL_IMAGES == 'ON' or current_quality_score > QUALITY_SCORE:
                    result = spider(url, page.text)
        
                if (RANDOM_START < approch_counter):
                    x_print("Random approche pattern...")
                    shuffle_list(urls_buffer)

                close_loop()
            except Exception as e:
                x_print(e)
                print("ERROR - in spider extraction process")
                close_loop()
                continue

    start_image_miner()


def get_request_url(url):
    if PROXY_ACTIVATED == 'ON':
        if not proxy_good:
            page = get_web_page(url)
            return page
        else:
            page = open_url_with_proxy(url)
            return page
    else:
        page = open_url_no_proxy(url)
        return page


def learn_keywords(keywords):

    if (keywords == None):
        return None
    x_print("Learning")
    x_print("KEYWORDS: " + str(keywords))
    if (keywords != "" and keywords != None):
        clean = []
        final_keywords = ""
        for word in keywords.split(" "):
            if word == None:
                continue
            if not word in clean:
                final_keywords = final_keywords + " " + word

        if not final_keywords in learned_keywords:
            final_keywords = search_engine_filter(final_keywords)
            learned_keywords.append(final_keywords)
            # Save and reload
            save_list(learned_keywords, "./intelligence/learned_keywords")
    return final_keywords

def new_turn():

    print("STARTING NEW TURN...")

    global spidered_site_count
    spidered_site_count = spidered_site_count + 1

    if (spidered_site_count > NB_OF_SITE_TO_SPIDER):
        spidered_site_count = 0
        import random
        x = random.randint(0, len(query_history)-1)

        urls_buffer.clear()
        urls_visited.clear()
        urls_images.clear()
        main(query_history[x])


import nltk
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')    

def nlp_freq(text):
    tokens = [t for t in text.split()]
    clean_tokens = tokens[:]
    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
        elif token in stopwords.words('french'):
            clean_tokens.remove(token)
        elif token in stopwords.words('spanish'):
            clean_tokens.remove(token)
        else:
            if len(token) <= MIN_WORD_SIZE or len(token) >= MAX_WORD_SIZE:
                clean_tokens.remove(token)

    freq = nltk.FreqDist(clean_tokens)
    print(freq)

    freq_score = 0

    for key, val in freq.items():
        if val >= FREQUENCY_MIN_WORDS:
            if len(key) >= MIN_WORD_SIZE:
                if len(key) <= MAX_WORD_SIZE:

                    print("Key:" + str(key) + ':' + "Value:" +  str(val))
                    
                    from nltk.stem import PorterStemmer
                    stemmer = PorterStemmer()
                    stem = stemmer.stem(str(key)) 

                    if (current_query.find(stem)>=0):
                        global current_quality_score
                        freq_score = freq_score + (1 * int(val))

    # freq.plot(20, cumulative=False)
    return freq_score, freq


def nlp_freq_special(text, fst):
    #stopwords.words('english')
    tokens = [t for t in text.split()]
    clean_tokens = tokens[:]
    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
        elif token in stopwords.words('french'):
            clean_tokens.remove(token)
        elif token in stopwords.words('spanish'):
            clean_tokens.remove(token)
        else:
            if len(token) <= MIN_WORD_SIZE or len(token) >= MAX_WORD_SIZE:
                clean_tokens.remove(token)

    freq = nltk.FreqDist(clean_tokens)
    print(freq)
    concepts = []
    freq_score = 0

    for key, val in freq.items():
        if val >= FREQUENCY_MIN_WORDS:
            if len(key) >= MIN_WORD_SIZE:
                if len(key) <= MAX_WORD_SIZE:

                    print("Key:" + str(key) + ':' + "Value:" +  str(val))
                    
                    if val >= int(fst):
                        concepts.append(key)

                    from nltk.stem import PorterStemmer
                    stemmer = PorterStemmer()
                    stem = stemmer.stem(str(key)) 

                    if (current_query.find(stem)>=0):
                        freq_score = freq_score + (1 * int(val))

    # freq.plot(20, cumulative=False)
    return freq_score, freq, concepts

def nlp_freq_special_group(clean_tokens, threashold):
    freq = nltk.FreqDist(clean_tokens)
    print(freq)
    concepts = []
    freq_score = 0

    for key, val in freq.items():
        if val >= FREQUENCY_MIN_WORDS:
            if len(key) >= MIN_WORD_SIZE:
                if len(key) <= MAX_WORD_SIZE:
                    if threashold <= val:
                        print("Key:" + str(key) + ':' + "Value:" +  str(val))
                        concepts.append(key)
                        learned_relations.append(key)

    # freq.plot(20, cumulative=False)
    return freq_score, freq, concepts

def search_engine_filter(final):
    if "google" or "bing" or "yahoo" in final:
        final = final.replace("google", " ")
        final = final.replace("bing", " ")
        final = final.replace("yahoo", " ")
    return final


def requests_urllib(url):

    req = urllib.request.Request(url)

    conn = urllib.request.urlopen(req, timeout=10)
    status = conn.getcode()
    contentType = conn.info().get_content_type()

    return conn, status, contentType


def main(query):

    if (query==None):
        query = input("Please enter a query: ")

    global current_query
    current_query = query

    x_print("INITIATION OF THE SPIDER/SCRAPER")
    init_program(query)
    
    x_print("START MINER")
    start_image_miner()

def start_html():
    return '<html>'

def end_html():
    return '</html>'

def print_html(text):
    text = str(text)
    text = text.replace('\n', '<br>')
    return '<p>' + str(text) + '</p>'

def start():

    query = ""
    main(query)

start()
