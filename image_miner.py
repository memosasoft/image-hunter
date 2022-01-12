
#!/usr/bin/env python
import configparser
import datetime  # needed to create unique image file name
import mimetypes  # needed for download functionality
import shutil  # to save it locally
import sqlite3
import time  # needed to create unique image file name
from sqlite3 import Error

# Importing Necessary Modules
import urllib.request
from urllib.request import URLError, HTTPError
import requests  # to get image from the web
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search

# Session url and img global_memory
global_memory = []
image_link_memory = []
url_global_memory = []

img_count = 0
url_count = 0
save_count = 0

text_quality_score = 0

# Program url buffers
urls_buffer = []  # long-term buffer =
urls_visited = []  # visited_links
urls_image_buffer = []

# future proxy developments
list_proxies = []
list_of_working_proxies = []

# idea/prototype
smart_user_profile = []

# search urls from google
search_urls = []
scraper_dictionary = []

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
QUALITY_SCORE = float(configuration.get('CONFIG', 'QUALITY_SCORE'))
KEYWORDS_IN_LINK = int(configuration.get('CONFIG', 'KEYWORDS_IN_LINK'))

MIN_LINK_SIZE = int(configuration.get('CONFIG', 'MIN_LINK_SIZE'))
MAX_LINK_SIZE = int(configuration.get('CONFIG', 'MAX_LINK_SIZE'))
MIN_WORD_SIZE = int(configuration.get('CONFIG', 'MIN_WORD_SIZE'))
MIN_STEM_SIZE = int(configuration.get('CONFIG', 'MIN_STEM_SIZE'))

QUERY_BOOST  = str(configuration.get('CONFIG', 'QUERY_BOOST'))

ANALYSIS_MAX_WORDS = int(configuration.get('CONFIG', 'ANALYSIS_MAX_WORDS'))
MIN_IMAGE_SIZE = int(configuration.get('CONFIG', 'MIN_IMAGE_SIZE'))
DOWNLOAD_OPTION = int(configuration.get('CONFIG', 'DOWNLOAD_OPTION'))
DOWNLOAD_HTML = int(configuration.get('CONFIG', 'DOWNLOAD_HTML'))

DEBUG_CONSOLE = str(configuration.get('CONFIG', 'DEBUG_CONSOLE'))
DEBUG_LOG = str(configuration.get('CONFIG', 'DEBUG_LOG'))
DB_TEXT_SIZE = int(configuration.get('CONFIG', 'DB_TEXT_SIZE'))

SAVE_COUNTER = int(configuration.get('CONFIG', 'SAVE_COUNTER'))
DIG_FOR_URLS = "ON"

TIME_LOCK = 2
DIRECTORS_PICKS = 300000

media_files = ",psd,webm,ogg,wav,zip,rar,7z,bin,mp4,mp3,mov,mpeg,tiff,ico,jpg,gif,png,bmp"
query_boost = ",photo,image,picture,gallery,resolution,5k,HD,wallpaper,hd,4k,art,high,definition,illustration,collection"

def init_program():
    # Query global_memory self-learning object  
    load_global_memory_url()

    # Stats
    x_print(str(len(urls_buffer)) + " in the main buffer")
    x_print(str(len(urls_visited)) + " in the visited websites")

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
    x_print("Images and media saved\n")
    
    # User system-interaction
    x_print("SETUP PROCESS")
    x_print("Starting setup process and cleanup")
    setup_process(user_input)
    
    query = input("What type of images you want to spider?")
    x_print("\nSEARCH MODULE\n")
    x_print("Connecting to search engines")
    x_print("Google, Yahoo and Bing")
    
    # add the user query to the user queries list
    # add also to the query_history list    x_print("\nNEW SELF-LEARNING FEATURE - AI")
    x_print("\nLoading user query global_memory for system self-learning purposes")    
    query_history = load_query_history()
    query_history.insert(0,query)
    query_history = save_query_history()

    # QUERY BOOST - special functionality to get
    # better image related searches from main 
    # search engine : Google, Yahoo and Bing
    query = clean_query(query)

    if QUERY_BOOST == "ON":  
        search_mining_prototype(query)
    else:
        search_urls = get_search_urls(query.strip())
        insert_search_results_in_buffer(search_urls)

