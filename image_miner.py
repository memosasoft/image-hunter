
#!/usr/bin/env python
import uuid
import configparser
from nturl2path import url2pathname
import webbrowser
import datetime  # needed to create unique image file name
import mimetypes  # needed for download functionality
import shutil  # to save it locally
import sqlite3
import time  # needed to create unique image file name
# Importing Necessary Modules
import urllib.request
from sqlite3 import Error
from urllib.request import HTTPError, URLError

import requests  # to get image from the web
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search

from search import search_yahoo

# Session url and img global_memory
global_memory = []
url_global_memory = []
file_memory = []

current_url = ""
current_title = ""
current_html = ""
current_text = ""
current_img_keywords = ""

img_count = 0
url_count = 0
save_count = 0
query_size = 0

quality_score = 0

# Program url buffers
urls_buffer = []  # long-term buffer =
urls_visited = []  # visited_links
urls_image_buffer = []

# search urls from google
search_urls = []
scraper_dictionary = []
qb_boost = []

# Learning array for text the system reads
learned_keywords = []
ua = UserAgent()

# keywords container for query and page content
query_history = []

# stop words and urls for blocking urls
stop_words = []
stop_urls = []

#!/usr/local/bin/python
configuration = configparser.ConfigParser()
configuration.read('config.env')

RELAX_TIME = float(configuration.get('CONFIG', 'RELAX_TIME'))
TIME_LOCK = float(configuration.get('CONFIG', 'TIME_LOCK'))
QUALITY_SCORE = float(configuration.get('CONFIG', 'QUALITY_SCORE'))
KEYWORDS_IN_LINK = int(configuration.get('CONFIG', 'KEYWORDS_IN_LINK'))
ANALYSIS_MAX_WORDS = int(configuration.get('CONFIG', 'ANALYSIS_MAX_WORDS'))
MIN_LINK_SIZE = int(configuration.get('CONFIG', 'MIN_LINK_SIZE'))
MAX_LINK_SIZE = int(configuration.get('CONFIG', 'MAX_LINK_SIZE'))
MIN_WORD_SIZE = int(configuration.get('CONFIG', 'MIN_WORD_SIZE'))
MIN_STEM_SIZE = int(configuration.get('CONFIG', 'MIN_STEM_SIZE'))

QUERY_BOOST = str(configuration.get('CONFIG', 'QUERY_BOOST'))
MIN_IMAGE_SIZE = int(configuration.get('CONFIG', 'MIN_IMAGE_SIZE'))
DOWNLOAD_HTML = str(configuration.get('CONFIG', 'DOWNLOAD_HTML'))

DEBUG_CONSOLE = str(configuration.get('CONFIG', 'DEBUG_CONSOLE'))
DEBUG_LOG = str(configuration.get('CONFIG', 'DEBUG_LOG'))
DB_TEXT_SIZE = int(configuration.get('CONFIG', 'DB_TEXT_SIZE'))

SAVE_COUNT = int(configuration.get('CONFIG', 'SAVE_COUNT'))
DIG_FOR_URLS = "ON"
MAX_WORKSPACE_SIZE = int(configuration.get('CONFIG', 'MAX_WORKSPACE_SIZE'))
LONG_KEYWORD_SIZE = int(configuration.get('CONFIG', 'LONG_KEYWORD_SIZE'))
MIN_PATTERN_SIZE = MIN_STEM_SIZE
media_files = "psd,apng,avif,bmp,gif,ico,cur,tif,tiff,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp,webm,ogg,tiff,ico,jpg,gif,png,bmp"
query_boost = "photography,photo,image,picture,pics,gallery,4k,hd,wallpaper,art,artwork,collection,png,svg,webp,webm,ogg,tiff,ico,jpg,gif,png,bmp"


def init_program():

    global query_size
    global query_history

    # Query global_memory self-learning object
    load_memory()

    # User system-interaction
    x_print("WELCOME TO Image-Miner")
    x_print("Powered by Python")

    #x_print("In memory of META-CRAWLER 1990")
    x_print("Image-Miner is connected to Google, Yahoo and Bing")
    x_print("Thank you for using Image-Miner")

    # clean urls lists
    user_input = input("\nClean start? (y/n)")

    # User system-interaction
    x_print("Saving images and media to archives folder")

    # transfert images and media to archives folder
    save_to_archive("./media/", "./archives/media/")
    save_to_archive("./interface/", "./archives/interface/")

    x_print("Images and media saved\n")

    # User system-interaction
    # x_print("SETUP PROCESS")
    # x_print("Starting setup process and cleanup")
    setup_process(user_input)

    query = input("What type of images you want to spider?")
    x_print("\nSEARCH MODULE\n")
    x_print("Connecting to Google, Yahoo and Bing")
    x_print("This may take a while")
    x_print("We are saving everything in the Database")
    x_print("For learning...\n")
    x_print("Thank you for your patience...")
    # add the user query to the user queries list
    # add also to the query_history list
    x_print("\nNEW SELF-LEARNING FEATURE - AI")
    x_print("\nLoading user query global_memory for system self-learning purposes")
    query = clean_query(query)
    query_temp = query.split(" ")
    query_size = len(query_temp)
    query_history = load_list("./intelligence/query_history", query_history)
    query_history.insert(0, query)
    learned_keywords.append(query)
    query_history = save_list(query_history, "./intelligence/query_history")

    # MULTIPLE QUERIES & QUERY BOOST
    # Simple functionality nothing fancy
    # Objective get better image related searches
    # from Google, Yahoo and Bing
    if QUERY_BOOST == "ON":
        search_urls = multiple_search_prototype(str(trim(query)))
    else:
        search_urls = get_search_urls(str(trim(query)))

    insert_in_buffer(search_urls)


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
    x_print("Concepts found in url ")
    x_print(str(trim(info)))
    return info


def clean_query(query):

    item = ["  ", ",", ".",
            "-", "+", "{", "}", "[", "]"]

    for i in item:
        while query.find(i) >= 0:
            query = query.replace(i, " ")
    query = query.strip()
    query = query.lstrip()
    query = query.lower()

    # Need to think...
    # Add the words
    # to learned keywords?
    #
    # Is it a good idea?
    #
    # Or are we going to hurt the system
    # with bad user input

    return query

