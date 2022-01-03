#!/usr/bin/env python
import datetime  # needed to create unique image file name
import mimetypes  # needed for download functionality
import shutil  # to save it locally
import time  # needed to create unique image file name

## Importing Necessary Modules
import requests  # to get image from the web
from bs4 import BeautifulSoup

urls_buffer = [] # program main url buffer
images_tags = [] # program main found url/link buffer

urls_links  = [] # buffer
urls_visited  = [] # visited_links
urls_extracted  = [] # urls_session

image_urls = []

# keywords container for query and page content
content_keywords = []
query_keywords = []

# stop words and urls for blocking urls
stop_words = []
stop_urls = []

response_container = ""

# Software parameter for twiking system images retrieval
RELAX_TIME = 2
CONTENT_QUALITY_SCORE = 60
MIN_LINK_LENGTH = 3
MIN_KEYWORD_LENGTH = 3
MIN_KEYWORDS_IN_LINK = 1
DIFFICULTY_RATIO = 8

# LEARNING FUNCTIONALITY
SMART_ERROR_SWITCH = 0
STABILIZER = 0

def init_program():
   
    print("WELCOME TO MY image-miner 2.0")       
    print("Python 3 program")    
    print("Developped")
    print("Guillermo Mosquera") 
    print("Memosasoft.ml - Memosa Services")
    print("help: gfm.mail,72@gmail.com\n")
    
    # clean urls lists
    user_input = input("Clean urls files? (y/n)")
    
    setup_process(user_input)
        
    # Insert urls on top of the url list
    # Download the first url
    val = input("What type of images you want to spider?")
       
    # get url start list for spidering process
    get_urls_search_api(val)
    
    # build query and content verification keyword list
    build_keywords_lists(val)
    
    relax(RELAX_TIME)
    
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
            
            if (len(keywords)>MIN_KEYWORD_LENGTH):
                
                query_keywords.append(keywords)
                content_keywords.append(keywords)
                                             
                # ADDING WORD WITHOUT S AT THE END
                if (keywords[len(keywords)-1]=="s"):
                    query_keywords.append(keywords[0:len(keywords)-1])        
                    content_keywords.append(keywords[0:len(keywords)-1])
                
                # ADDING WORD ROOT FOR BETTER MATCHING          
                if (len(keywords)>=6):
                    query_keywords.append(keywords[0:3])
                    content_keywords.append(keywords[0:3])
               
                # add root of the word 
                if (len(keywords)>=12):
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
    CONTENT_QUALITY_SCORE = CONTENT_QUALITY_SCORE * (len(query_keywords)/DIFFICULTY_RATIO)
    print("CONTENT_QUALITY_SCORE is " + str(CONTENT_QUALITY_SCORE) + "\n")

# starting list will be save to urls.txt
# each spidered url will verify html content and extract new urls to the file
# the urls.txt are the full for the spider 

def get_urls_search_api(val):
    # PSEUDO CODE 
    # Connect to search apiget_urls_from_search_api
    # Bring back urls from search api
    print("Connecting to search api")
    
    # loop thru search api 5
    max_loop = [1,2,3,4,5]
    print("Building keywords list object")
        
    for loop in max_loop:
        response = connect_search_api(val, loop)

        #relax(RELAX_TIME)   

        # save found url to urls.txt file
        f = open("urls.txt", "a")
            
        for search_results in response["value"]:
            search_url = search_results["url"]
            #print("\n\n_____________________________________________________")
            #print("\nkeywords to memory content verification list")
            #print("\nAdding: " + search_results["title"])
            
            content_keywords.append(search_results["title"])
            
            #print("\nurl to the url buffer list")
            #print("\nurl: " + search_url)
            f.write(search_url + "\n")
            
            #relax(RELAX_TIME)
            
        
        f.close()

