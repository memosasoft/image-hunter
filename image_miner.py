# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from selenium import webdriver as driver
import configparser
import mimetypes  # needed for download functionality
import os
import shutil  # to save it locally
import sys
import time
# Importing Necessary Modules
import urllib.request
import uuid
import webbrowser
from distutils.command.config import dump_file
from random import random
from re import I
from sqlite3 import Error

import requests  # to get image from the web
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search
from nturl2path import url2pathname

# Session url and img global_memory
urls_global_session_memory = []
images_seesion_memory = []

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
current_img_size = 0
current_description = ""
current_image_alt_text_test = ""

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
quality_score = 0

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
# adding specific keywords under de hood
# to get better searching and matching
search_boost = [
    "photo,image,picture,gallery,wallpaper,art,digital,svg,jpg,jpeg"]
match_boost = [
    "photo,image,picture,gallery,pic,art,digital,svg,jpg,jpeg,web,ogg,gif,png,bmp"]

match_query = ""
pattern_memory = []

# keywords container for query
query_history = []

# Learning component
dictionary = []
synonyms = []
learned_relations = []
spam_filter = []

# Learning array for text the system reads
learned_keywords = []

# Fake user agent
ua = UserAgent()
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

NB_OF_SITE_TO_SPIDER = int(configuration.get('CONFIG', 'NB_OF_SITE_TO_SPIDER'))
IMG_ALT_VERIFICATION = str(configuration.get('CONFIG', 'IMG_ALT_VERIFICATION'))
IMG_ALT_QS = int(configuration.get('CONFIG', 'IMG_ALT_QS'))
STEP_SCAN = int(configuration.get('CONFIG', 'STEP_SCAN'))

LEARNING_TFQST = int(configuration.get('CONFIG', 'LEARNING_TFQST'))
LEARN_TO_BLOCK_URL = int(configuration.get('CONFIG', 'LEARN_TO_BLOCK_URL'))
DOWNLOAD_EVERYTHIING = str(configuration.get('CONFIG', 'DOWNLOAD_EVERYTHIING'))
DEEP_ANALYSIS = str(configuration.get('CONFIG', 'DEEP_ANALYSIS'))
ANALYSIS_MAX_WORDS = int(configuration.get('CONFIG', 'ANALYSIS_MAX_WORDS'))
SPIDER_ALL_IMAGES = str(configuration.get('CONFIG', 'SPIDER_ALL_IMAGES'))

SEARCH_BOOST = str(configuration.get('CONFIG', 'SEARCH_BOOST'))
MATCH_BOOST = str(configuration.get('CONFIG', 'SEARCH_BOOST'))
QUERY_BOOST = str(configuration.get('CONFIG', 'QUERY_BOOST'))

PREVIEW_SIZE = int(configuration.get('CONFIG', 'PREVIEW_SIZE'))
DOWNLOAD_HTML = str(configuration.get('CONFIG', 'DOWNLOAD_HTML'))
HTML_IMAGE_PER_PAGE = int(configuration.get('CONFIG', 'HTML_IMAGE_PER_PAGE'))
SAVE_CYCLE = int(configuration.get('CONFIG', 'SAVE_CYCLE'))
MIN_IMAGE_SIZE = int(configuration.get('CONFIG', 'MIN_IMAGE_SIZE'))
MAX_FILE_NAME_SIZE = int(configuration.get('CONFIG', 'MAX_FILE_NAME_SIZE'))
DEBUG_CONSOLE = str(configuration.get('CONFIG', 'DEBUG_CONSOLE'))
DEBUG_LOG = str(configuration.get('CONFIG', 'DEBUG_LOG'))
FREELY_GRAB_URLS = str(configuration.get('CONFIG', 'FREELY_GRAB_URLS'))
MAX_WORKSPACE_SIZE = int(configuration.get('CONFIG', 'MAX_WORKSPACE_SIZE'))
MIN_QUALITY_IMAGE_SIZE = int(configuration.get(
    'CONFIG', 'MIN_QUALITY_IMAGE_SIZE'))
URL_LIMIT_AMOUNT = int(configuration.get('CONFIG', 'URL_LIMIT_AMOUNT'))
SAVE_SUBJECT_KEYWORDS = str(configuration.get(
    'CONFIG', 'SAVE_SUBJECT_KEYWORDS'))

RANDOM_START = int(configuration.get('CONFIG', 'RANDOM_START'))
DIG_FOR_URLS = str(configuration.get('CONFIG', 'DIG_FOR_URLS'))
PROGRAM_PATH = str(configuration.get('CONFIG', 'PROGRAM_PATH'))
PROXY_ACTIVATED = 'OFF'


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
    # x_print("SETUP PROCESS")
    # x_print("Starting setup process and cleanup")
    setup_process(user_input)

    if (query == ""):
        query = input("What type of images you want to spider?")

    query_size = str(len(query.split(" ")))

    # THIS IS A PERSONAL CHOICE AND A TRICK TO GET
    # MORE IMAGES IN THE SEARCH ITS NOT COMPLICATED
    current_query = query
    query = process_boost(query)

    #answer = input("Is this modification ok?")

    answer = 'y'
    query_history = load_list("./intelligence/query_history", query_history)
    query_history.insert(0, query)
    query_history = save_list(query_history, "./intelligence/query_history")

    x_print("\nSEARCH MODULE\n")
    x_print("Connecting to Google, Yahoo and Bing")
    x_print("This may take a while")

    # add the user query to the user queries list
    # add also to the query_history list
    x_print("\nNEW SELF-LEARNING FEATURE - AI")
    x_print("\nLoading user query global_memory for system self-learning purposes")

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
        #input("Error saving archive")
        print("Error saving archive")
        pass

    try:
        save_to_archive("./media/", "./archives/media/" +
                        str(query_foler) + "/")
        save_to_archive("./interface/", "./archives/interface/")
    except Exception as e:
        print(e)
        #input("Error saving archive")
        print("Error saving archive")
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
    x_print()

    return info


def process_boost(query):

    global current_query
    global match_boost
    global search_boost

    if SEARCH_BOOST == "ON":
        query = query + " " + clean_text(search_boost[0])
        search_boost.append(query)
        search_boost = clean_text(search_boost[0])
        search_boost = save_list(search_boost, "./intelligence/search_boost")
        print("Just added search boost")

    if MATCH_BOOST == "ON":
        # CRITICAL ELEMENT FOR MATCHING
        global match_query
        match_boost_data = clean_text(match_boost[0])
        match_query = query + " " + match_boost_data
        match_boost.append(match_query)
        match_boost = save_list(match_boost, "./intelligence/match_boost")
        print("Just added match boost")

    #print("Cleaning query")
    query = clean_text(query)

    return query