# EXPERIMENTAL MULTIPLE QUERY_BOOST
# ADDING IMAGE RELATED GENERAL KEYWORDS
# TO GET MORE SEARCH RESULTS


def multiple_search_prototype(query):
    # The code is not optimize yet
    # It dirty code so please no jokes...
    # Normalize the query string
    original_q = query.lower()
    prototype_rq = query.lower()
    query = query.lower()

    # Prepare query with extra image termes
    query = query + " " + query_boost
    query = clean_query(query)

    x_print("\nQUERY_BOOST ACTIVATED\n")
    x_print("\nSending multiple queries")
    x_print("with additional general image keywors\n")

    x_print("THIS IS A LONG PROCESS")
    x_print("PLEASE BE PATIENT\n")
    query_morph = str(query).split(' ')

    import random
    random.shuffle(query_morph)

    for i in query_morph:
        prototype_rq = prototype_rq + " " + i

    # PROTOTYPE EXTRA Random QUERY 1 and 2
    prototype_rq1 = prototype_rq + " archive digital"

    prototype_t = str(prototype_rq1).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    for i in prototype_t:
        prototype_x = prototype_x + " " + i

    prototype_rq1 = prototype_x
    query_history.insert(0, prototype_rq1)

    prototype_rq2 = prototype_rq + " galleries photo"

    prototype_t = str(prototype_rq2).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    for i in prototype_t:
        prototype_x = prototype_x + " " + i

    prototype_rq2 = prototype_x
    query_history.insert(0, prototype_rq2)

    prototype_rq3 = prototype_rq + " amazing digital images"

    prototype_t = str(prototype_rq3).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    for i in prototype_t:
        prototype_x = prototype_x + " " + i

    prototype_rq3 = prototype_x
    query_history.insert(0, prototype_rq3)
    prototype_rq4 = prototype_rq + " images galery photos"

    prototype_t = str(prototype_rq4).split(' ')
    prototype_x = ""
    import random
    random.shuffle(prototype_t)

    for i in prototype_t:
        prototype_x = prototype_x + " " + i

    prototype_rq4 = prototype_x
    query_history.insert(0, prototype_rq4)
    # Add extra image related search terms to enhance
    # the search results the list is in config.env
    search_urls = get_search_urls(query.strip())
    relax(TIME_LOCK)

    list_rq1 = get_search_urls(prototype_rq1.strip())
    relax(TIME_LOCK)

    list_rq2 = get_search_urls(prototype_rq2.strip())
    relax(TIME_LOCK)

    list_rq3 = get_search_urls(prototype_rq3.strip())
    relax(TIME_LOCK)

    list_rq4 = get_search_urls(prototype_rq4.strip())
    relax(TIME_LOCK)

    list_original = get_search_urls(original_q.strip())

    for i in list_rq1:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, prototype_rq1)

    for i in list_rq2:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, prototype_rq2)

    for i in list_rq3:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, prototype_rq3)

    for i in list_rq4:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, prototype_rq4)

    for i in list_original:
        i = urllib.parse.unquote(i)
        insert_search_urls(i, original_q)

    list_buffer = []
    search_urls = add_list_to_list(search_urls, list_rq1)
    search_urls = add_list_to_list(search_urls, list_rq2)
    search_urls = add_list_to_list(search_urls, list_rq3)
    search_urls = add_list_to_list(search_urls, list_rq4)
    search_urls = add_list_to_list(search_urls, list_original)

    # System interaction with user
    x_print("We got: " + str(len(search_urls)) + " urls to mine\n")
    x_print("Thank you Google, Yahoo and Bing...")
    # Inserting urls at the beginning of the url list
    x_print("\nAdding the search urls to the begining of search buffer...")

    return search_urls


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
        if (len(i) <= MIN_LINK_SIZE):
            continue
        if (len(i) >= MAX_LINK_SIZE):
            continue
        if not i.find("http") >= 0:
            continue

        if not i in urls_buffer:
            urls_buffer.insert(0, str(i))

    urls_buffer = save_list(urls_buffer, "urls")
    # save_memory()

# Self learning object to gain ai from
# user interaction - Prototype


def load_query_history():
    global query_history
    x_print("LOADING query history")
    with open("./intelligence/query_history", "r") as file:
        # reading each line"
        for line in file:
            line = clean_text(line)
            query_history.append(line)
    return query_history


def save_memory():
    global query_history
    global qb_boost
    global urls_buffer
    global urls_visited
    global scraper_dictionary
    global learned_keywords
    global urls_image_buffer

    x_print("Saving memory")
    urls_buffer = save_list(urls_buffer, "urls")
    urls_visited = save_list(urls_visited, "urls_visited")
    learned_keywords = save_list(
        learned_keywords, "./intelligence/learned_keywords")
    scraper_dictionary = save_list(
        scraper_dictionary, "./intelligence/scraper_dictionary")
    urls_image_buffer = save_list(urls_image_buffer, "urls_image_buffer")
    
    qb_boost = save_list(qb_boost, "./intelligence/query_boost")
    query_history = save_list(query_history, "./intelligence/query_history")


def load_memory():

    global urls_buffer
    global urls_image_buffer
    global urls_visited
    global query_history
    global qb_boost
    global scraper_dictionary
    global learned_keywords

    x_print("Loading memory")
    urls_visited = load_list("urls_visited", urls_visited)
    urls_buffer = load_list("urls", urls_buffer)
    urls_image_buffer = load_list("urls_image_buffer", urls_image_buffer)
    query_history = load_list("./intelligence/query_history", query_history)
    learned_keywords = load_list(
        "./intelligence/learned_keywords", learned_keywords)
    scraper_dictionary = load_list(
        "./intelligence/scraper_dictionary", scraper_dictionary)
    qb_boost = load_list(
        "./intelligence/query_boost", qb_boost)