def setup_process(user_input):
    if (user_input=="y"):
        clean_url_file()
        
    # clean images folders
    user_input = input("Clean images folders? (y/n)")
       
    if (user_input=="y") or (user_input=="Y"): 
        
        user_input = input("Partial clean up or full cleanup? (p)artial/(f)ull")
        
        if (user_input=="p") or (user_input=="P"): 
            delete_images_in_folders("partial")
    
        if (user_input=="f") or (user_input=="F"):        
            delete_images_in_folders("full")
            
    user_input = input("Delete html files?")
    
    if (user_input=="y") or (user_input=="Y"): 
        delete_html_in_folders()
    
def clean_url_file():
    with open("urls.txt", "w", encoding="utf-8") as file:
        file.write("")
    with open("urls_extracted.txt", "w", encoding="utf-8") as file:
        file.write("")
    with open("urls_visited.txt", "w", encoding="utf-8") as file:
        file.write("")
    with open("urls_images.txt", "w", encoding="utf-8") as file:
        file.write("")
        
def delete_images_in_folders(switch):
    import os
    import os.path
    import re
    
    mypath = "./images/large_images"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
    
    mypath = "./images/normal_images"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
            mypath = "./images/very_small_images"
    
    if (switch=="full"):
        mypath = "./images/small_images"
        for root, dirs, files in os.walk(mypath):
            for file in files:
                os.remove(os.path.join(root, file))
        
        mypath = "./images/very_small_images"
        for root, dirs, files in os.walk(mypath):
            for file in files:
                os.remove(os.path.join(root, file))

def delete_html_in_folders():
    import os
    import os.path
    import re
    
    mypath = "./images/data"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
     
def start_image_miner():
   
    global content_keywords
    global response_container 
   
    print("Loading memory...\n")
      
    # Load image-miner url memory 
    get_urls("urls_visited.txt", urls_visited)
    get_urls("urls.txt", urls_buffer)
    
    #relax(RELAX_TIME)   
    print("Memory loaded")
    print("Starting mining process...")
    
    for url in urls_buffer:
        print("\n\nSTART NEW PROCESS...")
        print("________________________________________________")
        relax(RELAX_TIME*2)
        
        print("\n\nPROCESSING URL: " + url)
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
    
        print("DOWNLOADING URL: " + url)
        relax(RELAX_TIME)
                
        html_file = get(url)
        
        if (verify(html_file)):
            continue
                        
        print("Adding url to visited memory...")
        if not url in urls_visited:
            urls_visited.append(url)
        
        print("Adding url from main buffer...")
        if url in urls_buffer:
            urls_buffer.remove(url)
        
        print("STARTING URL EXTRACTION PROCESS ")
        relax(RELAX_TIME) 
        
        # extract url
        urls_links = extract_urls(url, html_file)
        
        #relax(RELAX_TIME) 
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

                    
        print("PRO-ACTIVE COMPLETED\n") 
            
        print("\nSTARTING IMAGE EXTRACTION PROCESS ")
        print("\nEXTRACTING images from: \n\n")
        print(url + "\n\n")   
        
        relax(RELAX_TIME)
        
        # extract image
        images_tags = extract_images(url, html_file)
        
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
        
    # Recursive function will never stop
    start_image_miner()

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

def cleanup():       
    # Save all visited urls
    
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
   
def get(url):
    try:  
        if (verify_link(url)):             
            print("\n\nLINK VERIFICATION - PASSED")
        else:
            
            if not url in urls_visited:
                urls_visited.append(url)
                
            while url in urls_buffer:   
                urls_buffer.remove(url)
            
            print("\n\nLINK VERIFICATION TEST - Failed")
                        
            return None
                
        # Getting the webpage, creating a Response object.
        response = requests.get(url)
    
        # Extracting the source code of the page.
        html_file = response.text
        
        print("\nWriting url to disk")
        
        ## Set up the image URL and filename
        # original_filename = url.split("/")[-1]
        
        filedate = datetime.datetime.now()
        filename = filedate.strftime("spider-%Y%M%H%S%f.html")
        # filename = filename + original_filename
        
        with open("./data/" + filename , "w", encoding="utf-8") as file:
            file.write(html_file)
            file.close()

        print("\n\nPAGE download is successful...")
        
        relax(RELAX_TIME)
   
        if not url in urls_visited:
            urls_visited.append(url)
                
        while url in urls_buffer:   
            urls_buffer.remove(url)
            
        return html_file
    except:
        
        print('MAJOR EXCEPTION - getUrl()')  
        print('ERROR url : ' + url)   
    return None