def clean_query(query):

    items = ["  ", ",", ".",
             "-", "+", "{", "}", "[", "]"]

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

    # UNDER DEVELOPPEMENT
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
            #print("removing url: " + str(url))

    return list_of_urls


def check_search_urls(list_of_urls):

    for url in list_of_urls:
        result = first_check(url)

        if result == False:
            list_of_urls.remove(url)
            #print("removing url: " + str(url))

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

    urls_buffer = save_list(urls_buffer, "urls")
    return urls_buffer
    # save_memory()

# Self learning object to gain ai from
# user interaction - Prototype


def save_memory():
    global urls_buffer
    global urls_visited
    global urls_images

    global stop_urls
    global learned_relations
    global dictionary

    # shuffle_list(urls_buffer)
    x_print("Saving memory")
    urls_buffer = save_list(urls_buffer, "urls")
    x_print("Url memory saved")
    shuffle_list(urls_buffer)

    urls_visited = save_list(urls_visited, "urls_visited")
    x_print("Visited sites memory saved")

    urls_images = save_list(urls_images, "urls_images")
    x_print("Visited downloaded images memory saved")

    stop_urls = save_list(stop_urls, "./intelligence/stop_urls")
    dictionary = save_list(dictionary, "./intelligence/dictionary")
    learned_relations = save_list(
        learned_relations, "./intelligence/learned_relations")

    x_print("stop_urls saved")


def load_memory():

    global urls_buffer
    global urls_images

    global urls_visited
    global query_history
    global search_boost
    global dictionary
    global learned_relations
    global learned_keywords
    global stop_urls

    x_print("Loading memory")
    urls_buffer = load_list("urls", urls_buffer)
    x_print("Url memory loaded")

    urls_visited = load_list("urls_visited", urls_visited)
    x_print("Visited sites memory loaded")

    urls_images = load_list("urls_images", urls_images)
    x_print("Downloaded images memory loaded")

    stop_urls = load_list("./intelligence/stop_urls", stop_urls)
    dictionary = load_list("./intelligence/dictionary", dictionary)
    learned_relations = load_list(
        "./intelligence/learned_relations", learned_relations)


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
        if len(key) > 2:
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
    if not title in learned_keywords:
        learned_keywords.append(title)

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
        download(url)
        return False
    if url.find(str(".xls")) >= 0:
        download(url)
        return False
    if url.find(str(".htm")) >= 0:
        return True
    if url.find(str(".zip")) >= 0:
        download(url)
        return False
    if url.find(str(".js")) >= 0:
        return False

    # Download intresting files
    if url.find(str(".mp3")) >= 0:
        download(url)
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
    if DOWNLOAD_EVERYTHIING == 'ON':
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
                except Error as e:
                    x_print(e)
                    try:
                        relax(TIME_LOCK)
                        import wget
                        wget.download(str(url), str(target))
                    except Error as e:
                        x_print(e)
                        print("Error with the requests...")
                        x_print("Download ERROR...\n")
                        return None

                # Set the image source
                current_img_src = url
                x_print("\nURL: " + str(url))
                x_print("Download completed\n")
                print("Image count: " + str(img_count))
                print("Url count: " + str(url_count))
                x_print("For security reasons pacing at \n" +
                        str(TIME_LOCK) + " secondes...")
                relax(TIME_LOCK)
            else:
                x_print("DOWNLOAD AI TESTS FAILED...\n")
                return None

        except Error as e:
            x_print(e)
            x_print("Error downloading")
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
        except Error as e:
            x_print(e)
            x_print("Error backup wget downloading")
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

    import requests as r
    r = get_img_request_url(url)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        # Open a local file with wb ( write binary ) permission.

        current_img_keywords = extract_keywords(url)
        filename = generate_img_file_name(r, url, current_img_keywords)

        with open("./media/" + filename, 'wb') as f:
            import os
            shutil.copyfileobj(r.raw, f)

        target = "./media/" + filename
    return target