def extract_info_from_url(url):
    info = ""
    url_clean = url.replace(".", " ")
    url_clean = url_clean.replace(".", "_")
    url_clean = clean_url(url_clean)
    for i in url_clean.split("/"):
        i = clean_word(i)
        i = clean_numbers(i)
        i = clean_word_from_stop_list(i)
        info = info + " " + i

    info = clean_text(info)
    x_print("Concepts from the url: ")    
    x_print("Url: " + str(trim(info)))
    return info

def clean_query(query):

    item = ["  ", ",", ".",
        "-","+","{","}","[","]"]

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

def search_mining_prototype(query):
    x_print("My new Simple Image-Miner uses")
    x_print("Experimental QUERY_BOOST")
    
    # Normalize the query string
    original_q = query.lower()
    prototype_rq = query.lower()
    query = query.lower()

    # Prepare query with extra image termes
    query = query + " " + query_boost
    query = clean_query(query)
     
    x_print("\nQUERY_BOOST ACTIVATED: ")
    x_print("\nSending queries")
    
    # PROTOTYPE EXTRA Random QUERY 1 and 2
    prototype_rq1 = prototype_rq + " unique archive images art rare royalty free artist"
    prototype_rq2 = prototype_rq + " amazing galleries photo surprizing download digital"
    prototype_rq3 = prototype_rq + " digital rare strange weird amazing free digital"

    # Add extra image related search terms to enhance
    # the search results the list is in config.env
    search_urls = get_search_urls(query.strip())
    #x_print("Original SEARCH 1: " + str(len(search_urls)))
    
    list_rq1 = get_search_urls(prototype_rq1.strip())
    #x_print("GET SEARCH 1: " + str(len(list_rq1)))   

    list_rq2 = get_search_urls(prototype_rq2.strip())
    #x_print("GET SEARCH 2: " + str(len(list_rq2)))   

    list_rq3 = get_search_urls(prototype_rq3.strip())
    #x_print("GET SEARCH 3: " + str(len(list_rq3)))   

    list_rq4 = get_search_urls(original_q.strip())
    #x_print("GET SEARCH 3: " + str(len(list_rq3)))   

    #x_print("Initial search result")
    #print("FIRST LIST: " + str(len(search_urls)))
    search_urls = add_list_to_list(search_urls, list_rq1)
    #x_print("AFTER ADDIND THE FIRST Result Set: " + str(len(search_urls)))   

    #print("SECOND LIST: " + str(len(search_urls)))
    search_urls = add_list_to_list(search_urls, list_rq2)
    #x_print("AFTER ADDIND THE SECOND Result Set: " + str(len(search_urls)))   

    #print("THIRD LIST: " + str(len(search_urls)))
    search_urls = add_list_to_list(search_urls, list_rq3)
    #x_print("AFTER ADDIND THE THIRD Result Set: " + str(len(search_urls)))   
    search_urls = add_list_to_list(search_urls, list_rq4)

    #print("FOURTH LIST: " + str(len(search_urls)))
    # System interaction with user
    x_print("We got: " + str(len(search_urls)) + " urls to mine\n")
    x_print("Thank you Google, Yahoo and Bing...")
    # Inserting urls at the beginning of the url list
    x_print("\nAdding the search urls to the begining of search buffer...")
    insert_search_results_in_buffer(search_urls)
    
def add_list_to_list(list_to_grow, list_to_add):
    result_counter = 0
    for i in list_to_add:
        if not i in list_to_grow: 
            list_to_grow.append(i)
            print(str(result_counter) + " : " + i)
            result_counter = result_counter + 1
    return list_to_grow

def insert_search_results_in_buffer(search_urls):
    # Main url buffer
    global urls_buffer
    
    for i in search_urls:

        if (len(i)<=MIN_LINK_SIZE):
            continue
        if (len(i)>=MAX_LINK_SIZE):
            continue
        if not i.find("http")>=0:
            continue
        
        if not i in urls_buffer:
            urls_buffer.insert(0,str(i))    

    save_global_memory_urls()