def relax(sec):
    time.sleep(sec) 

def get_image(url):
    
    global image_urls
    
    import os

    try:        
        ## Set up the image URL and filename
        filename = url.split("/")[-1]
        
        # print("The image filename is: " + filename)
        
        # TODO - verify keywords in file name
        
        # Does the file have am extension
        # file name creating with timestamp
        filename = datetime.datetime.now()
        filename = filename.strftime("img-%Y%M%H%S%f") 

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream = True)
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
            with open("./images/" + filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)        
                f.close()
            
            try:   
                fileSize = os.path.getsize("./images/" + filename)
                
                if (ext == "mp4"):
                    shutil.move("./images/" + filename, './images/mp4')
                if (ext == "mp3"):
                    shutil.move("./images/" + filename, './images/mp3')
                elif (fileSize>100000):
                    shutil.move("./images/" + filename, './images/large_images')
                elif (fileSize>50000) and (fileSize<100000):
                    shutil.move("./images/" + filename, './images/normal_images') 
                elif (fileSize>500) and (fileSize<50000):
                    shutil.move("./images/" + filename, './images/small_images') 
                else:
                    shutil.move("./images/" + filename, './images/very_small_images') 
                    
                relax(RELAX_TIME)  
                print('Image successfully Downloaded: ',filename)
                      
            except:
                print("FILE CLASSIFICATION depending of size ERROR")
                    
            return True
        else:
            print('Image Couldn\'t be retreived')
            return False
    except:
        print('MAJOR EXCEPTION - Image Couldn\'t be retreived')
        return None   
         