def generate_img_file_name(r, url, current_img_keywords):

    ext_guess = url.split(".")[-1]
    file_guess = url.split("/")[-1]

    ext = get_extension(r)
    filename = str(uuid.uuid4())

    if (current_img_keywords != None) and (current_img_keywords != " ") and (current_img_keywords != "") and (len(current_img_keywords) > MIN_WORD_SIZE):
        print("Image keywords: " + current_img_keywords)
        reformated = current_img_keywords.replace(" ", "-")
        reformated = reformated.replace("_", "-")
        reformated = reformated.replace("+", "-")
        reformated = clean_file_name(reformated)

        if len(reformated) >= MIN_WORD_SIZE:
            if len(reformated) <= MAX_FILE_NAME_SIZE:
                filename = reformated + "-" + filename[0:4] + "." + ext
            else:
                filename = reformated[0:int(
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
            r = requests.get(url, stream=True, headers={
                'User-Agent': ua.random}, proxies=proxies, timeout=10)
            return r
        else:
            r = requests.get(url, stream=True, headers={
                'User-Agent': ua.random}, timeout=10)
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
        print("Error in get_size_img_check")


def clean_file_name(file_name):
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
    return file_name


def build_title_from_filename(url):
    ext = url.split(".")[-1]
    file = url.split("/")[-1]
    title = format_title(str(file), str(ext))
    return title


def image_size_check(img_file, img_src):

    if (img_file == None):
        return None
    if (img_src == None):
        return None

    if (img_file == 'None'):
        return None
    if (img_src == 'None'):
        return None

    import os
    import shutil

    global images_seesion_memory
    global current_image_alt_text_test

    file_size = os.path.getsize(img_file)
    file_name = img_file

    print("Image Name: " + str(file_name))
    print("Image size: " + str(file_size))
    global current_img_size
    current_img_size = file_size
    try:
        if (file_size > MAX_WORKSPACE_SIZE):
            if not img_file in images_seesion_memory:
                shutil.copy2(str(img_file), './archives/workspace/')
                images_seesion_memory.append(img_file)

                file = img_file.split("/")[-1]
                file = clean_filename(file)
                file_name = './archives/workspace/' + file
                print("Image is very large should be verified by the user")
                print("Path: " + file_name)

        if (file_size < MIN_IMAGE_SIZE):
            if not img_file in images_seesion_memory:
                shutil.copy2(str(img_file), './archives/workspace/')
                images_seesion_memory.append(img_file)

                file = img_file.split("/")[-1]
                file = clean_filename(file)
                file_name = './archives/workspace/' + file
                print("Image is very small it is an Icon")
                print("Path: " + file_name)

        global current_url
        print("Image is perfect")
        print("Path: " + file_name)

        dump_html(str(file_name), str(img_src))
    except Exception as e:
        print(e)
        global current_url
        print("Error in get_size_img_check()")
        print("Path: " + file_name)

        dump_html(str(file_name), str(img_src))
        pass


def format_url(url):
    try:
        from urllib.parse import urlparse
        url = urllib.parse.unquote(url)
    except Exception as e:
        print(e)
    return url


def init_web():
    global driver
    try:
        # coding=utf-8

        from selenium import webdriver
        driver = webdriver.Firefox(executable_path="./tools/geckodriver")

        # browser exposes an executable file
        # Through Selenium test we will invoke the executable file which will then #invoke actual browser
        # to maximize the browser windowdriver
        driver.maximize_window()
        # get method to launch the URL
        driver.get(PROGRAM_PATH)
        # to refresh the browser
        driver.refresh()
        # to close the browser

        print(driver.title)
        # to print the current URL in console
        print(driver.current_url)
        # get method to launch another URL
    except:
        pass


def refresh_web():  # first import the module
    try:
        driver.refresh()
    except:
        pass


def format_title(title, ext):
    try:
        from urllib.parse import urlparse
        title = urllib.parse.unquote(title)
    except Exception as e:
        print(e)

    title = clean_word(title)

    # Separate term that have capital letter
    full_title = ""
    for i in title:
        if (i.isupper()):
            full_title = full_title + " " + i.capitalize()
        else:
            full_title = full_title + i

    full_title = clean_text(full_title)
    cap_next = False
    full_title_final = ""
    for i in full_title:
        if (cap_next == True):
            full_title_final = full_title_final + i.capitalize()
            cap_next = False

            continue
        if (i == " "):
            full_title_final = full_title_final + i
            cap_next = True

        else:
            full_title_final = full_title_final + i
            cap_next = False

    full_title_final = clean_text(full_title_final)

    title = full_title_final
    title = clean_numbers(title)


def add_to_dic(i):
    global dictionary
    if i not in dictionary:
        dictionary.append(i)


def get_search_urls(query):

    search_urls = []
    google_results = []
    google_results2 = []
    google_results3 = []
    yahoo_results = []
    bing_results = []
    yandex_results = []
    duck_results = []

    if query == None:
        return search_urls

    import search_engine as search_interface

    try:
        google_results2 = search_interface.search_google(query + " photos")
        google_results3 = search_interface.search_google(query + " images")
    except:
        pass

    try:
        google_results = search_interface.search_google(query)

        #yahoo_results = search_interface.search_yahoo(query)
    except:
        pass

    try:
        bing_results = search_interface.search_bing(query)
    except:
        pass

    try:
        duck_results = search_interface.search_yandex(query)
    except:
        pass

    try:
        yandex_results = search_interface.search_yandex(query)
    except:
        pass

    search_urls = insert_in_buffer(yahoo_results)
    search_urls = insert_in_buffer(bing_results)
    search_urls = insert_in_buffer(yandex_results)
    search_urls = insert_in_buffer(duck_results)
    search_urls = insert_in_buffer(google_results2)
    search_urls = insert_in_buffer(google_results3)
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
        urls_memory.sort()
        urls_memory = save_list(urls_memory, "./intelligence/urls_memory")

        urls_visited.clear()
        urls_buffer.clear()

        # Stats
        #x_print(str(len(urls_buffer)) + " In the main buffer")
        #x_print(str(len(urls_visited)) + " In the visited websites")
    else:
        # Load image-miner url global_memory
        load_memory()


def clean_memory():
    with open("urls", "w", encoding="utf-8") as file:
        file.write("")

    with open("urls_visited", "w", encoding="utf-8") as file:
        file.write("")

    with open("urls_images", "w", encoding="utf-8") as file:
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


def learn_keywords(url, title):
    title = clean_text(str(title))
    url_keywords = extract_info_from_url(url)
    final_string = clean_text(title + " " + url_keywords)
    learned_keywords.append(trim(final_string))
    load_title_into_dictionary(final_string)


def load_title_into_dictionary(title):
    for i in title.split(" "):
        i = clean_word(i)
        i = check_stop_words(i)
        learn(i)


def learn(text):

    global learned_relations
    global dictionary, learned_keywords, synonyms

    try:

        index = 0
        # Insert some word in the system dictionary
        text = clean_text(str(text))
        temp_list = text.split(" ")
        list_size = len(temp_list)

        for word in temp_list:
            word = clean_word(word)
            word = check_stop_words(word)

            if (word == None) or word == "" or word == " ":
                continue

            if (index >= 2) and ((index < list_size-2)):
                previous_word = temp_list[index-1]
                next_word = temp_list[index+1]
                next_next_word = temp_list[index+2]
                relation = previous_word + " " + word + " " + \
                    next_word + " " + next_next_word + ": 1"
                if not word in learned_relations:
                    learned_relations.append(relation)

            index = index + 1

            import nlp_tools as n
            definition = n.definition(word)
            if len(definition) == 0:
                continue
            #synonyme = n.synonyms(word)
            #stem = n.stem(word)
            #word = word + "- stem: " + stem + " - definition: "
            synonyms = n.synonyms(word)
            for i in synonyms:
                ii = ii + " " + i
                synonyms.remove(i)

            ii = word + " : " + ii
            synonyms.append(ii)

            #synonyme = n.synonyms(word)
            #stem = n.stem(word)
            #word = word + "- stem: " + stem + " - definition: "
            for i in definition:
                word = word + " : " + str(i)
            #word = word + " - synonyme: " + str(synonyme)
            dictionary.append(word)

        learned_relations = save_list(
            learned_relations, "./intelligence/learned_relations")
        dictionary = save_list(dictionary, "./intelligence/dictionary")
        synonyms = save_list(synonyms, "./intelligence/synonyms")

        learned_relations.sort()
        dictionary.sort()
        synonyms.sort()

        learned_keywords = load_list(
            "./intelligence/learned_keywords", learned_keywords)

        for line in learned_keywords:
            line = line.replace(" - ", "\n")
            line = line.replace(" | ", "\n")
            line = line.replace(" - ", "\n")
            learned_keywords.remove(line)
            learned_keywords.append(line)

        learned_keywords = save_list(
            learned_keywords, "./intelligence/learned_keywords")
        learned_keywords = load_list(
            "./intelligence/learned_keywords", learned_keywords)

        learned_relations = load_list(
            "./intelligence/learned_keywords", learned_keywords)

        for line in learned_relations:
            line = line.replace(" - ", "\n")
            line = line.replace(" | ", "\n")
            line = line.replace(" - ", "\n")
            learned_relations.remove(line)
            learned_relations.append(line)

        learned_relations = save_list(
            learned_keywords, "./intelligence/learned_keywords")
        learned_relations = load_list(
            "./intelligence/learned_keywords", learned_keywords)

    except:
        #input("Error in Learn...")
        pass


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
    global quality_score
    quality_score = 0
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
                            str(quality_score))
                    x_print("PATTERN: " + str(pattern))
                    x_print("URL: " + str(link))
                    x_print("SCORE: " + str(score))
                    x_print("MATCHING KEYWORDS FOUND IN LINK - PASSED")
                    quality_score = quality_score + score
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
    global quality_score
    global pattern_memory
    global current_patterns_hits
    global current_query
    global spam_filter

    if pattern == "" or pattern == " ":
        print("ERROR invalid pattern")
        return quality_score

    try:
        # if not pattern in pattern_memory:
        if is_pattern_spam(pattern, 1):
            quality_score = quality_score - q_bonus
            print("NEGATIVE SPAM Match: " + str(pattern) + " QS="+str(quality_score))
            current_patterns_hits = current_patterns_hits + " - " + pattern

    except Exception as e:
        print(e)
        print("ERROR in is_pattern_in_query")
        return quality_score

    return quality_score


def is_pattern_spam(pattern, q_bonus):
    global QUALITY_SCORE
    global current_patterns_hits, quality_score
    global spam_filter

    for line in spam_filter:
        try:
            if not pattern in pattern_memory:
                if line.find(pattern) >= 0:
                    line = line.replace(pattern, "")
                    quality_score = quality_score - q_bonus
                    print("Negative Match: " + str(pattern) +
                          " QS="+str(quality_score))
                    current_patterns_hits = str(current_patterns_hits) + " - " + str(pattern)

        except Exception as e:
            print(e)
            print("ERROR in is_pattern_spam")
            return quality_score

    return True


def is_pattern_in_query(pattern, q_bonus):
    global quality_score
    global pattern_memory
    global current_patterns_hits

    if pattern == "" or pattern == " ":
        print("ERROR invalid pattern")
        return quality_score

    temp_query = match_query

    try:
        #if not pattern in pattern_memory:
        if temp_query.find(pattern) >= 0:
            temp_query = temp_query.replace(pattern, "")
            quality_score = quality_score + q_bonus
            print("Match: " + str(pattern) + " QS="+str(quality_score))
            current_patterns_hits = current_patterns_hits + " - " + pattern

    except Exception as e:
        print(e)
        print("ERROR in is_pattern_in_query")
        return quality_score

    return quality_score


def prepare_preview(text):
    size = PREVIEW_SIZE
    if (len(text) < PREVIEW_SIZE):
        size = len(text) - 1

    text = clean_text(text[0:size])

    return text


def calculate_quality_score(short_text):

    if short_text == None or short_text == MIN_WORD_SIZE:
        return 0

    try:
        global query_history
        global quality_score
        global pattern_memory

        quality_score = 0

        pattern = ""
        patterns = populate_patterns(short_text)
        print("MATRIX: " + str(patterns))
        meter = 0
        pattern_memory = []
        for pattern in patterns:
            if meter < ANALYSIS_MAX_WORDS:
                # if(pattern_first_check(pattern)):
                # if len(pattern) > MIN_STEM_SIZE:
                quality_score = is_pattern_in_query(pattern, 1)

                meter = meter + 1
    except Exception as e:
        print(e)
        print("Error in calculate_quality_score")

    # BONUS POINTS
    bonus = len(short_text)
    quality_score = quality_score + int(bonus/10)

    print("quality score=" + str(quality_score))
    return quality_score


def spam_check(short_text):

    if short_text == None or short_text == MIN_WORD_SIZE:
        return 0

    try:
        global query_history
        global quality_score
        global pattern_memory

        pattern = ""
        patterns = populate_patterns(short_text)
        print("MATRIX: " + str(patterns))
        meter = 0
        pattern_memory = []
        for pattern in patterns:
            if meter < ANALYSIS_MAX_WORDS:
                # if(pattern_first_check(pattern)):
                # if len(pattern) > MIN_STEM_SIZE:
                quality_score = is_pattern_in_spam_filter(pattern, 1)

                meter = meter + 1
    except Exception as e:
        print(e)
        print("Error in calculate_quality_score")

    print("quality score=" + str(quality_score))
    return quality_score


def populate_signature_stems(pattern, content_signatures):

    signature = ""
    pattern = prepare_pattern(pattern)
    if(pattern_first_check(pattern)):
        if len(pattern) > MIN_STEM_SIZE:
            signature = pattern[0:MIN_STEM_SIZE]

            if not signature in content_signatures:
                content_signatures.append(signature)

        if len(pattern) > MIN_STEM_SIZE*2:
            signature = pattern[MIN_STEM_SIZE:MIN_STEM_SIZE*2]

            if not signature in content_signatures:
                content_signatures.append(signature)

        if len(pattern) > MIN_STEM_SIZE+2:
            signature = pattern[len(pattern)-MIN_STEM_SIZE:len(pattern)]

            if not signature in content_signatures:
                content_signatures.append(signature)

        if len(pattern) > MIN_STEM_SIZE*2+2:
            signature = pattern[MIN_STEM_SIZE+2:MIN_STEM_SIZE*2+2]

            if not signature in content_signatures:
                content_signatures.append(signature)


def verify_content(url, title, text):

    global file_name_keywords

    if (url == None) or (text == None):
        return None

    if (url == "") or (text == ""):
        return None

    global query_size
    global current_text
    global current_preview
    global current_description
    global query_history
    global quality_score

    x_print("\n\nSTARTING PAGE CONTENT VERIFICATION")
    x_print("TITLE: " + str(title))
    x_print("url: " + str(url))

    # Reset at 0 Quality score
    global match_query
    match_query = query_history[0] + " " + match_boost[0]
    match_query = clean_query(match_query)
    # First quick test the title test
    # Only analyse the start of the document
    # First 1000 words to even out everyone
    # and not be affected by SPAMMERS
    preview = prepare_preview(text)
    preview = clean_text(preview)
    x_print("PREVIEW: " + str(preview))
    current_preview = preview

    words_in_text = 0

    quality_score = 0

    if (title != None):
        quality_score = calculate_quality_score(title)
        quality_score = spam_check(title)
        x_print("QS in TITLE is = " + str(quality_score))

        nb_words_in_title = len(title.split(' '))

        FIRST_CONTACT_TEST = (QUALITY_SCORE/nb_words_in_title)/2

        print("QS=" + str(quality_score))
        print("FIRST CONTACT TEST THRESHOLD IS: " +
              str(int(QUALITY_SCORE/nb_words_in_title)*3))

    if (quality_score < LEARN_TO_BLOCK_URL):
        block_url(current_url)

    if (preview != None):
        quality_score = calculate_quality_score(preview)
        #freq = nlp_freq(text)
        # print(freq)

    if quality_score > int(QUALITY_SCORE/2):
        if SAVE_SUBJECT_KEYWORDS == 'ON':
            data = title + "\n"
            data = data + "\n" + preview + "\n"
            import uuid

            global file_name_keywords
            save_data("./intelligence/keywords_memory/" +
                      file_name_keywords, data)

    x_print("QS in PREVIEW is = " + str(quality_score))

    if DEEP_ANALYSIS == 'ON':
        text = clean_text(text)
        quality_score = calculate_quality_score(text)
        x_print("QS in FULL TEXT WITH THRESHHOLD is = " + str(quality_score))
    if preview != None:
        words_in_text = len(preview)
        x_print("TOTAL NUMBER WORDS: " + str(words_in_text))
        x_print("PREPARING THE RESULTS...")

        match_query
        match_query = query_history[0] + " " + match_boost[0]
        x_print("QUERY: " + str(query_history[0].capitalize()))
        x_print("MATCH BOOST: " + str(match_boost[0]))
        x_print("MATCH QUERY: " + str(match_query))
        x_print("TITLE: " + str(title.capitalize()))
        x_print("URL: " + str(url))
        x_print("DB CONTENT: " + str(preview.capitalize()))
        x_print("FINAL QUALITY SCORE (QS) " + str(quality_score))

        adjuster = 12
        if words_in_text == 0:
            words_in_text = 1

        CQS = calculate_CQS(query_size, words_in_text) - adjuster

        if not CQS == None:
            x_print("WEBSITE CALCULATED QUALITY SCORE (CQS) NEEDED IS " + str(CQS-8))

        if quality_score > abs(CQS):
            print("CALCULATED QUALITY SCORE (CQS) TEST PASSED...")
            print("Inserting data in DB")
            insert_data_in_DB(url, title, preview)

        if quality_score > QUALITY_SCORE:
            print("QUALITY SCORE (CQS) TEST PASSED...")
            print("STARTING LEARNING...")
            learning_cycle()
            print("FINISHED LEARNING CYCLE...")
            # Experimental and with feedback
            # from the user for now
            if (quality_score > LEARNING_TFQST):
                print("LEARNING_TFQST - TEST PASSED...")
                print("NEED TO MEDITATE")
                return True
        x_print("URL FAILED THE QUALITY SCORE TEST: " + str(quality_score))
    return False


def insert_data_in_DB(url, title, preview):
    global current_root_url
    x_print("URL PASSES THE QUALITY SCORE TEST: " + str(quality_score))
    x_print("INSERTING DATA IN DB")
    insert_url_data(str(url), str(title), str(preview))
    dump_url_html(current_root_url)


def learning_cycle():
    # Add website root to be spidered
    root = get_root(current_url)
    if not root in urls_buffer:
        urls_buffer.append(root)

    file = open("./intelligence/sites_of_intrest", "a")
    file.write(root + "\n")
    file.close()

    # dump keywords for query boost
    x_print("Learning")
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

    # build patterns
    for pattern in short_text.split(" "):
        if(pattern_first_check(pattern)):
            if not pattern in patterns:
                STEP_SCAN = 1
                ADJ = 0
                STEP = STEP_SCAN
                patterns.append(pattern)

                while (ADJ < len(pattern)):

                    try:
                        pat = pattern[ADJ:MIN_PATTERN_SIZE+ADJ]
                        if (len(pat) >= MIN_PATTERN_SIZE):
                            pat = clean_word(pat)
                            if not pat in patterns:
                                patterns.append(pat)
                                #print("Adding: " + pattern[ADJ:MIN_PATTERN_SIZE+ADJ])

                        ADJ = ADJ + STEP
                    except Error as e:
                        x_print(e)
                        pass

    return patterns

# STILL IN DEVELOPMENT
# This function is not ready and in development
# still looking for a way to learn keywords to
# to the searching and matching functionality


def learn_NQWFT(query, current_title, clean_option):
    pass


def user_feedback(new_keywords_freq1, new_keywords_freq2, new_keywords_freq3):
    global match_boost
    global search_boost
    global current_query
    global match_query

    print(new_keywords_freq3)
    answer = input("Do you want to add the freq3+ keywords to your search?")

    new_keywords_search = ""

    if answer.lower() == "y" or "yes":
        new_keywords_search = new_keywords_freq3

    print(new_keywords_freq2)
    answer = input("Do you want to add the freq2+ keywords to your search?")

    if answer.lower() == "y" or "yes":
        new_keywords_search = new_keywords_search + " ~ " + new_keywords_freq2

    print(new_keywords_freq1)
    answer = input("Do you want to add the freq1+ keywords to your search?")
    if answer.lower() == "y" or "yes":
        new_keywords_search = new_keywords_search + " ~ " + new_keywords_freq1

    print(new_keywords_freq3)
    print(new_keywords_freq2)
    answer = input("Do we add matching? freq 3")
    new_keywords_match = ""

    if answer.lower() == "y" or "yes":
        new_keywords_match = new_keywords_freq3

    print(new_keywords_freq2)
    answer = input("Do we add matching? freq 2")

    if answer.lower() == "y" or "yes":
        new_keywords_match = new_keywords_match + " ~ " + new_keywords_freq2

    print(new_keywords_freq1)
    answer = input("Do we add matching? freq 1")

    if answer.lower() == "y" or "yes":
        new_keywords_match = new_keywords_match + " ~ " + new_keywords_freq1

    search_boost.append(current_query + " ~ " + new_keywords_freq1)
    match_boost.append(current_query + " ~ " + new_keywords_freq2)

    search_boost_data = clean_text(search_boost[0])
    match_boost_data = clean_text(match_boost[0])

    search_boost_data = eliminate_double(search_boost_data)
    match_boost_data = eliminate_double(match_boost_data)

    search_boost_data = search_boost_data + " ~ " + new_keywords_search
    match_boost_data = match_boost_data + " ~ " + new_keywords_search

    match_query = current_query + " " + match_boost_data
    match_query = clean_text(match_query)

    memory = []
    clen_string = ""

    for word in match_query.split(' '):
        if not word in memory:
            clen_string = clen_string + " " + word
            memory.append(word)

    match_query = trim(clen_string)


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
    WORDS_FOR_ANALYSES = 10
    if (words_in_text < WORDS_FOR_ANALYSES):
        return None

    LESS_DIFFICULT = 3
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
    if len(pattern) > LONG_KEYWORD_SIZE:
        return False
    return True


def prepare_pattern(pattern):
    if len(pattern) < MIN_WORD_SIZE:
        return False
    if len(pattern) > MAX_WORD_SIZE:
        return False
    if len(pattern) < MIN_PATTERN_SIZE:
        return False
    if len(pattern) > LONG_KEYWORD_SIZE:
        return False
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
    global url_count
    global img_count
    global spidered_site_count

    # check_media(url)

    x_print("\nPROCESSING url extraction process\nurl: " + url)
    soup = BeautifulSoup(html, "html.parser")
    global current_description
    description = soup.find("meta", attrs={'property': 'description'})

    if description != None:
        current_description = description["content"]

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
                qa = calculate_quality_score(keywords)

                if qa > QUALITY_SCORE:
                    urls_buffer.append(link)

            if (FREELY_GRAB_URLS == 'ON'):
                urls_buffer.append(link)

        except Error as e:
            x_print(e)

    return urls_buffer


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

    items = ["\xa0", "|", "(", ")", "[", "]", "{", "}", "  ", "…", "[", "]", "?", "",
             "»", "#", ":", "–", "©", ",", ".", "\t", "#", "*", "/", "\\", "~", "^", "–", "]"]
    text = text.lower()

    for filter in items:
        text = text.replace(filter, " ")

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("\r", " ")

    while "  " in text:
        text = text.replace("  ", " ")

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

            result = verifify_image_alt_tag(img_info)

            if(result):
                print("IMAGE ALT TEST PASSED")

            result = full_img_verification(link, img_info)
            extract_img(link, url)

        except Error as e:
            x_print(e)
            print("Error in IMAGE EXTRACTION MAIN FRAME")

    closing_html_dump(current_img_src, current_url)
    # Double TIME_LOCK
    return urls_images


def full_img_verification(link, img_info):

    print("link : " + str(link))
    if img_info != None:
        print("img_info : " + img_info)
    print("current_img_keywords : " + current_img_keywords)

    qa = calculate_quality_score(current_img_keywords)
    print("QA: " + str(qa))

    if qa > IMG_ALT_QS:
        # closing_dump(link.get("src"))
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
            except Error as e:
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

            except Error as e:
                x_print(e)
                return False
    return True


def verifify_image_alt_tag(img_tag_text_info):
    global quality_score
    global current_image_alt_text_test
    global pattern_memory
    global current_img_keywords

    pattern_memory = []
    quality_score = 0
    if img_tag_text_info != None:
        if img_tag_text_info != "" or img_tag_text_info != " ":
            print("image the info: ")
            print(img_tag_text_info)
            quality_score = calculate_quality_score(img_tag_text_info)
            quality_score = quality_score * 2
            current_img_keywords = current_img_keywords.lower() + " " + \
                img_tag_text_info.lower()
            print("QA: " + str(quality_score))

        if (IMG_ALT_VERIFICATION == "ON"):
            if quality_score < IMG_ALT_QS:
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
    html = ""
    html = html = '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="30" /><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>'
    html = html + '<center><form action = "search.html" method = "POST"><input type = "submit" value = "Let go again!!!"></form><br></center>'
    html = html + '<center>Results for ' + current_query + \
        '</center><br><center>The system is searching real-time the net, learning and thinking...</center><br><br></body></html>'

    html_code = '<!DOCTYPE html><html lang="en"><body><center><h1>Image-Hunter</h1><h4>Playing around for learning reasons<br>with AI and Images</h4><img src="NpTzUs.webp" style="display:inline-block;width:500px;height:auto;object-fit:contain;" border="2"><p>The page will refresh when results are ready.</p><p>Or follow this <a href="../interface/">link </a><p><a href="image-hunter-img-view.html">Image view </a>, <a href="image-hunter.html">Detailed view </a>or <a href="image-hunter-search.html">Search Results</p></form></center></body></html>'
    f = open("./dev/image-hunter.html", "w")
    f.write(str(html_code))
    f.close()

    f = open("./dev/image-hunter-original.html", "w")
    f.write(str(html_code))
    f.close()

    f = open("./dev/image-hunter-img-view.html", "w")
    f.write(str(html_code))
    f.close()

    f = open("./dev/image-hunter-search.html", "w")
    f.write(str(html_code))
    f.close()

    init_web()


def dump_html(img, img_src):
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

    query_foler = current_query.replace(" ", "-")

    if HTML_IMAGE_PER_PAGE < html_img_counter:
        closing_html_dump(img_src, current_url)
        html_img_counter = 0
        html_file_name = str(uuid.uuid4())
        current_query = query_history[0]
        query_foler = current_query.replace(" ", "-")

    if HTML_IMAGE_PER_PAGE < html_img_counter+1:
        url = PROGRAM_PATH
        refresh_web()
        #open_web(str(url + "/EVERYTHING-" + query_foler + "-" + html_file_name + ".html"))

    html_img_counter = html_img_counter + 1

    # GLOBAL THUMBNAIL VIEW
    #file_name = str(uuid.uuid4())
    # dump_thumbnail_html(img_src,file_name)

    html = '<a href="' + img_src + '"><img border="2" src="' + img_src + \
        '" style="display:inline-block;width:15%;height:15%;object-fit:contain;" /></a>'
    f = open("./interface/global-view-" + html_file_name+".html", "a")
    f.write(str(html))
    f.close()

    closing_html_dump(img_src, current_url)

    global current_image_alt_text_test
    hit = False

    if (current_image_alt_text_test == True) and (MIN_QUALITY_IMAGE_SIZE < current_img_size):
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-BEST-IMG-SIZE-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (current_image_alt_text_test == True):
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (MIN_QUALITY_IMAGE_SIZE < current_img_size):
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BIG-SIZE-"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if quality_score > IMG_ALT_QS and MIN_QUALITY_IMAGE_SIZE < current_img_size:
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BIG-SIZE-TEXT-ALT-MATCH-QS-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if quality_score > IMG_ALT_QS:
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-QS"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if quality_score > IMG_ALT_QS and current_image_alt_text_test == True and MIN_QUALITY_IMAGE_SIZE < current_img_size:
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/SIZE-TEXT-ALT-MATCH-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (hit == True):

        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BEST-RESULTS-" + query_foler +
                 "-" + html_file_name + ".html", "a")
        f.write(str(html))
        f.close()

        if img.find("webp") >= 0:
            shutil.copy(img, "./dev/NpTzUs.webp")

        html = '<center><a href="' + current_root_url + '"><img src="' + img_src + ' " alt="' + current_preview + \
            '" style="display:inline-block;width:40%;height:auto;object-fit:contain;"></a></center>'
        html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + current_root_url + \
            '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + \
            current_img_keywords.upper() + " [...] " + '</center>'
        f = open("./dev/results.html", "a")
        f.write(str(html_code))
        f.close()

        html_code = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:14%;height:14%;object-fit:contain;" /></a>'
        f = open("./dev/image-hunter-img-view.html", "a")
        f.write(str(html_code))
        f.close()

        html = '<center><a href="' + current_root_url + '"><img src="' + img_src + ' " alt="' + current_preview + \
            '" style="display:inline-block;width:40%;height:auto;object-fit:contain;"></a></center>'
        html_code = html + '<center><b>TITLE: ' + current_title.capitalize() + '</b></center><center><a href="' + current_root_url + \
            '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + \
            current_img_keywords.upper() + " [...] " + '</center>'
        f = open("./dev/image-hunter.html", "a")
        f.write(str(html_code))
        f.close()

        html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + \
            '</b></center><a href="' + current_root_url + \
            '">' + current_root_url + '</a></center>'
        f = open("./dev/image-hunter-search.html", "a")
        f.write(str(html_code))
        f.close()

    html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
        '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
    f = open("./interface/EVERYTHING-" + query_foler +
             "-" + html_file_name + ".html", "a")
    f.write(str(html))
    f.close()