# Self learning object to gain ai from
# user interaction - Prototype
def load_query_history():
    global query_history
    x_print("LOADING query pattern history")
    with open("./intelligence/query_history", "r") as file:
        # reading each line"
        for line in file:
            line = clean_text(line)
            query_history.append(line)
    return query_history

def save_global_memory_urls():
    global query_history
    global urls_buffer
    global urls_visited
    global scraper_dictionary
    global learned_keywords
    global urls_image_buffer
      
    x_print("Saving into global_memory")  
    urls_buffer = save_urls(urls_buffer, "urls")
    urls_visited = save_urls(urls_visited, "urls_visited")
    learned_keywords = save_urls(learned_keywords, "./intelligence/learned_keywords")
    scraper_dictionary = save_urls(scraper_dictionary, "./intelligence/scraper_dictionary")
    urls_image_buffer = save_urls(urls_image_buffer,"urls_image_buffer")

def load_global_memory_url():
    global query_history
    global urls_buffer
    global urls_visited
    global scraper_dictionary
    global learned_keywords
    
    urls_visited = get_urls("urls_visited", urls_visited)
    urls_buffer = get_urls("urls_image_buffer", urls_image_buffer)
    learned_keywords = get_urls("./intelligence/learned_keywords", learned_keywords)
    scraper_dictionary = get_urls("./intelligence/scraper_dictionary", scraper_dictionary)
   
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

def insert_data(url, keywords, filename, original_name):
    try:
        db_file = "./intelligence/data-miner.db"
        conn = sqlite3.connect(db_file)
             
        if (keywords == None):
            keywords = "empty"
        if (original_name == None):
            original_name = "empty"   
        
        c = conn.cursor()
        c.execute("INSERT INTO image (url, keywords, filename, file_id) VALUES (?,?,?,?)",
                  (url, keywords, filename, original_name))
        conn.commit()
        
        conn.close()
    except Error as e:
        x_print(e)

def check_keywords_in_urls(url):
    global query_history

    for key in query_history[0].split(" "):
        key = str(key).lower()
        url = str(url).lower()
        if len(key)>2:
            if url.find(key)>=0: 
                return True
    return False  
def insert_url_data(url, title, text):
    try:
        text = ""
        db_file = "./intelligence/data-miner.db"
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("INSERT INTO url (url, title, text) VALUES (?,?,?)",
                  (url, title, text))
        conn.commit()
        conn.close()
    except Error as e:
        x_print(e)

def check_media(url):
    url = url.lower()
    # There is a small bug with the end of the file
    # this function should clean de url
    for media_ext in media_files.split(","):
        if url.find(str("."+media_ext.strip())) >= 0:
            download(url)
            break

def download(url):
    global global_memory
    global img_count
    
    save_path = './media/'
    ext = url.split(".")[-1]
    file =  url.split("/")[-1]
    
    if url not in global_memory:
        try:                
            # Download process
            import wget
            
            wget.download(url, save_path + file)
            relax(TIME_LOCK) 

            x_print("URL : " + url)
            urls_image_buffer.append(url)

            x_print("Download completed")
        except:
            x_print("Error downloading")
            x_print("URL causing error is: " + url)
            if(1 < img_count):
                img_count = img_count -1
            
    if(url.find(".mp4") <= 1 and url.find("mp3") <= 1):
        archive_filename = "./intelligence/ARCHIVE_MEDIA.M3U"

    if(url.find(".mp3") > 0):
        archive_filename = "./intelligence/ARCHIVE_MP3.M3U"

    if(url.find(".mp4") > 0):
        archive_filename = "./intelligence/ARCHIVE_MP4.M3U"
    
    EXTINF_text = ""
    title = file
    
    with open(archive_filename, "a") as file:        
        EXTINF_text = "#EXTINF:-1, " + title
        file.write(EXTINF_text + "\n")        
        file.write(url + "\n")       
        file.close()
        global_memory.append(title)

def build_title_from_filename(url):
    ext = url.split(".")[-1]
    file = url.split("/")[-1]
    title = format_title(str(file), str(ext))
    return title

def get_size_img_check(file_name_and_location):
    import os
    file_size = os.path.getsize(file_name_and_location)

    if (file_size>DIRECTORS_PICKS):
        shutil.move(str(file_name_and_location), './directors_picks/')                                   

    if (file_size<MIN_IMAGE_SIZE):
        shutil.move(str(file_name_and_location), './junk/')                                   
    pass

