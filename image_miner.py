#!/usr/bin/env python
import configparser
import datetime  # needed to create unique image file name
import mimetypes  # needed for download functionality
import shutil  # to save it locally
import sqlite3
import time  # needed to create unique image file name
from sqlite3 import Error

# Importing Necessary Modules
import requests  # to get image from the web
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search

urls_buffer = []  # program main url buffer
images_tags = []  # program main found url/link buffer

urls_links = []  # buffer
urls_visited = []  # visited_links
urls_extracted = []  # urls_session
total_links = 0

list_proxies = []
list_of_working_proxies = []

ua = UserAgent()
memory = []

# search urls from google
listUrl = []
image_urls = []

# keywords container for query and page content
content_keywords = []
query_keywords = []
m_keywords = []

# stop words and urls for blocking urls
stop_words = []
stop_urls = []

response_container = ""

#!/usr/local/bin/python
configuration = configparser.ConfigParser()
configuration.read('config.env')

RELAX_TIME = float(configuration.get('CONFIG', 'RELAX_TIME'))

QUALITY_SCORE = float(configuration.get('CONFIG', 'QUALITY_SCORE'))
DIFFICULTY_RATIO = int(configuration.get('CONFIG', 'DIFFICULTY_RATIO'))

KEYWORDS_IN_LINK = int(configuration.get('CONFIG', 'KEYWORDS_IN_LINK'))
MIN_LINK_SIZE = int(configuration.get('CONFIG', 'MIN_LINK_SIZE'))
MIN_WORD_SIZE = int(configuration.get('CONFIG', 'MIN_WORD_SIZE'))

DESCRIPTION_SIZE = int(configuration.get('CONFIG', 'DESCRIPTION_SIZE'))

DOWNLOAD_OPTION = int(configuration.get('CONFIG', 'DOWNLOAD_OPTION'))
DOWNLOAD_HTML = int(configuration.get('CONFIG', 'DOWNLOAD_HTML'))

MEDIA_FILES = "m3u,mkv,m3u8,mp4,webm,mp3,jpeg,mov,avi" 
EXTRA_KEYWORDS = "photo,photograph,image,picture,pic,gallery,wallpaper,hd,4k,art,illustration,collection,unique,special,landscape"
OFFLIMIT_DOMAINS = "github,lifewire,youtube,apple,link,microsoft,google,facebook,twitter" 
        
def init_program():
    print("WELCOME TO MY image-miner\n")
    print("Powered by Python")

    # clean urls lists
    user_input = input("Clean start? (y/n)")
    setup_process(user_input)

    # Insert urls on top of the url list
    # Download the first url
    query = input("What type of images you want to spider?")

    # add the user query to the user querie list
    # add also to the query_keywords list
    query_keywords.append(query)

    # Add extra image related search terms to enhance
    # the search results the liste is in config.env
    listUrl = search(query.strip())
    print("IMAGE MINER WILL ADD THE FOLLOWING KEYWORDS")
    print("TO GET MOTRE RESULTS")
    relax(RELAX_TIME*2)
    
    import random
    KEYWORDS = []

    x = random.randint(1, 15)
    for i in EXTRA_KEYWORDS.split(","):
        if i == x:
            break
        KEYWORDS.append(i)

    t = 0
    while t < x:
        y = random.randint(1, 15)
        for i in EXTRA_KEYWORDS.split(","):
            if i == y:
                break
        KEYWORDS.append(y)
        relax(RELAX_TIME)
        t = t + 1

    print("Will add the following words: ")
    relax(RELAX_TIME*2)
    
    for i in KEYWORDS:
        print(i)

    print("\n\nAdding... ")    
    relax(RELAX_TIME*2)
   
    for extra_query in EXTRA_KEYWORDS.split(","):
        relax(RELAX_TIME)
        query_keywords.append(extra_query)
        query = query + " " + extra_query

    print("THIS IS THE FULL ENHANCED SEARCH QUERY: ")
    relax(RELAX_TIME*2)

    print("New Url have been added to the meemory")
    for i in listUrl:
        urls_buffer.append(i)
        relax(RELAX_TIME)