def closing_html_dump(img_src, url):

    global current_title
    global current_url
    global current_root_url
    global current_query
    global current_text
    global current_img_src
    global current_img_keywords
    global current_patterns_hits
    global quality_score

    html = '<center><a href="' + current_root_url + '"><img border="1" src="' + img_src + \
        '" style="display:inline-block;width:50%;height:50%;object-fit:contain;" /></a></center>'
    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + \
        current_root_url + '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + current_img_keywords.capitalize() + " [...] " + '</center><center><b>PREVIEW:</b>' + current_preview.capitalize() + " [...] " + '</center><center><a href="' + \
        img_src + '">' + img_src + '</a></center><br>QUALITY SCORE: ' + str(quality_score) + '<br>QUERY: ' + str(
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
    global quality_score

    html = '<center><center><b>' + current_title.capitalize() + ' QS SCORE: ' + \
        str(quality_score) + ' </b></center>'
    html_code = html + '<center><a href="' + \
        str(url) + '">' + url + '</a></center><br>'
    #html_code = html + '<center> ' + current_text + '</center>'
    f = open("./interface/URLS-" + file + ".html", "a")
    f.write(str(html_code))
    f.close()

    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + \
        '</b></center><a href="' + current_root_url + \
        '">' + current_root_url + '</a></center>'
    f = open("./dev/image-hunter-search.html", "a")
    f.write(str(html_code))
    f.close()