def format_title(title, ext):    
    try:
        from urllib.parse import urlparse
        title = urlparse.unquote(title)
    except:
        pass

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
    x_print("STARTING SETUP PROCESS")
    if (user_input == "y"):
        clean_url_global_memory_files()
    
        # clean images folders
        delete_media_in_folders("full")
        delete_html_in_folders()    
        
        global urls_visited
        global urls_buffer
        
        # Load image-miner url global_memory
        load_global_memory_url()

        # Stats
        x_print(str(len(urls_buffer)) + "In the main buffer")
        x_print(str(len(urls_visited)) + "In the visited websites")
        
def clean_url_global_memory_files():
    with open("urls", "w", encoding="utf-8") as file:
        file.write("")
        
    with open("urls_visited", "w", encoding="utf-8") as file:
        file.write("")
        
def delete_media_in_folders(switch):
    import os
    import os.path

    my_path = "./media/"
    for root, dirs, files in os.walk(my_path):
        for file in files:
            os.remove(os.path.join(root, file))

def delete_html_in_folders():
    import os
    import os.path
    my_path = "./data/"
    for root, dirs, files in os.walk(my_path):
        for file in files:
            os.remove(os.path.join(root, file))

def learn_from_scraping(url, html):
    # Extract Title
    # Extract section of text
    # Learn title of document like a groupe 
    # off concepts with a relation ship between
    # them this info will be used later once
    # the system learns de vocabulary
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string
    learn_keywords(url, html, title)
    prepare_data_and_insert_in_database(url, html, title)
    
def clean_urlx(url_keywords):
    url_keywords = url_keywords.replace("https", "")
    url_keywords = url_keywords.replace("http", "")
    url_keywords = url_keywords.replace("html", "")
    url_keywords = url_keywords.replace("php", "")
    url_keywords = url_keywords.replace("www", "")
    url_keywords = url_keywords.replace("com", "")
    return url_keywords

def learn_keywords(url, html, title):
    title = clean_text(str(title))
    url_keywords = extract_info_from_url(url) 
    final_string = clean_text(title + " " + url_keywords)
    learned_keywords.append(trim(final_string))
    load_title_into_dictionary(final_string)

def load_title_into_dictionary(title):
    for i in title.split(" "):
        i = clean_word(i)
        i = clean_word_from_stop_list(i)
        dictionnary_learn(i)

def prepare_data_and_insert_in_database(url, html, title):
    text = get_text(html)
    while text.find("\n")>=0:
        text = clean_text(text)
    
    text = clean_text(str(text))
    # Make sure there is enoughs text for the database
    end = 0
    if len(text)<DB_TEXT_SIZE:
        end = len(text)
    else:
        end = DB_TEXT_SIZE
    
    print("TITLE: " + str(title))
    print("URL: " + str(url)) 
    print("TEXT: " + str(text[0:end]))
    # Learn from url and title

    # Insert url in database with information
    insert_url_data(url, title, text[0:end])

def dictionnary_learn(title):
    # Insert some word in the system dictionnary
    title = clean_text(str(title))
    for word in title.split(" "):
        scraper_dictionary.append(word)

def evaluate_url(url, html):
    # check stop words in url
    if not check_stop_words_in_urls(url):
        return False

    learn_from_scraping(url, html)
    # Extract highest frequency keywords
    # verify stop_urls terms
    # verify keywords in url
    # verify page content
    # Then make a decision if we should spider it
    # and extract information from children's
    return True

def get_urls(filename, urls_list):

    # read url file
    with open(filename, "r") as file:
        # reading each line"
        for line in file:
            url = clean_url(line)
            urls_list.append(url)

    clean_list = []
    for i in urls_list:
        if (len(i)<=MIN_LINK_SIZE):
            continue
        if (len(i)>=MAX_LINK_SIZE):
            continue
        if not i.find("http")>=0:
            continue
        
        if not i in clean_list:
            clean_list.append(i)
    
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
    # EMAIL Extraction intelligence to be developped
    if (url.find("mailto:") >= 0):
        dump_email_data("./intelligence/email", url)
        url = urls_buffer[0]
        x_print("Email found adding to email list...")
    else:
        if (url.find("@") >= 0):
            dump_email_data("./intelligence/email_validation.txt", url)
            
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
    files=os.listdir(src)
    
    # iterating over all the files in
    # the source directory
    for fname in files:        
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(src,fname), trg)

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