def save_query_history():
    # write url in visited site file
    global query_history
    temp_global_memory = []

    with open("./intelligence/query_history", "w", encoding="utf-8") as file:
        for query in query_history:
            if not query is None:
                if not query in temp_global_memory:
                    file.write(query + "\n")
                    temp_global_memory.append(query)
        file.close()
    return query_history


def insert_search_urls(url, query):
    try:
        db_file = "./archives/data/data-miner.db"
        conn = sqlite3.connect(db_file)

        c = conn.cursor()
        c.execute("INSERT INTO search (url, query) VALUES (?,?)",
                  (url, query))
        conn.commit()

        conn.close()
    except Error as e:
        x_print(e)


def check_keywords_in_urls(url):
    global query_history

    for key in query_history[0].split(" "):
        key = str(key).lower()
        url = str(url).lower()
        if len(key) > 2:
            if url.find(key) >= 0:
                return True
    return False


def insert_url_data(url, title, text):

    title = clean_text(title)
    text = clean_text(text)

    global current_title
    current_title = title

    learned_keywords.append(title)
    learned_keywords.append(text)

    try:
        db_file = "./archives/data/data-miner.db"
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("INSERT INTO url (url, title, text) VALUES (?,?,?)",
                  (url, title, text))
        conn.commit()
        conn.close()
    except Error as e:
        x_print(e)


def check_url(url):
    url = url.lower()
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
    if url.find(str(".xlm")) >= 0:
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
    if url.find(str(".mp4")) >= 0:
        download(url)
        return False
    if url.find(str(".m3u")) >= 0:
        download(url)
        return False
    if url.find(str(".mkv")) >= 0:
        download(url)
        return False
    return True

def check_media(url):
    if url == None:
        return False

    url = url.lower()
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
    if url.find(str(".xlm")) >= 0:
        return False
    if url.find(str(".xls")) >= 0:
        return False
    if url.find(str(".htm")) >= 0:
        return False
    if url.find(str(".zip")) >= 0:
        return False
    # There is a small bug with the end of the file
    # this function should clean de url
    for media_ext in media_files.split(","):
        if url.find(str("."+media_ext.strip())) >= 0:
            download(url)
            return True
    return False

def clean_filename(file_name):
    file_name = urllib.parse.unquote(file_name)
    if (file_name.find("?") >= 0):
        end = file_name.find("?")
        file_name = file_name[0:end]
    return file_name

def download(url):

    global global_memory
    global img_count
    global url_count
    global current_url

    save_path = './media/'
    ext = url.split(".")[-1]
    file = url.split("/")[-1]
    file = clean_filename(file)

    target = str(save_path) + str(file)

    if url not in global_memory:
        try:

            x_print("First test the image URL")
            x_print("Url: " + current_url)
            result = url_verification(url)

            if (result):
                x_print("VERIFICATION PASSED...")
                x_print("Second url test for image source")

                result = verify_link(url)
                if (not result):
                    x_print("VERIFICATION Failed...")
                    return None

            x_print("Second test for image URL")
            x_print("VERIFICATION PASSED...")
            # NEED TO VERIFY KEYWORDS

            if (result):

                try:
                    import wget
                    target = get_image(url)
                    verify_image_size(str(target), str(url))
                except:
                    try:
                        wget.download(str(url), str(target))
                        verify_image_size(str(target), str(url))
                    except:
                        print("Error with the requests...")
                        x_print("Download ERROR...\n")
                        return None

                x_print("\nURL: " + str(url))
                x_print("Download completed\n")
                print("Image count: " + str(img_count))
                print("Url count: " + str(url_count))
                x_print("To avoid being blocked and detected")
                x_print("We must take a break...\n")
                relax(TIME_LOCK)
            else:
                x_print("DOWNLOAD AI TESTS FAILED...\n")
                return None

        except Error as e:
            x_print(e)
            x_print("Error downloading")
            x_print("URL causing error is: " + str(url) + "\n")
            x_print("File download location: " + str(target) + "\n")

            if(1 < img_count):
                img_count = img_count - 1

            return None

    # What ever site must be
    # inserted in the images buffer
    if (not url in urls_image_buffer):
        urls_image_buffer.append(url)

    if (url in urls_buffer):
        urls_buffer.remove(url)

    img_count = img_count + 1

    return True

def extract_keywords(filename):
    keywords = ""
    buffer = ""
    keywords = filename.replace("-"," ")
    keywords = keywords.replace("+"," ")
    keywords = keywords.replace("%"," ")
    keywords = keywords.replace("&"," ")
    keywords = keywords.replace("/"," ")
    keywords = keywords.replace("*"," ")
    keywords = keywords.replace("_"," ")
    keywords = keywords.replace("!"," ")
    keywords = keywords.replace("@"," ")
    keywords = keywords.replace("#"," ")
    keywords = keywords.replace("$"," ")
    keywords = keywords.replace("("," ")
    keywords = keywords.replace(")"," ")
    keywords = keywords.replace("."," ")
    keywords = keywords.replace("-"," ")
    keywords = keywords.replace("."," ")
    keywords = keywords.replace("["," ")
    keywords = keywords.replace("]"," ")
    
    keywords = keywords.replace("jpg"," ")
    
    keywords = keywords.replace("jpeg"," ")
    
    keywords = keywords.replace("gif"," ")
    
    keywords = keywords.replace("bmp"," ")

    keywords = keywords.replace("svg"," ")
    
    for word in keywords.split(" "):
        
        MIN_WORD_SIZE = 2
        MAX_WORD_SIZE = 17
        
        if len(word) > MAX_WORD_SIZE: 
            continue

        if len(word) < MIN_WORD_SIZE: 
            continue
        
        if (word.isnumeric()):
            continue

        if (word.isalpha()):
            buffer = buffer + " " + word
            continue
        if (word.isalnum()):
            buffer = buffer + " " + word

    keywords = str(trim(buffer))

    return keywords