def dump_thumbnail_html(img_src, file_name):

    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_keywords
    global html_file_name
    global html_img_counter
    global current_patterns_hits
    global quality_score

    html = '<center><a href="' + str(img_src) + '.html"><img border="2" src="' + img_src + \
        '" style="display:inline-block;width:25%;height:25%;object-fit:contain;" /></a></center>'
    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + \
        current_url + '">' + current_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + current_img_keywords.capitalize() + " [...] " + '</center><center><b>PREVIEW:</b>' + current_preview.capitalize() + " [...] " + '</center><center><a href="' + \
        img_src + '">' + img_src + '</a></center><br>QUALITY SCORE: ' + str(quality_score) + ' <br>IMAGE Keywords: ' + str(
            current_img_keywords) + ' <br>PATTERNS: ' + str(current_patterns_hits) + '<div><hr>'
    f = open("./interface/" + file_name + ".html", "a")
    f.write(str(html_code))
    f.close()


def intro_html_dump():

    global current_title
    global current_url
    global current_text
    global html_file_name

    html_code = '<link rel="stylesheet" type="text/css" href="../archive/interface/style.css" media="screen" /><div id="main">'
    f = open("./interface/main-" + html_file_name + ".html", "a")
    f.write(str(html_code))
    f.close()