def load_stop_list():
    global stop_words
    file = open("./intelligence/stop_list", "r")
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

def clean_word_from_stop_list(word):
    # preformating word
    if word in stop_words:
        return ""
    return word

def clean_word(word):
    for char in word:
        # ^ is the references char
        if char in "()(){},.-:;|*/+\"\\~^–":
            word = word.replace(char, " ")
    word = trim(word)
    return word

def verify_link(link):
    global query_history
    global text_quality_score

    x_print("LINK VERIFICATION")
    text_quality_score = 0

    for pattern in query_history[0].split(" "):
        link = link.lower()
        pattern = pattern.lower()
        
        # FIRTS CONTACT WITH INTELLIGENCE 
        # Look for mathematical stem or root of word
        if (len(pattern)<MIN_STEM_SIZE):
            stem = pattern[0:len(pattern)]
        else:
            stem = pattern[0:MIN_STEM_SIZE]
        
        x_print("Needed stem for partial match: " + stem)
        
        if (link.find(stem) >= 0):

            x_print("MATCH pattern is " + pattern)

            if (len(pattern) > MIN_WORD_SIZE):
                text_quality_score = text_quality_score + 1

                if text_quality_score > KEYWORDS_IN_LINK-1:

                    x_print("ACCEPTED LINK - PATTERN MATCH SCORE : " + str(text_quality_score))
                    x_print("URL: " + link)
                    x_print("MATCHING KEYWORDS FOUND IN LINK - PASSED")

                    return True
            else:
                x_print("MATCH is canceled pattern is to small: MIN_WORD_SIZE")  
        else:
            x_print("NO MATCH")
            x_print("URL: " + link)
    
    x_print("NO MATCHING KEYWORDS FOUND IN LINK - FAILED")
    x_print("URL: " + link)
    x_print("WE SHOULD NO FOLLOW THIS ROAD")
    x_print("LETS KEEP ON MINING URLS TO GET IAMGES WE ARE LOOKING FOR")
    return False

def dig_for_urls(url):
    # DIG to find more URLs
    page = requests.get(str(url), headers={'User-Agent': ua.random}, timeout=105)  
    # page = requests.get(str(url), timeout=15)  
    urls_visited.append(url)

    if page.status_code == 200:          
        x_print("We got in... ")
        x_print("Extracting URL: " + str(url))
        x_print("DOWNLOAD IS SUCCESSFUL...")
        # Extracting the source code of the page.
        html_file = page.text     
        urls = extract_only_urls(url, html_file)

        for new_url in urls:
            print("adding URL: " + str(new_url))
            urls_buffer.append(str(new_url))

def verify_url_with_query(url):
    for word in query_history[0]:
        if url.find(word)>=0:
            return True;
    return False
    