def get_image(url):
    import os
    # Set up the image URL and filename
    filename = url.split("/")[-1]
    # file name creating with timestamp
    global current_img_keywords

    try:
        current_img_keywords = extract_keywords(filename)
    except:
        pass

    filename = datetime.datetime.now()
    filename = filename.strftime("img-%Y%M%H%S%f")

    # Open the url image, set stream to True, this will return the stream content.
    # r = requests.get(url, stream=True)
    r = requests.get(url, stream=True, headers={'User-Agent': ua.random}, timeout=20)
    ext = get_extension(r)

    filename = str(uuid.uuid4())
    filename = filename + "." + ext

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open("./media/" + filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        target = "./media/" + filename
        return target


def verify_image_size(target, web_src):
    
    print("Verification of image...") 
    print("Before transfer to depot...")
    
    try:
        get_size_img_check(target, web_src)
    except Error as e:
        x_print(e)
        print("Error in get_size_img_check")


def build_title_from_filename(url):
    ext = url.split(".")[-1]
    file = url.split("/")[-1]
    title = format_title(str(file), str(ext))
    return title


def get_size_img_check(img_file, img_src):
    import os
    import shutil
    from pathlib import Path

    global file_memory
    file_size = os.path.getsize(img_file)
    file_name = img_file
    relax(TIME_LOCK)

    print("Image Name: " + str(file_name))
    print("Image size: " + str(file_size))
    relax(TIME_LOCK)
    
    try:
        if (file_size > MAX_WORKSPACE_SIZE):
            if not img_file in file_memory:
                relax(TIME_LOCK)
                shutil.copy2(str(img_file), './archives/workspace/')
                file_memory.append(img_file)
            
                file = img_file.split("/")[-1]
                file = clean_filename(file)
                file_name = './archives/workspace/' + file
                print("Image is very large should be verified by the user")
                print("Path: " + file_name)

        if (file_size < MIN_IMAGE_SIZE):
            if not img_file in file_memory:
                relax(TIME_LOCK)
                shutil.copy2(str(img_file), './archives/workspace/')
                file_memory.append(img_file)
            
                file = img_file.split("/")[-1]
                file = clean_filename(file)
                file_name = '../archives/workspace/' + file
                print("Image is very small it is an Icon")
                print("Path: " + file_name)

        if (file_size > MIN_IMAGE_SIZE):
            global current_url
            print("Image is perfect")
            print("Path: " + file_name)
            relax(TIME_LOCK)
            dump_html(str("."+file_name), str(img_src))
    except:
        pass


def format_url(url):
    try:
        from urllib.parse import urlparse
        url = urllib.parse.unquote(url)
    except Error as e:
        x_print(e)
    return url


def open_web(url):  # first import the module
    webbrowser.open(url)


def format_title(title, ext):
    try:
        from urllib.parse import urlparse
        title = urllib.parse.unquote(title)
    except Error as e:
        x_print(e)

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
    global scraper_dictionary
    if i not in scraper_dictionary:
        scraper_dictionary.append(i)


def get_search_urls(query):
    search_urls = []
    import search as search_interface
    search_urls = search_interface.search_google(query)
    search_urls = search_interface.search_yahoo(query)
    search_urls = search_interface.search_bing(query)
    #print("Results found: " + str(len(search_urls)))
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

        urls_visited.clear()
        urls_buffer.clear()

        # Stats
        x_print(str(len(urls_buffer)) + " In the main buffer")
        x_print(str(len(urls_visited)) + " In the visited websites")
    else:
        # Load image-miner url global_memory
        load_memory()


def clean_memory():
    with open("urls", "w", encoding="utf-8") as file:
        file.write("")

    with open("urls_visited", "w", encoding="utf-8") as file:
        file.write("")

    with open("urls_image_buffer", "w", encoding="utf-8") as file:
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
        dictionnary_learn(i)


def dictionnary_learn(title):
    # Insert some word in the system dictionnary
    title = clean_text(str(title))
    for word in title.split(" "):
        scraper_dictionary.append(word)


def load_list(filename, urls_list):

    # read url file
    with open(filename, "r") as file:
        # reading each line"
        for line in file:
            url = clean_url(line)
            urls_list.append(url)

    clean_list = []
    for i in urls_list:
        if (len(i) <= MIN_LINK_SIZE):
            continue
        if (len(i) >= MAX_LINK_SIZE):
            continue
        if not i.find("http") >= 0:
            continue

        if not i in clean_list:
            clean_list.append(i)

    for i in clean_list:
        if i not in urls_list:

            if (len(i) <= MIN_LINK_SIZE):
                continue
            if (len(i) >= MAX_LINK_SIZE):
                continue

            urls_list.append(i)

    return urls_list


def dump_email_data(file_name, data):
    with open(file_name, "a") as file:
        x_print("filename: " + file_name)
        x_print("data: " + data)
        file.write(data + "\n")
        file.close()


def check_email(url):
    # EMAIL Extraction intelligence to be developped
    if (url.find("mailto:") >= 0):
        dump_email_data("./intelligence/email", url)
        url = urls_buffer[0]
        x_print("Email found adding to email list...")
    else:
        if (url.find("@") >= 0):
            dump_email_data("./intelligence/email_validation", url)


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

    # defining source and destination
    # paths
    files = os.listdir(src)

    # iterating over all the files in
    # the source directory
    for fname in files:
        # copying the files to the
        # destination directory
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
        'script',
        'css',
        'link',
        'javascript',
        # there may be more elements you don't want, such as "style", etc.
    ]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
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
    for char in word:
        # ^ is the references char
        if char in "â…[]?!@#$%&\':–©(){},.-:;|*/+\"\\~^–":
            word = word.replace(char, " ")
    word = trim(word)
    return word


def verify_link(link):
    if KEYWORDS_IN_LINK == 0:
        return True

    x_print("LINK VERIFICATION")
    global quality_score
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

                if score >= KEYWORDS_IN_LINK:

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


def is_pattern_in_query(pattern, q_bonus):
    global quality_score
    query = query_history[0] + query_boost
    query = clean_text(trim(query))

    if pattern in query:
        quality_score = quality_score + q_bonus
        print("Match: " + str(pattern))
        return quality_score
    if query.find(pattern) >= 0:
        quality_score = quality_score + q_bonus
        print("Match: " + str(pattern))
        return quality_score

    return quality_score