def trim(text_section):
    if text_section == None:
        return None
    if text_section == "" or " ":
        return None
    text_section = clean_word(text_section)
    text_section = text_section.lstrip()
    text_section = text_section.rstrip()
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
                    url = trim_url(url)
                    url = url.replace("\n", "")
                    clean.append(url)
    return clean


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title != None:
        title = soup.title.get_text()
        return title
    return None


def format_for_pattern_check(url, title, text):

    global quality_score
    url = format_url(url)

    if (title == None):
        title = ""
        quality_score = quality_score - 2
    else:
        quality_score = quality_score + 2

    title = title.lower()

    if (text == None):
        text = ""
        quality_score = quality_score - 3
    else:
        quality_score = quality_score + 3
        
    text = text.lower()
    text = text.replace("\'", " ")

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
        #x_print("URL VERIFICATION FAILED - IN BASIC CHECK")
        #x_print("URL: " + str(url))
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
        #x_print("URL VERIFICATION FAILED - IN BASIC CHECK")
        #x_print("URL: " + str(url))
        pass
    return result


def close_loop():

    global save_count
    global url_count
    global img_count
    global urls_buffer
    global current_query
    global query_history
    global stop_urls
    global dictionary
    global learned_relations

    #x_print("Random approche pattern...")
    # shuffle_list(urls_buffer)
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

        if (len(urls_buffer) > URL_LIMIT_AMOUNT):
            urls_buffer = check_critical_amount_of_urls(urls_buffer)

        print("SAVE URLS")

        save_memory()
        save_media()

        save_count = 0

        x_print("SAVING DATA")
        stop_urls = save_list(stop_urls, "./intelligence/stop_urls")
        query_history = save_list(
            query_history, "./intelligence/query_history")
        dictionary = save_list(dictionary, "./intelligence/dictionary")
        learned_relations = save_list(
            learned_relations, "./intelligence/learned_relations")


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

    if (not result):
        x_print("\nSECOND URL VERIFICATION FAILED...")
        x_print("FIRST CHECK FAILED...")
        relax(TIME_LOCK)
        x_print("Random approche pattern...")

        if (RANDOM_START > approch_counter):
            approch_counter = 0
            shuffle_list(urls_buffer)
            shuffle_list(urls_buffer)
            shuffle_list(urls_buffer)

        approch_counter = approch_counter + 1

        return result
    else:
        x_print("FIRST CHECK SUCCESS...\n")

    return result