def verify_page_content(url, title, text):
    
    # Only analyse the start of the document
    # First 1000 words to even out everyone 
    # and not be affected by SPAMMERS 
    if (url == None):
        return False
        
    x_print("STARTING PAGE CONTENT VERIFICATION")
    x_print("TITLE: " + str(title))
    x_print("Checking url: ")
    x_print("url: " + str(url))

    global query_history
    global text_quality_score
    # Clean numbers from text
    # text = clean_numbers(text)

    pattern = ""
    text_keywords = []
    text_keywords_sl = []
    words_in_text = 0
    
    # First quick test the title test
    title = title.lower()
    
    for pattern in title.split(" "):
        if pattern in query_history[0]:
            text_quality_score = text_quality_score + 1
    
    x_print("Title pre-test quality score (QS) " + str(text_quality_score)) 
    # Clean the keywords in the document
    for pattern in text.split(" "):
        if (text_quality_score>QUALITY_SCORE):
            return True
        words_in_text = words_in_text + 1
            
        pattern = pattern.lower()
        pattern = pattern.strip()
        pattern = str(pattern)
        pattern = clean_word_from_stop_list(pattern)
        
        # Populate the text_keywords with keeywords 
        # and stem of keywords for matching query 
        # profile keywords for stat analysys
        # of web page
        if (len(pattern) >= MIN_WORD_SIZE):
            # Eliminate double
            if not pattern in text_keywords:
                # x_print(word)
                text_keywords.append(pattern)
                if len(pattern) > MIN_STEM_SIZE:
                    text_keywords.append(pattern[0:MIN_STEM_SIZE])
            else:
                if not pattern in text_keywords_sl:
                    text_keywords_sl.append(pattern)
    
    x_print("TOTAL NUMBER WORDS: " + str(words_in_text))
    x_print("Unique keywords: " + str(len(text_keywords)))
    x_print("Highers freq keywords: " + str(len(text_keywords_sl)))  

    # FINAL IN HOUSE ANALYSYS OF WEB PAGE CONTENT
    # TO EVALUATE IF WE SHOULD DOWNLOAD THE IMAGES  
    for pattern in text_keywords:
        
        if (text_quality_score>QUALITY_SCORE):
            return True

        pattern = pattern.strip()
        pattern = pattern.lower()

        if pattern in query_history[0]:
            text_quality_score = text_quality_score + 1

        # Check for stems
        if len(pattern) > MIN_STEM_SIZE:
            if pattern[0:MIN_STEM_SIZE] in query_history[0]:
                text_quality_score = text_quality_score + 1

    x_print("TITLE: " + str(title))
    x_print("URL: " + str(url))
    x_print("Initial Quality score (QS) " + str(text_quality_score))
    
    # EXTRA EVALUATION FOR HIGH FREQUENCY KEYWORDS
    for pattern in text_keywords_sl:
        if (text_quality_score>QUALITY_SCORE):
            break

        pattern = pattern.strip()
        pattern = pattern.lower()

        if pattern in query_history[0]:
            text_quality_score = text_quality_score + 5
    
    x_print("TEXT TOTALLY CLEANED")
    x_print("IN HOUSE EVALUATION BASED ON KEYWORDS")
    x_print("IN COMPLETED...")
    x_print("PREPARING THE RESULTS...")
    x_print("TITLE: " + str(title))
    x_print("URL: " + str(url))
    x_print("------------------------")
    
    if len(text)>DB_TEXT_SIZE*2:
        x_print(text[0:DB_TEXT_SIZE*2]+" [...]")
        x_print("PARTIAL TEXT PRESENTED")
        x_print("THE TEXT IS TOO LARGE")
    else:
        x_print(text)
        x_print("COMPLETE TEXT PRESENTED")

    x_print("------------------------")
    x_print("RESULTS")    
    x_print("------------------------")
    x_print("TITLE: " + title)
    x_print("URL: " + url)
    x_print("DB CONTENT: " + text[0:text.find(" ", text.find(" ", DB_TEXT_SIZE))])
    
    learned_keywords.append(text[0:text.find(" ", DB_TEXT_SIZE)])
    text_quality_score = 0
    x_print("FINAL QUALITY SCORE (QS) " + str(text_quality_score))
    if text_quality_score > QUALITY_SCORE:
        x_print("URL PASSES THE QUALITY SCORE TEST: " + str(text_quality_score))
        x_print("IMAGES SHOULD BE GOOD LET DOWNLOAD THEM " + str(text_quality_score))
        return True
    x_print("URL FAILED THE QUALITY SCORE TEST: " + str(text_quality_score))    
    x_print("IMAGES SHOULD NOT BE DOWNLOADED " + str(text_quality_score))    
    return False

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
    
    x_print("\nPROCESSING url extraction process\nurl: " + url)
    soup = BeautifulSoup(html, "html.parser")
            
    for link in soup.find_all("a"):
        try:
            link = link.get("href")
            link = fix_link(link, url)

            print(link)    
            
            if (verify_url_with_query(link)):
               urls_buffer.append(link)
        except:
            pass                
    return urls_buffer

        
def check_pattern(pattern, html):
    import re
    vidlinks = re.findall(pattern, html) #find all between the two parts in the data
    #print(vidlinks[0] + ".m3u8") #print the full link with extension

    if (len(vidlinks)>0):
        with open("keywords", "a") as file:
            for rc in vidlinks:
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
    if (link.find("http")>=0):
        return link
    if(link[0:2] == "//"):
        if(len(link)==2):
            link = root_url
        link = "https:" + str(link)
    if(link[0:1] == "/"):
        link = root + str(link)
    return link