def insert_data(url, keywords, filename, original_name):
    try:
        relax(RELAX_TIME*2)
        db_file = "data-miner.db"
        conn = sqlite3.connect(db_file)
        relax(RELAX_TIME*2)
        
        if (keywords == None):
            keywords = "empty"
        if (original_name == None):
            original_name = "empty"
        
        relax(RELAX_TIME*2)
        c = conn.cursor()
        c.execute("INSERT INTO image (url, keywords, filename, file_id) VALUES (?,?,?,?)",
                  (url, keywords, filename, original_name))
        conn.commit()
        relax(RELAX_TIME*2)
        conn.close()
    except Error as e:
        print(e)

def check_media(url_extracted):
    print("Checking Media...")
    relax(RELAX_TIME)

    # Most common media files
    for media_ext in MEDIA_FILES.split(","):
        relax(RELAX_TIME)
        if url_extracted.find(str("."+media_ext.strip())) >= 0:
            print("Hit media found in : " + url_extracted)
            relax(RELAX_TIME*2)
            downloadFile(url_extracted)


def downloadFile(url_extracted):
    global memory
    print("MEDIA FOUND starting PROCESS")
    print("MEDIA FOUND : " + url_extracted)
    relax(RELAX_TIME*2)

    import uuid
    filename = str(uuid.uuid4())
    file = url_extracted.split("/")[-1]
    relax(RELAX_TIME*2)
    
    # Dump invalid urls
    # Request the profile picture of the OP:

    # Now use this like below,
    save_path = './media/'
    relax(RELAX_TIME*2)

    if (DOWNLOAD_OPTION == 1):
        if url_extracted not in memory:
            import wget
            relax(RELAX_TIME)
            try:
                wget.download(url_extracted, save_path + file)
                relax(RELAX_TIME)
                memory.append(url_extracted)
            except:
                print("Error downloading")

    title = url_extracted
    ext = url_extracted.split(".")[-1]
    
    relax(RELAX_TIME*2)
    
    file = url_extracted.split("/")[-1]
    title = format_title(str(file), str(ext))
    
    relax(RELAX_TIME*2)
    
    # Dump invalid urls
    if(url_extracted.find(".mp4") <= 1 and url_extracted.find("mp3") <= 1):
        archive_filename = "ARCHIVE_MEDIA.M3U"

    # Dump invalid urls
    if(url_extracted.find(".mp3") > 0):
        archive_filename = "ARCHIVE_MP3.M3U"

    # Dump invalid urls
    if(url_extracted.find(".mp4") > 0):
        archive_filename = "ARCHIVE_MP4.M3U"

    relax(RELAX_TIME*2)

    if title not in memory:
        with open(archive_filename, "a") as file:
            relax(RELAX_TIME)

            print("VOD url: " + url_extracted)
            EXTINF_text = "#EXTINF:-1, " + title
            file.write(EXTINF_text + "\n")

            relax(RELAX_TIME)
            file.write(url_extracted + "\n")

            relax(RELAX_TIME)
            file.close()
            memory.append(title)
    else:
        print("VIDEO ALL READY EXTRACTED")
        with open(archive_filename, "a") as file:
            relax(RELAX_TIME)
            
            print("VOD url: " + url_extracted)
            EXTINF_text = "#EXTINF:-1, " + title
            file.write(EXTINF_text + "\n")
            
            relax(RELAX_TIME)
            file.write(url_extracted + "\n")
            
            relax(RELAX_TIME)
            file.close()
            memory.append(title)

def format_title(title, ext):
    
    try:
        from urllib.parse import urljoin, urlparse
        title = urlparse.unquote(title)
        relax(RELAX_TIME)
    except:
        pass

    title = clean_word_final(title)
    relax(RELAX_TIME)

    # Separate term that have capital letter
    full_title = ""
    for i in title:
        if (i.isupper()):
            full_title = full_title + " " + i.capitalize()
            relax(RELAX_TIME)
        else:
            full_title = full_title + i

    relax(RELAX_TIME)
    full_title = full_title.replace("  ", " ")
    cap_next = False
    full_title_final = ""
    for i in full_title:
        if (cap_next == True):
            full_title_final = full_title_final + i.capitalize()
            cap_next = False
            relax(RELAX_TIME)
            continue
        if (i == " "):
            full_title_final = full_title_final + i
            cap_next = True
            relax(RELAX_TIME)
        else:
            full_title_final = full_title_final + i
            cap_next = False
            relax(RELAX_TIME)

    relax(RELAX_TIME)
    full_title_final = full_title_final.replace("  ", " ")
    full_title_final = full_title_final.lstrip()
    full_title_final = full_title_final.strip()
    relax(RELAX_TIME)

    print("FINISHID FORMAT TITLE: " + str(full_title_final))
    title = full_title_final
    title = clean_numbers(title)

    return title