def title_score(title):
    try:
        global query_history
        quality_score = 0
        pattern = ""

        # First quick test the title test
        query = query_history[0] + query_boost

        if(not query in qb_boost):
            qb_boost.insert(0,query)
            save_memory()

        query = query.lower()
        query = clean_text(query)
        title = title.lower()

        print("\nTitle: " + str(title))
        print("Query: " + str(query))

        if not title in learned_keywords:
            learned_keywords.append(str(title))

        if not query in learned_keywords:
            learned_keywords.append(str(query))

        save_list(learned_keywords, "./intelligence/learned_keywords")

        for pattern in title.split(" "):
            pattern = clean_word(pattern)
            pattern = check_stop_words(pattern)

            if (pattern == None) or (pattern == "") or (pattern == " "):
                continue

            if (len(pattern) < MIN_STEM_SIZE):
                continue

            print(pattern)

            quality_score = is_pattern_in_query(pattern, 4)

            # check pattern with no number
            pattern = clean_numbers(pattern)

            quality_score = is_pattern_in_query(pattern, 3)

            stem_size = MIN_STEM_SIZE

            if len(pattern) > MIN_STEM_SIZE:
                stem_size = MIN_STEM_SIZE
            else:
                stem_size = len(pattern)-1

            try:
                # check root/stems of the word
                quality_score = is_pattern_in_query(pattern[0:stem_size], 2)
                quality_score = is_pattern_in_query(pattern[2:stem_size+2], 2)
                quality_score = is_pattern_in_query(pattern[4:stem_size+4], 2)
                quality_score = is_pattern_in_query(pattern[6:stem_size+6], 2)
            except:
                print("Error in title/querry matching")
                pass
    except Error as e:
        x_print(e)
        print("Error in title_score")

    return quality_score