def read_evaluate_learn(url, html):

    global current_url
    global current_title
    global current_text
    global url_count
    global img_count

    x_print("URL count : " + str(url_count))
    x_print("Image count :" + str(img_count))
    x_print("Current URL :" + str(url))

    title = get_title(html)
    text = get_html_textual_content(html)
    url, title, text = format_for_pattern_check(url, title, text)
    result = verify_content(url, title, text)

    if (DOWNLOAD_EVERYTHIING == 'ON'):
        result = True
        if (result):
            current_url = url
            title = clean_text(title)

            current_title = title
            current_text = text

    if (DOWNLOAD_HTML == "ON"):
        download_website_html_page(html)

    return result


def spider(url, html):

    global urls_buffer
    global urls_visited
    global urls_images

    urls_buffer = extract_urls(url, html)
    urls_images = extract_images(url, html)

    if (url in urls_buffer):
        urls_buffer.remove(url)

    if (not url in urls_buffer):
        urls_visited.append(url)

    x_print("Random approche pattern...")
    if (RANDOM_START < approch_counter):
        shuffle_list(urls_buffer)
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
        page = requests.get(str(url), headers={
                            'User-Agent': ua.random}, proxies=proxies, timeout=10)
        if page.status_code == 200:
            global proxy_good, i_proxy
            i_proxy = id_proxy
            proxy_good = True
            return page
        return None
    except:
        return None