def search(query):

    list_google = []
    list_yahoo = []
    list_bing = []

    import search_lib as s
    query = query.replace(" ", "+")

    list_google = s.search_google(query)
    list_yahoo = s.search_yahoo(query)
    list_bing = s.search_bing(query)

    print("list_google as " + str(len(list_google)) + " results")
    print("list_yahoo as " + str(len(list_yahoo)) + " results")
    print("list_bing as " + str(len(list_bing)) + " results")

    for i in list_google:
        if not i in listUrl:
            listUrl.append(i)
    for i in list_yahoo:
        if not i in listUrl:
            listUrl.append(i)
    for i in list_bing:
        if not i in listUrl:
            listUrl.append(i)

    print("Total number of search queries : " + str(len(listUrl)))
    return listUrl

# starting list will be save to urls.txt
# each spidered url will verify html content and extract new urls to the file
# the urls.txt are the full for the spider
def setup_process(user_input):
    print("STARTING SETUP PROCESS")
    if (user_input == "y"):
        clean_url_file()
        relax(RELAX_TIME*40)

        # clean images folders
        delete_images_in_folders("full")
        relax(RELAX_TIME*40)

        delete_html_in_folders()
        relax(RELAX_TIME*40)

def clean_url_file():
    with open("urls.txt", "w", encoding="utf-8") as file:
        file.write("")
        relax(RELAX_TIME*4)

    with open("urls_extracted.txt", "w", encoding="utf-8") as file:
        file.write("")
        relax(RELAX_TIME*4)

    with open("urls_visited.txt", "w", encoding="utf-8") as file:
        file.write("")
        relax(RELAX_TIME*4)

    with open("urls_images.txt", "w", encoding="utf-8") as file:
        file.write("")
        relax(RELAX_TIME*4)


def delete_images_in_folders(switch):
    import os
    import os.path
    import re
    mypath = "./images/"
    relax(RELAX_TIME*40)


def delete_html_in_folders():
    import os
    import os.path
    import re
    relax(RELAX_TIME*40)

    mypath = "./images/data"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))