def populate_signature_stems(pattern, content_signatures):
    signature = ""
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

    global query_history
    global quality_score

    # Only analyse the start of the document
    # First 1000 words to even out everyone
    # and not be affected by SPAMMERS
    if (url == None) or (text == None):
        return False

    x_print("\n\nSTARTING PAGE CONTENT VERIFICATION")
    x_print("TITLE: " + str(title))
    x_print("url: " + str(url))

    text_size = 0

    # pro-active cleaning processs
    text = clean_text(text)
    title = clean_text(title)

    if (len(text) > DB_TEXT_SIZE):
        text_size = DB_TEXT_SIZE
    else:
        text_size = len(text) - 1

    x_print("TEXT PREVIEW: " + str(text[0:text_size]))

    # Reset at 0 Quality score
    quality_score = 0

    # First quick test the title test
    title = title.lower()
    quality_score = title_score(title)

    pattern = ""
    words_in_text = 0

    content_signatures = []
    content_signatures_sl = []
    content_signatures_hf = []
    content_signatures_long = []

    x_print("\nTitle pre-test quality score (QS) " + str(quality_score))

    # Text pre-processing
    text = trim(text)

    # Clean the keywords in the document
    for pattern in text.split(" "):
        # if (quality_score>QUALITY_SCORE):
        #print("The Quality Score is: " + str(quality_score))
        # return True
        query = query_history[0] + query_boost
        query = clean_text(query)

        words_in_text = words_in_text + 1

        if words_in_text >= ANALYSIS_MAX_WORDS:
            break

        if len(pattern) < MIN_PATTERN_SIZE:
            continue

        pattern = pattern.lower()
        pattern = pattern.strip()
        pattern = str(pattern)

        pattern = clean_word(pattern)
        pattern = check_stop_words(pattern)

        if (pattern == None) or (pattern == ""):
            continue

        if len(pattern) >= LONG_KEYWORD_SIZE:
            if (not pattern in content_signatures_long):
                content_signatures_long.append(pattern)
                populate_signature_stems(pattern, content_signatures_long)
                populate_signature_stems(pattern, content_signatures)

        print("Pattern: " + str(pattern))
        # Populate the content_signatures with keywords
        # and stem of keywords for matching query
        # profile keywords for stat analysis
        # of web page

        try:

            if (len(pattern) >= MIN_WORD_SIZE):
                # Eliminate double
                if not pattern in content_signatures:
                    # x_print(pattern)
                    content_signatures.append(pattern)
                    populate_signature_stems(pattern, content_signatures)
                else:
                    if not pattern in content_signatures_sl:
                        content_signatures_sl.append(pattern)
                        content_signatures.append(pattern)
                        populate_signature_stems(
                            pattern, content_signatures_sl)
                        populate_signature_stems(pattern, content_signatures)

                    else:
                        if not pattern in content_signatures_hf:
                            content_signatures_hf.append(pattern)
                            content_signatures.append(pattern)
                            populate_signature_stems(
                                pattern, content_signatures_hf)
                            populate_signature_stems(
                                pattern, content_signatures)

        except Exception as e:
            print(e)
            input("Press enter to continue")

    x_print("TOTAL NUMBER WORDS: " + str(words_in_text))
    x_print("Unique signatures: " + str(len(content_signatures)))

    print(str(content_signatures))

    x_print("Highers (2) freq signatures: " + str(len(content_signatures_sl)))

    print(str(content_signatures_sl))

    x_print("Highers (3+) freq signatures: " + str(len(content_signatures_hf)))

    print(str(content_signatures_hf))

    x_print("long signatures: " + str(len(content_signatures_long)))

    print(str(content_signatures_long))

    # FINAL IN HOUSE ANALYSIS OF WEB PAGE CONTENT
    # TO EVALUATE IF WE SHOULD DOWNLOAD THE IMAGES
    words_in_text = 0
    for pattern in content_signatures:
        if words_in_text >= ANALYSIS_MAX_WORDS:
            break

        words_in_text = words_in_text + 1

        # if (quality_score>QUALITY_SCORE):
        #print("QS(Quality Score) is : " + str(quality_score))
        # return True

        pattern = pattern.lower()
        pattern = pattern.strip()
        pattern = str(trim(pattern))

        pattern = clean_word(pattern)
        pattern = check_stop_words(pattern)

        pattern = str(trim(pattern))

        if (pattern == None) or (pattern == "") or (pattern == " "):
            continue

        if len(pattern) < MIN_PATTERN_SIZE:
            continue

        quality_score = is_pattern_in_query(pattern, 2)

        # Check for stems
        if len(pattern) > MIN_STEM_SIZE:
            quality_score = is_pattern_in_query(pattern[0:MIN_STEM_SIZE], 3)
        if len(pattern) > MIN_STEM_SIZE+2:
            quality_score = is_pattern_in_query(pattern[2:MIN_STEM_SIZE+2], 1)
        if len(pattern) > MIN_STEM_SIZE*2:
            quality_score = is_pattern_in_query(
                pattern[MIN_STEM_SIZE:MIN_STEM_SIZE*2], 1)
        if len(pattern) > MIN_STEM_SIZE+4:
            quality_score = is_pattern_in_query(pattern[4:MIN_STEM_SIZE+4], 1)
        if len(pattern) > MIN_STEM_SIZE+6:
            quality_score = is_pattern_in_query(pattern[6:MIN_STEM_SIZE+6], 1)

    x_print("\nTITLE: " + str(title))
    x_print("URL: " + str(url))
    x_print("Quality score (QS) " + str(quality_score))

    if quality_score > QUALITY_SCORE:
        db_txt = ""
        if len(text) < DB_TEXT_SIZE:
            db_txt = text[0:len(text)]
        else:
            db_txt = text[0:DB_TEXT_SIZE]

        db_txt = clean_text(db_txt)
        insert_url_data(str(url), str(title), str(db_txt))

        global current_text
        current_text = db_txt

        # learn_keywords(str(url), str(title))
        # learn_keywords(str(url), str(db_txt))

    # EXTRA EVALUATION FOR HIGH FREQUENCY KEYWORDS
    for pattern in content_signatures_sl:

        pattern = pattern.lower()
        pattern = pattern.strip()
        pattern = str(trim(pattern))
        pattern = clean_word(pattern)
        pattern = check_stop_words(pattern)
        pattern = trim(pattern)

        if words_in_text >= ANALYSIS_MAX_WORDS:
            break
        if len(pattern) < MIN_PATTERN_SIZE:
            continue
        if (pattern == None) or (pattern == "") or (pattern == " "):
            continue
        try:
            if query.find(pattern) >= 0:
                quality_score = quality_score + 2
                print("MATCH: " + pattern)

            if query.find(pattern[0:MIN_STEM_SIZE]) >= 0:
                quality_score = quality_score + 2
                print("MATCH: " + pattern[0:MIN_STEM_SIZE])

            # Check for stems
            if len(pattern) > MIN_STEM_SIZE:
                quality_score = is_pattern_in_query(
                    pattern[0:MIN_STEM_SIZE], 3)
            if len(pattern) > MIN_STEM_SIZE+2:
                quality_score = is_pattern_in_query(
                    pattern[2:MIN_STEM_SIZE+2], 1)
            if len(pattern) > MIN_STEM_SIZE*2:
                quality_score = is_pattern_in_query(
                    pattern[MIN_STEM_SIZE:MIN_STEM_SIZE*2], 1)
            if len(pattern) > MIN_STEM_SIZE+4:
                quality_score = is_pattern_in_query(
                    pattern[4:MIN_STEM_SIZE+4], 1)
            if len(pattern) > MIN_STEM_SIZE+6:
                quality_score = is_pattern_in_query(
                    pattern[6:MIN_STEM_SIZE+6], 1)

        except:
            print("ERROR in matching process")
            pass

    x_print("\nTEXT TOTALLY CLEANED")
    x_print("IN HOUSE EVALUATION BASED ON KEYWORDS")
    x_print("IN COMPLETED...")
    x_print("PREPARING THE RESULTS...")
    title = trim(title)
    x_print("TITLE: " + str(title))
    x_print("URL: " + str(url))
    if len(text) > DB_TEXT_SIZE:
        x_print(text[0:DB_TEXT_SIZE]+" [...]")
        #x_print("PARTIAL TEXT PRESENTED")
        #x_print("THE TEXT IS TOO LARGE\n")
    else:
        x_print(text)
        #x_print("COMPLETE TEXT PRESENTED\n")

    x_print("")
    x_print("RESULTS")
    x_print("TITLE: " + title)
    x_print("URL: " + url)
    x_print("DB CONTENT: " +
            text[0:text.find(" ", text.find(" ", DB_TEXT_SIZE))])

    global query_size
    x_print("FINAL QUALITY SCORE (QS) " + str(quality_score))

    CQS = calculate_CQS(query_size, words_in_text)
    x_print("CALCULATED QUALITY SCORE (CQS) NEEDED IS " + str(CQS))

    if quality_score > CQS:
        x_print("URL PASSES THE QUALITY SCORE TEST: " + str(quality_score))
        relax(TIME_LOCK*2)

        # Add website root to be spidered
        root = get_root(current_url)
        if not root in urls_buffer:
            urls_buffer.append(root)
        
        # dump keywords for query boost
        learned_keywords.append(current_title)
        learned_keywords.append(current_text[0:200])
        
        new_query = query_history[0] + " " + current_title
        new_query = clean_text(new_query)
        qb_boost.insert(0,new_query)
        save_memory()
        #for i in db_txt.split(" "):
        #    QB_keywords.append(i)

        return True

    x_print("URL FAILED THE QUALITY SCORE TEST: " + str(quality_score))
    relax(TIME_LOCK*2)
    return False


def calculate_CQS(query_size, words_in_text):
    CQS = 0
    WIT = words_in_text / 100
    IS = QUALITY_SCORE + WIT / query_size 
    if IS > (QUALITY_SCORE*2):
        CQS = QUALITY_SCORE * 2 - query_size
    else:
        CQS = IS
    return CQS


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
    global scraper_dictionary
    global save_count
    global url_count
    global img_count

    # check_media(url)

    x_print("\nPROCESSING url extraction process\nurl: " + url)
    soup = BeautifulSoup(html, "html.parser")

    for link in soup.find_all("a"):
        try:
            link = link.get("href")
            link = fix_link(link, url)

            print(link)

            # if (verify_url_with_query(link)):
            if not link in urls_buffer:
                urls_buffer.append(link)
        except Error as e:
            x_print(e)
    return urls_buffer