# Buscar correo en la base de datos


def search_DB_for_urls(db_file, email, frase):
    import sqlite3
    from sqlite3 import Error
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        sql = 'SELECT COUNT(*) FROM emails where email LIKE "%' + \
            str(email) + '%" AND phrase LIKE "%' + str(frase) + '%"'
        result = c.execute(sql).fetchone()
        conn.close()
        return (result[0])
    except Error as e:
        pass


def open_url_no_proxy(url):
    try:
        page = requests.get(str(url), headers={'User-Agent': ua.random}, timeout=10)
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
        page = requests.get(str(url), headers={
                            'User-Agent': ua.random}, proxies=proxies, timeout=30)
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

    print("STARTING A NEW LOOP")
    print("URL: " + str(url))
    print("NUMBER OF URLS LEFT TO MINE: " + str(len(urls_buffer)))
    print("Image count: " + str(img_count))
    print("Url count: " + str(url_count))
    print("Save step: " + str(save_count))


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

    global_count = 0

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

    learned_relations = load_list(
        "./intelligence/learned_relations", learned_relations)
    learned_keywords = load_list(
        "./intelligence/learned_keywords", learned_keywords)

    query_history = load_list("./intelligence/query_history", query_history)
    search_boost = load_list("./intelligence/search_boost", search_boost)
    match_boost = load_list("./intelligence/match_boost", match_boost)
    user_profil = load_list("./intelligence/user_profil", user_profil)
    proxies_list = load_list("./tools/proxies", proxies_list)
    spam_filter = load_list("./intelligence/spam_filter", spam_filter)

    x_print("Starting image mining process...\n")
    x_print("Loading the memory...\n")

    for url in urls_buffer:

        new_turn()

        current_root_url = url
        current_url = url

        print_loop_info(url)
        result = first_check(url)

        if (result):
            try:
                print("DOWNLOADING URL: " + url)
                page = get_request_url(url)
                if page == None:
                    continue
                if page.status_code == 200:
                    result = read_evaluate_learn(url, page.text)

            except Error as e:
                x_print(e)
                print("ERROR - in get_web_page Requests")
                close_loop()
                continue

            try:
                if page == None or result == False:
                    continue

                if SPIDER_ALL_IMAGES == 'ON':
                    result = spider(url, page.text)
                else:
                    if quality_score > QUALITY_SCORE:
                        result = spider(url, page.text)

            except Error as e:
                x_print(e)
                print("ERROR - in spider extraction process")
                close_loop()
                continue

            try:
                if (result):
                    keywords = prepare_keywords_for_database(current_title)
                    keywords = clean_text(keywords)
                    keywords = trim(keywords)
                    keywords = learn_keywords(keywords)

                close_loop()

            except Error as e:
                x_print(e)
                print("ERROR in closing loop process")
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


def nlp_freq(text):

    import nltk
    from nltk.corpus import stopwords
    stopwords.words('english')
    tokens = [t for t in text.split()]

    clean_tokens = tokens[:]

    sr = stopwords.words('english')

    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
        else:
            if len(token) <= MIN_WORD_SIZE or len(token) >= MAX_WORD_SIZE:
                clean_tokens.remove(token)

    freq = nltk.FreqDist(clean_tokens)
    print(freq)
    for key, val in freq.items():
        if val >= 3:
            if len(key) >= MIN_WORD_SIZE:
                if len(key) <= MAX_WORD_SIZE:
                    print(str(key) + ':' + str(val))

    freq.plot(20, cumulative=False)
    return freq

# Optional request object


def search_engine_filter(final):
    if "google" or "bing" or "yahoo" in final:
        final = final.replace("google", " ")
        final = final.replace("bing", " ")
        final = final.replace("yahoo", " ")
    return final


def requests_urllib(url):

    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': ua.random
        })

    conn = urllib.request.urlopen(req, timeout=10)
    status = conn.getcode()
    contentType = conn.info().get_content_type()

    return conn, status, contentType


def main(query):
    global current_query
    x_print("INITIATION OF THE SPIDER/SCRAPER")
    init_program(query)

    current_query = query
    first_dump(current_query)

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


if __name__ == '__main__':
    import sys
    import threading

    query = ""
    if (len(sys.argv) > 1):
        query = sys.argv[1]

    while (True):

        # Entry point
        if (query == ""):
            # Created the Threads
            t1 = threading.Thread(target=main(""))
            t1.run()
            t1.join()
            t1.isDaemon(True)

        file = open("./data", "r")
        query = file.readlines()

        try:

            if (query_memory != query):
                # Created the Threads
                t1 = threading.Thread(target=main(query[len(query)-1]))
                t1.run()
                t1.join()
                t1.isDaemon(True)
        except:
            pass

        relax(TIME_LOCK)
        query_memory = query