def get_root(url):
    end_of_url = url.find('/',12)
    root = url[0:end_of_url]
    return root

def clean_text(url_text):
    url_text = url_text.lower()
    url_text = url_text.replace("\xa0", "")
    url_text = url_text.replace("\'", "'")
    url_text = url_text.replace("\\'", "'")

    while url_text.find("\n")>=0:
        url_text = url_text.replace("\n", " ")
    
    while url_text.find("\t")>=0:
        url_text = url_text.replace("\t", " ")
    
    while url_text.find("  ")>=0:
        url_text = url_text.replace("  ", " ")

    new_clean_text = ""
    for i in url_text.split(" "):
        word = clean_word(i)
        new_clean_text = new_clean_text + " " + i

    return new_clean_text

def extract_only_urls(url, html):

    x_print("\nStarting SOUP\n")
    soup = BeautifulSoup(html, "html.parser")

    for links in soup.find_all("a"):

        try:
            link = links.get("href")
            if link in urls_visited:
                #x_print("Link has all ready been downloaded in visited list global_memory")
                continue
        except:
            pass
    
        # Check if the url is long enoughs to process
        x_print("____________________________________________")
        x_print("\nVERIFY size of url")
        x_print("URL: " + link)

        if (len(link) < MIN_LINK_SIZE):
            x_print("\ninvalid link length to small - FAILED")
            continue

        if (len(link) > MAX_LINK_SIZE):
            x_print("\ninvalid link length to long - FAILED")
            # 
            continue
        x_print("SIZE OF THE LINK - PASSED")
        x_print("Stop url list passed - PASSED")

        # Rebuild the site if the url root is missing
        if not link is None:
            root_path = ""
            if link.find("http") < 0:
                # get root https path
                root_path = fix_link(url, link)

                if not root_path in urls_buffer:
                    x_print("Adding root path\n" + root_path)
                    urls_buffer.append(root_path)

                if link[0] == "/":
                    link = root_path + link
                else:
                    link = root_path + "/" + link

        x_print("\nROOT PATH VERIFICATION - PASSED")
        x_print("URL: " + link)
        

        if verify_link(link):
            x_print("\nLink verification test - PASSED\n")
            x_print("URL: " + link)
            
            
            if not link in urls_buffer:
                print("Addinf url to urls_buffer to feed scraper-spider")
                print("Url: " + str(link))
                urls_buffer.append(link)                    
        else:
            continue

# this function extract urls or img from a url
# it returns a list of urls or images tags
def extract_images(url, html_file):
    # Images stats
    numLink = 0
    
    global img_count
    global image_link_memory
    x_print("\nPROCESSING image tags extraction: \nURL: " + url + "\n")
    x_print("Creating soup object...")
    soup = BeautifulSoup(html_file, "html.parser")
    x_print("STARTING IMAGE EXTRACTION")
    for link in soup.find_all("img"):
        try:            
            numLink = numLink + 1
            link = link.get("src")
    
            if (link == None):
                continue
            else:
                link = fix_link(link,url)
                if not link in image_link_memory:
                    try:
                        check_email(link)
                        download(link)

                        img_count = img_count + 1
                        urls_visited.append(link)
                        image_link_memory.append(link)
                        print("Image count: " + str(img_count) ) 
                    except:
                        continue
        except:
            continue

    return urls_visited