def save_html(html):
    import uuid
    filename = str(uuid.uuid4())

    with open("./html/"+filename+".html", "w") as file:
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


def check_m3u8(html):
    check_pattern("src='(.*?).m3u8'/>", html)


def fix_link(link, root_url):
    if link == None:
        return None
    
    root = get_root(root_url)

    if (link.find("http") >= 0):
        return link
    
    if(link[0:3] == "../"):
        # Dont try this without
        # adult supervision :)
        folder = root_url.split('/')
        for i in folder:
            new_guess = new_guess + "/" + i + "/"
            link = new_guess
            print(link)
            get_image(link)
        return None
    
    if(link[0:2] == "//"):
    
        if(len(link) == 2):
            link = root_url
        link = "https:" + str(link)
        return link

    if(link[0:1] == "/"):
        link = root + str(link)
        return link
    
    return link


def get_root(url):
    end_of_url = url.find('/', 12)
    root = url[0:end_of_url]
    return root

# Hacking time :)
# This is not recommended...


def hacking_fix(link):
    # Hacking time
    guess_url = "https:" + link
    print("Second url guess: " + guess_url)
    result = check_media(guess_url)
    link = "http:" + link

# Hacking time :)
# This is not recommended...
# If you are beginner in programming...
# What the hell lets try anyway...
# Will try to figure out the bug later :)


def hack_fix_again(link, root_url, guess_url):
    print("Can't determine url will hack the url...")
    print("First url guess: " + guess_url)
    result = check_media(guess_url)

    if (not result):
        guess_url = root_url + str(link)
        print("Second url guess: " + guess_url)
        result = check_media(guess_url)


def clean_text(text):
    text = text.lower()
    text = text.replace("\xa0", "")
    text = text.replace("\'", "'")
    text = text.replace("\\'", "'")
    text = text.replace("  ", " ")
    text = text.replace("-", " ")
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = text.replace("\n", " ")
    text = text.replace("\"", " ")
    text = text.replace("\'", " ")

    while text.find("\n") >= 0:
        text = text.replace("\n", " ")

    while text.find("\t") >= 0:
        text = text.replace("\t", " ")

    while text.find("  ") >= 0:
        text = text.replace("  ", " ")

    new_clean_text = ""
    for i in text.split(" "):
        word = clean_word(i)
        new_clean_text = new_clean_text + " " + i

    new_clean_text = trim(new_clean_text)

    return new_clean_text

# this function extract urls or img from a url
# it returns a list of urls or images tags


def extract_images(url, html_file):
    # Images stats
    numLink = 0

    global img_count
    global urls_image_buffer

    x_print("\nPROCESSING image tags extraction: \nURL: " + url + "\n")
    x_print("Creating soup object...")

    soup = BeautifulSoup(html_file, "html.parser")

    try:
        x_print("STARTING IMAGE EXTRACTION")
        soup_memory = soup.find_all("img")
        for link in soup.find_all("img"):
            try:
                numLink = numLink + 1
                link = link.get("src")

                if (link == None):
                    continue
                else:
                    link = fix_link(link, url)
                    if not link in urls_image_buffer:
                        try:
                            result = verify_url_basic_check(link)

                            if result:
                                check_email(link)

                                result = check_media(link)

                                if result == None:
                                    continue

                                # Slow down or we will

                                if not link in urls_visited:
                                    urls_visited.append(link)
                                if not link in urls_image_buffer:
                                    urls_image_buffer.append(link)
                            else:
                                print("Url failed basic test...")
                                continue

                            # Double TIME_LOCK
                            relax(TIME_LOCK)
                        except Error as e:
                            x_print(e)
                            continue
            except Error as e:
                x_print(e)
    except Error as e:
        x_print(e)
        print("Error in IMAGE EXTRACTION MAIN FRAME")
        for i in soup_memory:
            try:
                result = check_media(i)
            except:
                pass

    # Double TIME_LOCK
    relax(TIME_LOCK)
    return urls_visited