def get_text(the_page):  
    soup = BeautifulSoup(the_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ""
    blacklist = [
        '[document]',
        'script',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'css',
        'script',
        'meta',
        'div'
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

    with open("stop_list.txt","r") as file: 
    # reading each line"
        for word in file:
            word = word.replace("\n","")
            word = trim(word)
            stop_words.append(word)

def word_size(text, size):    
    rebuild_text = ""    
    # preformating word     
    for word in text.split():    
        if len(word)<size:
            rebuild_text =  rebuild_text  
        else:
            rebuild_text =  rebuild_text + " " + word 
        
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
    
    i_score = 0
        
    for keyword in query_keywords:
        link = link.lower()
        if (link.find(keyword.lower())>=0):
            
            print("MATCH keyword is " + keyword)
            
            if (len(keyword)>MIN_KEYWORD_LENGTH):
                i_score = i_score + 1
                
                if i_score > MIN_KEYWORDS_IN_LINK-1:
                    
                    print("ACCEPTED LINK - KEYWORD MATCH SCORE : " + str(i_score))   
                    print("URL: " + link)     
                    print("MATCHING KEYWORDS FOUND IN LINK - PASSED") 
                    
                    return True
    
    print("NO MATCHING KEYWORDS FOUND IN LINK - FAILED") 
    return False  
    
def verify_page_content(url, text):
     
    print("STARTING PAGE CONTENT VERIFICATION")
    print("Checking url: ")
    print("url: " + url)
       
    global content_keywords
    global i_score
    
    i_score = 0
    
    keywords = []
    
    for items in content_keywords:
        for word in items.split():
            word = word.lower()
            word = trim(word)
            word = str(word)
            
            word = clean_word_final(word)
            word = clean_stop_list(word)
            
            if (len(word)>2): 
                if not word in keywords:
                    #print(word)
                    keywords.append(word)
                    
                    # add keyword without s at the end
                    if (keywords[len(keywords)-1]=="s"):
                        keywords.append(word[0:len(keywords)-1])
                        
                    # add root word
                    keywords.append(word[0:6])
             
    for keyword in text.split():
        
        # normalize keyword 
        keyword = keyword.lower()
        keyword = trim(keyword)
        keyword = str(keyword)
        
        # keyword clean and stop list
        keyword = clean_word_final(keyword)
        keyword = clean_stop_list(keyword)
        
        if (len(keyword)>2): 
            if keyword in query_keywords:
                i_score = i_score + 10
                if i_score > CONTENT_QUALITY_SCORE:
                    print("URL PASSES QUALITY SCORE: " + str(i_score))  
                    return False
                
                #print("Hit a match score for url is: " + str(i_score))
                #print("keyword: " + str(keyword))
                #print("url: " + str(url))
                
                #relax(RELAX_TIME)
            
                                
            if keyword in keywords:
                i_score = i_score + 1
                if i_score > CONTENT_QUALITY_SCORE:
                    print("URL PASSES QUALITY SCORE: " + str(i_score))  
                    return False
                
                #print("Hit a match score for url is: " + str(i_score))
                #print("keyword: " + str(keyword))
                #print("url: " + str(url))
                #relax(RELAX_TIME)

                    
    print("FINAL QUALITY SCORE: " + str(i_score))      
    
    if i_score > CONTENT_QUALITY_SCORE:
        print("URL PASSES QUALITY SCORE: " + str(i_score))      
        return False
    
    return True
    
# this function extract urls or img from a url
# it returns a list of urls or images tags
def extract_urls(url, html): 
    
    try:
        
        urls_links = []
        
        print("\nPROCESSING url extraction process\nurl: " + url)
        soup = BeautifulSoup(html, "html.parser")
        
        print("Getting text in url...\n ")
        url_text = get_text(html)
        relax(RELAX_TIME) 
        
        print("Formating text...\n\n ")
        relax(RELAX_TIME) 
        
        try:
            # NEED TO MAKE A STRIP FUNCTION
            url_text = url_text.replace("\n", " ")   
            url_text = url_text.replace("  ", " ")    
                    
            url_text = word_size(url_text, MIN_LINK_LENGTH)

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
        
        if (verify_page_content(url, url_text)):
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
                
                if (len(link)<MIN_LINK_LENGTH):
                    print("\ninvalid link length to small - FAILED")
                    #relax(RELAX_TIME) 
                    continue
                
                print("SIZE OF THE LINK - PASSED")
                #relax(RELAX_TIME) 
                
                # Rebuild the site if the url root is missing
                if not link is None:
                    root_path = ""
                    if link.find("http")<0:
                        # get root https path
                        root_path = get_path(url, link)
                        
                        if not root_path in urls_buffer:
                            print("Adding root path\n" +  root_path)
                            urls_buffer.append(root_path)
                            
                        if link[0] == "/":
                            link = root_path + link
                        else:
                            link = root_path + "/" + link  
                            
                print("\nROOT PATH VERIFICATION - PASSED")
                print("URL: " + link)
                #relax(RELAX_TIME) 
                        
                if verify_link(link):
                    print("\nLink verification test - PASSED\n\n")
                    print("URL: " + link)
                    #relax(RELAX_TIME)
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
                            #relax(RELAX_TIME)
                        else:
                            print("\n\nStop list test - FAILED\n\n")
                            continue
                        
                        print("new link found:\n" + link)
                        
                        if not link in urls_buffer:
                            print("ADDING TO MAIN URL BUFFER\n\n" + link)
                            urls_buffer.append(link)
                            #relax(RELAX_TIME) 
 
                    except:
                        print('MAJOR EXCEPTION URLS - extract_urls() sub section link in links')
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
                if link.find("http")<0:
                    # get root https path
                    root_path = get_path(url, link)
                    
                    if not root_path in urls_buffer:
                        print("Adding root path\n" +  root_path)
                        urls_buffer.append(root_path)
                        
                    if link[0] == "/":
                        link = root_path + link
                    else:
                        link = root_path + "/" + link  
            
            print("\nAFTER ROOT VERIFICATION:\nURL: " + link + "\n\n")
                        
            if not link in img_links:
                if (link != url): 
                    try:      
                        print("\nCHEKING IMAGE LINK FOR STOP WORDS IN URL\n")
                        
                        if (check_url_for_stop_keyword(str(link))):    
                            print("\nAdding link img_links")
                            print("\nImage link passes keyword in link - PASSED ")
                            print("\nURL:" + link)  
                        else:
                            print("\nMATCH STOP WORD FOUND IN URL TEST _ FAILED")
                            print("\nThis link wont be spidered")
                            continue
             
                        if not link in image_urls:
                            img_links.append(link) 
                            print("\nImages link not in memory - PASSED")    
                        else:
                            print("\nImages will not be added allready in memory - FAILED") 
                            continue     
                    except:
                        print('\nEXCEPTION - extract_images() sub section link in links:')   
                        #relax(RELAX_TIME)    
        
        print("\nIMAGES " + numLink + " HAVE ALL BEEN EXTRACTED")
        relax(RELAX_TIME)  
        
        return img_links
    
    except:
        print('EXCEPTION - extract images')
        relax(RELAX_TIME)  
        return img_links

def clean_raw_text(url_text):
    while (url_text.find("\t")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
    
    while (url_text.find("\n")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
    
    while (url_text.find("  ")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
    
    while (url_text.find("  ")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
    
    while (url_text.find("  ")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
        
    return url_text
        
def save_urls(urls, file_name): 
    # write url in visited site file
    url_memory = []
    
    with open(file_name, "w", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                if not url in url_memory:
                    file.write(url + "\n")
                if not url in url_memory:
                    url_memory.append(url) 
        file.close()
    
def get_path(url, link): 
    
    if (url.find("https://")>=0):
        url = url.replace("https://","")
        split_url = url.split("/")   
        return "https://" + split_url[0]
    
    if (url.find("http://")>=0):
        url = url.replace("http://","")   
        split_url = url.split("/")   
        return "http://" + split_url[0]
    
    # Just a guess
    url = url.replace("https://","")
    split_url = url.split("/")   
    return "https://" + split_url[0]

def verify(url):
    if (url == "") or (url == " ") or (url == None) or (len(url)<MIN_LINK_LENGTH):
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

def check_url_for_stop_keyword(url_to_check):
    
    for stop_url in stop_urls:
        
        try:
            if (url_to_check.find(stop_url)>=0):
                print("Ignoring url found match in URL check list keyword")
                print("\nUrl: " + url_to_check)
                print("Stop keyword is: " + stop_url + "\n")
                print("STOP WORD IN URL TEST - FAILED\n")
                #relax(RELAX_TIME)
                return False
        except:
            print("ERROR in check_url_for_stop_keyword()") 
            print("BECAUSE OF ERROR - STOP WORD IN URL TEST - FAILED\n")
            return False

    print("Url passed the URL check list test - PASSED")
    #relax(RELAX_TIME)
                        
    return True

def load_stop_urls():
    global stop_urls
    
    with open("stop_urls.txt","r") as file: 
                                  
        # reading each line"
        for line in file:
            line = line.replace("\n","")
            line = trim(line)
            stop_urls.append(line)
            
def trim(text_section): 
    text_section = text_section.strip()
    text_section = text_section.lstrip()
    return text_section 

def main():   
    # Start image spider/miner program
    load_stop_urls()
    load_stop_list()

    init_program()
    start_image_miner()
    
# start image miner 2.0    
main()