def start_image_miner():
    global content_keywords
    global response_container

    print("Loading memory...\n")
    relax(RELAX_TIME*40)

    # Load image-miner url memory
    get_urls("urls_visited.txt", urls_visited)
    get_urls("urls.txt", urls_buffer)

    # relax(RELAX_TIME)
    print("Memory loaded")
    print("Starting mining process...")

    for url in urls_buffer:
        print("\n\nSTART NEW PROCESS...")
        print("________________________________________________")
        relax(RELAX_TIME*2)
        if (url is not None):
            print("\n\nPROCESSING URL: " + str(url))
        relax(RELAX_TIME*4)

        # check url to block spider to process unwanted sites
        print("Checking stop list...\n")
        if (check_url_for_stop_keyword(str(url))):

            # as the url all ready been processed
            print("Checking visited list...\n")
            relax(RELAX_TIME)

            if not url in urls_visited:
                print("Initial verification - PASSED\n")
                relax(RELAX_TIME)
            else:
                urls_buffer.remove(url)
                continue
        else:
            urls_buffer.remove(url)
            continue
        
        if (url == None):
            continue

        print("DOWNLOADING URL: " + url)
        relax(RELAX_TIME)
        check_media(url)
        print("URL ABUSIVE MEDIA CHECK")
        html_file = get(url)

        # HTML VERIFICATION
        if (verify(html_file)):
            continue

        print("Adding url to visited memory...")
        if not url in urls_visited:
            urls_visited.append(url)
            relax(RELAX_TIME)

        print("Removing url from main buffer...")
        if url in urls_buffer:
            urls_buffer.remove(url)
            relax(RELAX_TIME)

        print("STARTING URL EXTRACTION PROCESS ")
        relax(RELAX_TIME)

        # extract url
        urls_links = extract_urls(url, html_file)
        relax(RELAX_TIME)

        # relax(RELAX_TIME)
        if urls_links == None or len(urls_links) < 1:
            continue

        print("PRO-ACTIVE CLEANUP PROCESS\n")
        relax(RELAX_TIME)

        # insert in session eliminating duplicate links
        for found_url in urls_links:
            if found_url in urls_buffer:
                while found_url in urls_links:
                    urls_links.remove(found_url)
                    continue

            if found_url in urls_visited:
                while found_url in urls_links:
                    urls_links.remove(found_url)
                    continue

            if (verify(found_url)):
                continue

            if not found_url in urls_buffer:
                if not found_url in urls_visited:
                    print("Url link found: " + found_url)
                    urls_buffer.append(found_url)
                    relax(RELAX_TIME*40)

        print("PRO-ACTIVE CLEANUP COMPLETED\n")
        print("\nSTARTING IMAGE EXTRACTION PROCESS ")
        print("\nEXTRACTING images from: \n\n")
        print(url + "\n\n")
        relax(RELAX_TIME)

        check_media(url)
        # extract image
        images_tags = extract_images(url, html_file)
        relax(RELAX_TIME*40)

        if images_tags == None:
            continue

        print("\n\nIMAGE LINK EXTRACTION SUCCESS\nwith: " + url)
        relax(RELAX_TIME)

        # insert in session eliminating duplicate links
        for img in images_tags:
            if not img in image_urls:
                image_urls.append(img)
                get_image(img)
            else:
                print("Image is ignored all ready spidered test - FAILED")

        # global cleanup to eliminate
        # #links that have been visited
        print("\n\nCALLING FINAL CLEANUP PROCESS\nwith: " + url)
        cleanup()

    relax(RELAX_TIME*4)
    # Recursive function will never stop
    start_image_miner()

def cleanup():
    # Save all visited urls
    relax(RELAX_TIME*4)
    print("Saving urls.txt")
    print("Saving urls_visited.txt")
    print("cleaning urls memory")

    # create a clean list
    clean_list = []

    # Rebuild the session list and clean
    for url in urls_buffer:
        if not url in urls_visited:
            clean_list.append(url)

    # Empty session url list
    urls_buffer.clear()

    # Rebuild the session list and clean
    for url in clean_list:
        if not url in urls_visited:
            urls_buffer.append(url)

    save_urls(urls_buffer, "urls.txt")
    save_urls(urls_visited, "urls_visited.txt")

def get_urls(filename, urls_list):

    # read url file
    with open(filename) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            if not line in urls_list:
                urls_list.append(trim(line))

    # debug - function information
    return urls_list

def dump_email_data(file_name, data):
    if not data in memory:
        relax(RELAX_TIME)
        with open(file_name, "a") as file:
            print("filename: " + file_name)
            print("data: " + data)
            file.write(data + "\n")
            file.close()
    memory.append(data)

def get(url):

    global m_keywords

    try:
        if (verify_link(url)):
            relax(RELAX_TIME*4)
            print("\n\nLINK VERIFICATION - PASSED")
        else:

            if not url in urls_visited:
                urls_visited.append(url)

            while url in urls_buffer:
                urls_buffer.remove(url)

            print("\n\nLINK VERIFICATION TEST - Failed")
            relax(RELAX_TIME*4)

            return None

        if (url.find("mailto:") >= 0):
            dump_email_data("email.txt", url)
            url = urls_buffer[0]
        if (url.find("@") >= 0):
            dump_email_data("email_validation.txt", url)
            url = urls_buffer[0]
        # Getting the webpage, creating a Response object.
        try:
            print("Preparing the request object")
            relax(RELAX_TIME*4)
            
            try:
                page = requests.get(url, headers={'User-Agent': ua.random}, timeout=5  )  
                print(page)
            except Error as e:
                pass
            # Extracting the source code of the page.
            html_file = page.text
            print("\nWriting url to disk")

            # Set up the image URL and filename
            original_filename = url.split("/")[-1]

            filedate = datetime.datetime.now()
            filename = filedate.strftime("spider-%Y%M%H%S%f.html")
            # filename = filename + original_filename

            if DOWNLOAD_HTML == 1:
                with open("./data/" + filename, "w", encoding="utf-8") as file:
                    file.write(html_file)
                    file.close()
                relax(RELAX_TIME*40)

            m_key = ""
            for i in m_keywords:
                m_key = m_key + "-" + i

            insert_data(url, m_key, filename, original_filename)
            print("\n\nPAGE download is successful...")
            relax(RELAX_TIME)

            if not url in urls_visited:
                urls_visited.append(url)

            while url in urls_buffer:
                urls_buffer.remove(url)

            return html_file

        except Error as e:
            print(e)
            print('MAJOR EXCEPTION - getUrl()')
            print('ERROR url : ' + url)
        return None
    except Error as e:
        print(e)
        print('MAJOR EXCEPTION - getUrl()')
        print('ERROR url : ' + url)
    return None