def save_list(urls, file_name):
    # write url in visited site file
    if urls == None:
        return False

    # Clean the file before inserting the valuesss
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("")
        file.close()

    clean_memory = []
    with open(file_name, "a", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                if not url in clean_memory:
                    file.write(url + "\n")
                    clean_memory.append(url)
        file.close()
        urls = clean_memory
    return urls


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

    for stop_url_keyword in stop_urls:
        try:
            stop_url_keyword = stop_url_keyword.replace("\n", "")
            #print("Checking: " + str(stop_url_keyword))
            if (url.find(str(stop_url_keyword)) >= 0):
                print("URL STOP KEYWORD FOUND: " + str(stop_url_keyword))
                return False
        except Error as e:
            x_print(e)
            return False
    return True


def verify_url_basic_check(url):
    if (url == None):
        return False
    if (len(url) < MIN_LINK_SIZE):
        return False
    if (len(url) > MAX_LINK_SIZE):
        return False
    else:
        return True


def load_stop_urls():
    global stop_urls
    x_print("LOADING STOPLIST")
    file = open("./intelligence/stop_urls", "r")
    stop_urls = file.readlines()


def load_profile():
    global stop_urls
    x_print("LOADING USER PROFILE")
    file = open("profile", "r")
    smart_user_profile = file.readlines()
    return smart_user_profile


def load_profile():
    global stop_urls
    smart_user_profile = load_profile()
    return smart_user_profile


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
    return check_media(url)


filename = str(uuid.uuid4())


def dump_html(img, img_src):
    
    global current_title
    global current_url
    global current_text
    global filename

    if (True):
        html = '<div><br><br><center><a href="' + \
            img + '"><img src="' + img + '" width="50%" height="auto" /></a></center><center><center><br><b>' + current_title + '</b></center><a href="' + \
            current_url + '">' + current_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + current_img_keywords + " [...] " + '</center><center><b>TEXT WEBPAGE:</b>' + current_text[0:200] + " [...] " + '</center><center><a href="' + \
            img + '">' + img_src + '</a></center><div><br><br><br><hr>'

        f = open("./interface/"+filename+".html", "a")
        f.write(str(html))
        f.close()

        html = '<center><div align="center" style="  \
            ;display: inline-block;width: 300;height:  \
                auto;valign:middle;"><a href="' + img + '"><img style="width:300;height:auto;" border="1" src="' + img + '"/></a></div></center>'
        f = open("./interface/main-" + filename + ".html", "a")
        f.write(str(html))
        f.close()

def intro_dump(filename):
    
    global done

    if (True):
        html = '<link rel="stylesheet" type="text/css" href="../archive/interface/style.css" media="screen" /><div id="main">'
        f = open("./interface/main-" + filename + ".html", "a")
        f.write(str(html))
        f.close()
        done = True

def trim(text_section):
    if text_section == None:
        text_section="Amazing images fractals"    
    text_section = text_section.strip()
    return text_section

def prepare_keywords_for_database(title):

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
                if not url in clean:
                    url = trim(url)
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
    url = url.lower()
    
    if (title == None):
        title = ""

    title = title.lower()
    
    if (text == None):
        text = ""
    
    text = text.lower()
    return url, title, text

def get_html_textual_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    text_in_html = soup.get_text()
    text_in_html = clean_text(text_in_html)
    return text_in_html


def shuffle_list(list):
    import random
    x_print("SHUFFLING DE LIST")
    x_print("sneaky random approche pattern...")
    # Random URL search path
    # We may hit the jackpot
    random.shuffle(list)
    relax(TIME_LOCK)
    random.shuffle(list)
    relax(TIME_LOCK)
    random.shuffle(list)
    x_print("SHUFFLING...")
    x_print("\nAND TAKING A BREAK...")
    relax(TIME_LOCK)


def url_verification(url):
    x_print("STARTING URL VERIFICATION")
    result = check_url(url)
    if (not result):
        return False

    result = verify_url_basic_check(url)

    if (result == True):
        result = check_stop_words_in_urls(url)
    else:
        x_print("URL VERIFICATION FAILED - IN BASIC CHECK")
        x_print("URL: " + str(url))
    return result


def close_loop():

    global save_count
    global urls_buffer

    print("SAVE COUNTER IS AT " + str(save_count))

    if (SAVE_COUNT < save_count):
        print("SAVE COUNTER IS AT THE LIMIT")
        print("CLEANING BUFFERS")
        urls_buffer = clean_up_buffer(urls_buffer)

        print("SAVE URLS")
        save_memory()
        save_count = 0

        #src = "./archives/workspace/"
        #trg = "./media/"
        #save_to_archive(src, trg)
        shuffle_list(urls_buffer)


def first_check(url):
    global urls_buffer
    global current_url
    global save_count

    current_url = url  # = format_url(url)
    save_count = save_count + 1

    result = url_verification(url)

    if (result == False):
        x_print("\nURL VERIFICATION FAILED - STOP WORD in URL")
        x_print("URL: " + str(url))
        x_print("FIRST CHECK FAILED...")
        relax(TIME_LOCK)
        return result

    x_print("\nFIRST URL VERIFICATION PASSED...")
    result = verify_link(url)

    if (not result):
        x_print("\nSECOND URL VERIFICATION FAILED...")
        x_print("FIRST CHECK FAILED...")
        relax(TIME_LOCK)
        shuffle_list(urls_buffer)
        return result
    else:
        x_print("\nSECOND URL VERIFICATION PASSED...")
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
    
    current_url = url
    current_title = title
    current_text = text

    if (DOWNLOAD_HTML == "ON"):
        save_html(html)
        relax(TIME_LOCK)

    return result


def spider(url, html):

    global urls_buffer
    global urls_visited
    global urls_image_buffer

    urls_buffer = extract_urls(url, html)
    urls_image_buffer = extract_images(url, html)

    if (url in urls_buffer):
        urls_buffer.remove(url)

    if (not url in urls_buffer):
        urls_visited.append(url)

    shuffle_list(urls_buffer)

    return True


def get_webpage(url):
    
    global url_count
    page = None

    try:
        page = requests.get(str(url), headers={
            'User-Agent': ua.random}, timeout=20)
        url_count = url_count + 1
        if (url in urls_buffer):
            urls_buffer.remove(url)
    except:
        pass
    
    relax(TIME_LOCK)
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
    global urls_image_buffer
    global urls_visited

    global scraper_dictionary
    global learned_keywords
    global query_history

    global current_url
    global current_title
    global current_text
    global current_html

    print("Load memory")
    load_memory()

    print("Cleaning buffers")
    # Pro-active clean up process
    urls_buffer = clean_up_buffer(urls_buffer)

    x_print("Starting image mining process...\n")
    x_print("Loading the memory...\n")
    url = 'file:///home/linux/Bureau/Programmation/image-miner-X/interface'
    open_web(url)

    for url in urls_buffer:
        print_loop_info(url)
        result = first_check(url)

        if (not result):
            close_loop()
            continue

        try:

            page = get_webpage(url)
            if page == None: 
                continue

        except Error as e:
            x_print(e)
            print("ERROR - in get_webpage Requests")
            close_loop()
            continue

        try:
            result = read_evaluate_learn(url, page.text)
        except Error as e:
            x_print(e)
            print("ERROR - in read_evaluate_learn NLP section")
            close_loop()
            continue

        try:
            if page == None: 
                continue

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
                learned_keywords.append(keywords)
                save_list(learned_keywords,"./intelligence/learned_keywords")

            close_loop()

        except Error as e:
            x_print(e)
            print("ERROR in closing loop process")
            close_loop()
            continue

# Optional request object


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


def main():
    # Start image spider/miner program
    x_print("Start image-miner program")
    x_print("LOADING URLS")
    load_stop_urls()

    x_print("LOADING LISTS")
    load_stop_words()

    x_print("INITIATION OF THE SPIDER/SCRAPER")
    init_program()

    x_print("START MINER")
    start_image_miner()


# Entry point
main()