def save_urls(urls, file_name):
    # write url in visited site file
    if urls == None:
        return False
    
    global url_global_memory
    with open(file_name, "a", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                if not url in url_global_memory:
                    file.write(url + "\n")
                    url_global_memory.append(url)
        file.close()
    return urls 
    
def verify(url):
    if (url == None):
        return True
    if (len(url) < MIN_LINK_SIZE):
        return True
    if (len(url) > MAX_LINK_SIZE):
        return True
    if (url == None):
        return True
    else:
        return False

def get_extension(response):
    mtype = response.headers.get("Content-Type", "image/jpeg")
    mtype = mtype.partition(";")[0]

    if "/" not in mtype:
        mtype = "image/" + mtype

    if mtype in MIMETYPE_MAP:
        return MIMETYPE_MAP[mtype]

    exts = mimetypes.guess_all_extensions(mtype, strict=False)
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
    for stop_url in stop_urls:
        try:
            if (url.find(stop_url) >= 0):
                return False
            else:
                return True
        except:
           return False

def load_stop_urls():
    global stop_urls
    x_print("LOADING STOPLIST")
    file = open("./intelligence/stop_urls", "r") 
    stop_urls = file.readlines()

def load_profile():
    global stop_urls
    x_print("LOADING USER PROFIL")
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

def trim(text_section): 
    text_section = text_section.lstrip()
    text_section = text_section.strip()
    return text_section

def prepare_keywords_for_database(title):
    keywords = title.lower()
    for ix in stop_words:
        for iy in keywords.split(" "):
            if ix == iy:
                keywords = keywords.replace(ix, " ")
    return keywords
            
def clean_up_url_buffers(urls_buffer):
    clean = []
    for i in urls_buffer:
        if not i in clean:
            clean.append(i)
    urls_buffer = clean
    clean.clear()
 
def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.get_text()
    return title

def format_for_pattern_check(url, title, text):
    url = url.lower()
    title = title.lower()
    text = text.lower()
    return url, title, text

def get_html_textual_content(html):            
    soup = BeautifulSoup(html, 'html.parser')
    text_in_html = soup.get_text()
    text_in_html = clean_text(text_in_html)
    return text_in_html

def shuffle_list(list):
    import random
    x_print("SHUFFLING DE DECK...")

    # Random URL search path 
    # We may hit the jackpot
    random.shuffle(list)
        
def start_image_miner(): 
    global save_count
    global img_count
    global url_count
    global urls_buffer
    global urls_image_buffer
    global urls_visited

    x_print("Starting image mining process...\n")
    x_print("Loading the memory...\n")
    load_global_memory_url()
    page = ""
    for url in urls_buffer:
        
        x_print("STARTING URL EXTRACTION PROCESS")
            
        try:
            page = requests.get(str(url), headers={'User-Agent': ua.random})  
    
            # TEST
            # page, status, contentType = requests_hack(url
        except:
            print("Error in resquest unhandeled")
            relax(10)
            continue
        
        try:
            url_count = url_count + 1               
            x_print("URL count : " + str(url_count))
            x_print("Image count :" + str(img_count))
            x_print("Current URL :" + str(url)) 
        except:
            print("Error in stats")
        try:        
            title = get_title(page.text)
            text = get_html_textual_content(page.text)
            url, title, text = format_for_pattern_check(url, title, text)
            result = verify_page_content(url, title, text)
        except:
            print("Error in NLP section")
            continue
        
        try:        
        
            if (result):
                urls_buffer = extract_urls(url, text)
                urls_image_buffer = extract_images(url, page.text)
                urls_buffer.remove(url)
                urls_visited.append(url)
        except:
            print("ERROR in extraction process")
        
        try:  
            db_txt = ""
            keywords = prepare_keywords_for_database(title)
            keywords = clean_text(keywords)
            keywords = trim(keywords)

            db_txt = text[0:DB_TEXT_SIZE]
            
            if len(text) < DB_TEXT_SIZE:
                db_txt =  text[0:len(text)]   
            
            db_txt = clean_text(db_txt)
            db_txt = title + " " + keywords + " " + db_txt
            insert_url_data(str(url),str(db_txt), str(title))
            
            shuffle_list(urls_buffer) 
            
            learn_keywords(str(url),str(db_txt), str(title))
            clean_up_url_buffers(urls_buffer)
            clean_up_url_buffers(urls_visited)
            shuffle_list(urls_buffer)
            save_global_memory_urls()
        except:
            continue


# Extrae los correos de una única URL
def requests_hack(url):

    print ("Searching emails... please wait")

    count = 0
    listUrl = []

    req = urllib.request.Request(
            url, 
            data=None, 
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
    load_stop_list()

    x_print("INITIATION OF THE SPIDER/SCRAPER")
    init_program()

    x_print("START MINER")
    start_image_miner()

# Entry point
main()