def relax(sec):
    time.sleep(sec)

def get_image(url):
    global image_urls

    import os

    try:
        # Set up the image URL and filename
        origibnal_filename = url.split("/")[-1]
        filename = origibnal_filename
        check_media(url)
        relax(RELAX_TIME*40)

        # Does the file have am extension
        # file name creating with timestamp
        filename = datetime.datetime.now()
        filename = filename.strftime("img-%Y%M%H%S%f")

        # Open the url image, set stream to True, this will return the stream content.
        try:

            r = requests.get(
                url, headers={'User-Agent': ua.random}, stream=True, timeout=100)
            ext = get_extension(r)
            filename = filename + "." + ext

            if ext == "shtml":
                print("IMAGE IS NOT AN IMAGE - shtml")
                print("IMAGE EXTRACTION - FAILED")
                relax(RELAX_TIME)
                return False

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Because image was downloaded add it to visited links
                if not url in urls_visited:
                    urls_visited.append(url)

                if not url in image_urls:
                    image_urls.append(url)

                # Eliminate url from main urls buffer - Rethink NOT really needed
                while url in urls_buffer:
                    urls_buffer.remove(url)

                # Open a local file with wb ( write binary ) permission.
                with open("./images/" + filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                    f.close()

                try:

                    fileSize = os.path.getsize("./images/" + filename)
                    check_media(url)

                    relax(RELAX_TIME)
                    print('Image successfully Downloaded: ', filename)

                    m_key = ""
                    for i in m_keywords:
                        m_key = m_key + "-" + i

                    insert_data(url, m_key, filename, origibnal_filename)

                except:
                    print("FILE CLASSIFICATION depending of size ERROR")

                return True
            else:
                print('Image Couldn\'t be retreived')

                return False

        except:
            print('MAJOR EXCEPTION - Image Couldn\'t be retreived')
            return None

    except:
        print('MAJOR EXCEPTION - Image Couldn\'t be retreived')
        return None


def get_text(the_page):
    soup = BeautifulSoup(the_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ""
    blacklist = [
        '[document]',
        'script'
        'head'
        'meta'
        'css'
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output


def debug_info(info):
    # read url file
    f = open("debug.txt", "a")
    f.write(info)
    f.close()

def load_stop_list():
    global stop_words
    with open("stop_list.txt", "r") as file:
        # reading each line"
        for word in file:
            word = word.replace("\n", "")
            stop_words.append(word.strip())

def word_size(text, size):
    rebuild_text = ""
    # preformating word
    for word in text.split():
        if len(word) < size:
            rebuild_text = rebuild_text
        else:
            rebuild_text = rebuild_text + " " + word

    return rebuild_text

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

    print("LINK VERIFICATION")
    check_media(link)

    i_score = 0

    for keyword in query_keywords:
        link = link.lower()
        if (link.find(keyword.lower()) >= 0):

            print("MATCH keyword is " + keyword)

            if (len(keyword) > MIN_WORD_SIZE):
                i_score = i_score + 1

                if i_score > KEYWORDS_IN_LINK-1:

                    print("ACCEPTED LINK - KEYWORD MATCH SCORE : " + str(i_score))
                    print("URL: " + link)
                    print("MATCHING KEYWORDS FOUND IN LINK - PASSED")

                    return True

    print("NO MATCHING KEYWORDS FOUND IN LINK - FAILED")
    return False


def verify_page_content(url, title, text):

    if (url == None):
        return False

    print("STARTING PAGE CONTENT VERIFICATION")
    print("Checking url: ")
    print("url: " + url)

    global m_keywords
    global content_keywords
    global i_score

    i_score = 0

    keywords = []
    m_keywords = []

    for items in content_keywords:
        for word in items.split():
            word = word.lower()
            word = trim(word)
            word = str(word)

            word = clean_word_final(word)
            word = clean_stop_list(word)

            if (len(word) > 2):
                if not word in keywords:
                    # print(word)
                    keywords.append(word)

                    # add keyword without s at the end
                    if (keywords[len(keywords)-1] == "s"):
                        keywords.append(word[0:len(keywords)-1])

                    # add root word
                    keywords.append(word[0:6])

    # Clean numbers from text
    text = clean_numbers(text)
    m_keywords.append(title)
    print("TEXT TOTALLY CLEANED")
    print(text)
    print("------------------------")
    print("TITLE: " + title)
    print("URL: " + url)
    print("CONTENT: " + text[0:text.find(" ",
          text.find(" ", DESCRIPTION_SIZE))])
    m_keywords.append(text[0:text.find(" ", DESCRIPTION_SIZE)])

    relax(RELAX_TIME*30)

    for keyword in text.split():

        # normalize keyword
        keyword = keyword.lower()
        keyword = trim(keyword)
        keyword = str(keyword)

        # keyword clean and stop list
        keyword = clean_word_final(keyword)
        keyword = clean_stop_list(keyword)

        if (len(keyword) > 2):
            if keyword in query_keywords:

                m_keywords.append(keyword)
                print("KEYWORD ADDED" + keyword)
                i_score = i_score + 10
                if i_score > QUALITY_SCORE:
                    if not keyword in m_keywords:
                        m_keywords.append(keyword)

                    print("URL PASSES QUALITY SCORE: " + str(i_score))
                    return False

                #print("Hit a match score for url is: " + str(i_score))
                #print("keyword: " + str(keyword))
                #print("url: " + str(url))

                relax(RELAX_TIME)

            if keyword in keywords:
                i_score = i_score + 1
                if i_score > QUALITY_SCORE:
                    print("URL PASSES QUALITY SCORE: " + str(i_score))
                    return False

                #print("Hit a match score for url is: " + str(i_score))
                #print("keyword: " + str(keyword))
                #print("url: " + str(url))
                # relax(RELAX_TIME)

    print("FINAL QUALITY SCORE: " + str(i_score))

    if i_score > QUALITY_SCORE:
        print("URL PASSES QUALITY SCORE: " + str(i_score))
        return False

    return True


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

    try:

        urls_links = []

        print("\nPROCESSING url extraction process\nurl: " + url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.head.title.text
        url_text = soup.get_text()
        print("Getting text in url...\n ")
        relax(RELAX_TIME)

        print("Formating text...\n\n ")
        relax(RELAX_TIME)

        try:
            # NEED TO MAKE A STRIP FUNCTION
            url_text = url_text.replace("\n", " ")
            url_text = url_text.replace("  ", " ")

            url_text = word_size(url_text, MIN_LINK_SIZE)

            url_text = clean_raw_text(url_text)

            # normalize keyword
            url_text = url_text.lower()

            # keyword clean and stop lists
            url_text = clean_word_final(url_text)
            url_text = clean_stop_list(url_text)

            url_text = clean_raw_text(url_text)

            url_text = trim(url_text)
            url_text = str(url_text)

            print(url_text)
            relax(RELAX_TIME)
        except:
            print("ERROR - FORMATING URL CONTENT")

        print("\nVERIFYING PAGE CONTENT before extracting links from url")
        relax(RELAX_TIME)

        if (verify_page_content(url, title, url_text)):
            print("URL IS IGNORED - It does not have a good quality score\n\n")
            relax(RELAX_TIME)
            return urls_links

        print("\nURL CONTENT TEST - PASSED\n")
        relax(RELAX_TIME)

        print("\nSTARTING URL EXTRACTION PROCESS\n")
        relax(RELAX_TIME)

        print("\nStarting SOUP\n")
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all("a"):

            try:
                link = link.get("href")

                print(link)

                if link in urls_visited:
                    print("Link has all ready been downloaded in visited list memory")
                    continue

                # Check if the url is long enoughs to process
                print("____________________________________________")
                print("\n\nVERIFY size of url")
                print("URL: " + link)

                if (len(link) < MIN_LINK_SIZE):
                    print("\ninvalid link length to small - FAILED")
                    # relax(RELAX_TIME)
                    continue

                print("SIZE OF THE LINK - PASSED")
                relax(RELAX_TIME)

                # Rebuild the site if the url root is missing
                if not link is None:
                    root_path = ""
                    if link.find("http") < 0:
                        # get root https path
                        root_path = get_path(url, link)

                        if not root_path in urls_buffer:
                            print("Adding root path\n" + root_path)
                            urls_buffer.append(root_path)

                        if link[0] == "/":
                            link = root_path + link
                        else:
                            link = root_path + "/" + link

                print("\nROOT PATH VERIFICATION - PASSED")
                print("URL: " + link)
                # relax(RELAX_TIME)

                if verify_link(link):
                    print("\nLink verification test - PASSED\n\n")
                    print("URL: " + link)
                    # relax(RELAX_TIME)
                    urls_links.append(link)
                else:
                    continue

            except:
                print('ERROR EXCEPTION - extract() sub section link = link.get(sub_tag)')
                print(link)
                relax(RELAX_TIME)

            if not link in urls_links:
                if (link != url):

                    try:
                        if (check_url_for_stop_keyword(link)):
                            print("\n\nStop list test - PASSED\n\n")
                            # relax(RELAX_TIME)
                        else:
                            print("\n\nStop list test - FAILED\n\n")
                            continue

                        print("new link found:\n" + link)

                        if not link in urls_buffer:
                            print("ADDING TO MAIN URL BUFFER\n\n" + link)
                            urls_buffer.append(link)
                            # relax(RELAX_TIME)

                    except:
                        print(
                            'MAJOR EXCEPTION URLS - extract_urls() sub section link in links')
                        relax(RELAX_TIME)

        return urls_links
    except:
        print('MAJOR EXCEPTION URLS - extract_urls()')
        relax(RELAX_TIME)

        return urls_links

# this function extract urls or img from a url
# it returns a list of urls or images tags


def extract_images(url, html):

    # Images stats
    numLink = 0

    try:
        img_links = []

        print("\n\nPROCESSING image tags extraction: \nURL: " + url + "\n")

        print("Creating soup object...")

        soup = BeautifulSoup(html, "html.parser")

        print("STARTING IMAGE EXTRACTION")

        for link in soup.find_all("img"):

            numLink = numLink + 1

            link = link.get("src")

            print("\nImage link\n\nURL: " + link)
            print("\nNumber of images " + str(numLink))

            # Rebuild the site if the url root is missing
            if not link is None:
                root_path = ""
                if link.find("http") < 0:
                    # get root https path
                    root_path = get_path(url, link)

                    if not root_path in urls_buffer:
                        print("Adding root path\n" + root_path)
                        urls_buffer.append(root_path)

                    if link[0] == "/":
                        link = root_path + link
                    else:
                        link = root_path + "/" + link

            print("\nAFTER ROOT VERIFICATION:\nURL: " + link + "\n\n")

            if not link in img_links:
                if (link != url):
                    try:

                        relax(RELAX_TIME)
                        print("\nCHEKING IMAGE LINK FOR STOP WORDS IN URL\n")

                        relax(RELAX_TIME)
                        if (check_url_for_stop_keyword(str(link))):
                            print("\nAdding link img_links")
                            print("\nImage link passes keyword in link - PASSED ")
                            print("\nURL:" + link)
                        else:
                            print("\nMATCH STOP WORD FOUND IN URL TEST _ FAILED")
                            print("\nThis link wont be spidered")
                            continue

                        relax(RELAX_TIME)
                        if not link in image_urls:
                            img_links.append(link)
                            print("\nImages link not in memory - PASSED")
                        else:
                            print(
                                "\nImages will not be added allready in memory - FAILED")
                            continue
                    except:
                        print(
                            '\nEXCEPTION - extract_images() sub section link in links:')
                        # relax(RELAX_TIME)

        relax(RELAX_TIME)
        print("\nIMAGES " + numLink + " HAVE ALL BEEN EXTRACTED")
        relax(RELAX_TIME)
        return img_links

    except:
        print('EXCEPTION - extract images')
        relax(RELAX_TIME)
        return img_links


def clean_raw_text(url_text):

    from urllib.parse import urljoin, urlparse
    url_text = urlparse.unquote(url_text)
    
    while (url_text.find("\t") >= 0):
        url_text = url_text.replace("\t", " ")
        url_text = url_text.replace("\n", " ")
        url_text = url_text.replace("  ", " ")

    relax(RELAX_TIME)

    while (url_text.find("\n") >= 0):
        url_text = url_text.replace("\t", " ")
        url_text = url_text.replace("\n", " ")
        url_text = url_text.replace("  ", " ")

    relax(RELAX_TIME)

    while (url_text.find("  ") >= 0):
        url_text = url_text.replace("\t", " ")
        url_text = url_text.replace("\n", " ")
        url_text = url_text.replace("  ", " ")

    relax(RELAX_TIME)

    while (url_text.find("  ") >= 0):
        url_text = url_text.replace("\t", " ")
        url_text = url_text.replace("\n", " ")
        url_text = url_text.replace("  ", " ")

    relax(RELAX_TIME)

    while (url_text.find("  ") >= 0):
        url_text = url_text.replace("\t", " ")
        url_text = url_text.replace("\n", " ")
        url_text = url_text.replace("  ", " ")

    relax(RELAX_TIME)
    from urllib.parse import urljoin, urlparse
    url_text = urlparse.unquote(url_text)
    return url_text


def save_urls(urls, file_name):
    # write url in visited site file
    url_memory = []

    relax(RELAX_TIME)

    with open(file_name, "w", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                if not url in url_memory:
                    file.write(url + "\n")
                if not url in url_memory:
                    url_memory.append(url)
        file.close()

    relax(RELAX_TIME)


def get_path(url, link):

    print("Fixing broken paths : " + link)
    print("Url : " + url)

    relax(RELAX_TIME)

    if (url.find("https://") >= 0):
        url = url.replace("https://", "")
        split_url = url.split("/")
        return "https://" + split_url[0]

    relax(RELAX_TIME)

    if (url.find("http://") >= 0):
        url = url.replace("http://", "")
        split_url = url.split("/")
        return "http://" + split_url[0]

    relax(RELAX_TIME)

    # Just a guess
    url = url.replace("https://", "")
    split_url = url.split("/")
    return "https://" + split_url[0]


def verify(url):

    relax(RELAX_TIME)

    if (url == "") or (url == " ") or (url == None) or (len(url) < MIN_LINK_SIZE):
        return True
    else:
        return False


def get_extension(response):

    relax(RELAX_TIME)

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


def check_url_for_stop_keyword(url_to_check):

    relax(RELAX_TIME)

    for stop_url in stop_urls:
        try:
            if (url_to_check.find(stop_url) >= 0):
                print("Ignoring url found match in URL check list keyword")
                print("\nUrl: " + url_to_check)
                print("Stop keyword is: " + stop_url + "\n")
                print("STOP WORD IN URL TEST - FAILED\n")
                # relax(RELAX_TIME)
                return False
        except:
            print("ERROR in check_url_for_stop_keyword()")
            print("BECAUSE OF ERROR - STOP WORD IN URL TEST - FAILED\n")
            return False

    print("Url passed the URL check list test - PASSED")
    relax(RELAX_TIME)

    return True


def load_stop_urls():

    relax(RELAX_TIME)

    global stop_urls
    print("LOADING STOPLIST")

    with open("stop_urls.txt", "r") as file:
        # reading each line"
        for line in file:
            line = line.replace("\n", "")
            line = trim(line)
            stop_urls.append(line)


def trim(text_section):

    relax(RELAX_TIME)

    text_section = text_section.strip()
    text_section = text_section.lstrip()
    return text_section


def main():
    # Start image spider/miner program
    print("Start image-miner program")
    print("The system take some time to start")
    print("Please be patient...")

    relax(RELAX_TIME)
    print("LOADING URLS")
    load_stop_urls()

    relax(RELAX_TIME)
    print("LOADING LISTS")
    load_stop_list()

    relax(RELAX_TIME)
    print("INIT")
    init_program()

    relax(RELAX_TIME)
    print("START MINER")
    start_image_miner()


# start image miner 2.0
main()
