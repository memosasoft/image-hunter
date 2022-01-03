#!/usr/bin/env python
from bs4 import BeautifulSoup

## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import datetime
import time
import mimetypes
import _thread

urls_buffer = []

images_links = []
images_links_processed = [] # images_session

urls_links  = []
urls_visited  = [] # visited_links
urls_extracted  = [] # urls_session

RELAX_TIME = 1
SMART_ERROR_SWITCH = 0
STABILIZER = 0

def start_image_miner():
   
    print("WELCOME TO MY image-miner")       
    print("Starting image mining")
    print("Simple Python 3 program ")    
    print("Developped Doctor g. ") 
    print("help: gfm@gmail.com")
  
    print("Loading memory")
    
    # Load image-miner url memory 
    get_urls("urls_visited.txt", urls_visited)
    get_urls("urls_images.txt", images_links_processed)
    get_urls("urls_extracted.txt", urls_extracted)
    get_urls("urls.txt", urls_buffer)
   
    global SMART_ERROR_SWITCH
    
    relax(RELAX_TIME) 
    
    print("Memory loaded")
    print("Starting mining process...")
    
    for url in urls_buffer:
        
            # DO NOT SPIDER BEWARE OF BIG PLAYERS
            # TODO - INSERT THIS STOP SITES INTO A
            #        FILE THAT CAN BE EDITED   
        if (url.find("facebook")>=0):
            print("url related to facebook")
            continue
        if (url.find("twitter")>=0):
            print("url related to twitter")
            continue
        if (url.find("google")>=0):
            print("url related to google")
            continue
        if (url.find("linkedin")>=0):
            print("url related to linkedin")
            continue
        if (url.find("yahoo")>=0):
            print("url related to yahoo")
            continue
        if (url.find("youtube")>=0):
            print("url related to youtube")
            continue
        if (url.find("instagram")>=0):
            print("url related to instagram")
            continue           
        if (url.find("pinterest")>=0):
            print("url related to pinterest")
            continue  
        if (url.find("cooldigital")>=0):
            print("url related to cooldigital")
            continue   
        if (url.find("500px")>=0):
            print("url related to 500px")
            continue  
        if (url.find("bing")>=0):
            print("url related to bing")
            continue  
        if (url.find("telus")>=0):
            print("url related to telus")
            continue  
        if (url.find(".mp4")>=0):
            print("FOUND A MP4 - CHANGING MODE")
            get_image(url)
            continue  
                
            # NEED TO VISIT THIS LINKS
            # AND BLOCK SPIDER PROCESS
            # THIS PLAYERS CAN TAKE LEGAL
            # ACTION - BETTER BE CAREFUL
            
            # pixabay
            # unsplash
            # pikwizard
            # Pexels
            # Life of Pix 
            # Gratisography
            # SplitShire
            # Burst 
            # Rawpixel 
            # Libreshot
            # PicJumbo 
            # Kaboompics
            # Rgbstock 
            # Good Stock Photos
            # StockSnap.io
            # Fancy Crave
            # ISO Republic.
            # Startup Stock Photos 
            # MMT Stock
            # FoodiesFeed 
            # Freerange 
            # StockVault
            # Styled Stock
            # New Old Stock
            # Skitterphoto
            # NegativeSpace
            # Moose Stock Photos
            # Picspree
                        
            if (link.find("telus")>=0):
                print("Link related to telus")
                continue  
         
        print("GETTING URL: " + url)
        
        # download url
        html_file = get(url)
        
        if (html_file == None):
            continue
        
        print("URL DOWNLOAD SUCCESS: " + url)
       
        print("Adding url to visited memory...")
        urls_visited.append(url)
        
        print("STARTING URL EXTRACTION PROCESS ")
        relax(RELAX_TIME) 
        
        # extract url
        urls_links = extract(url, html_file, "a", "href")
        
        if (urls_links == None):
            continue
        
        print("URLS EXTRACTION PROCESS SUCCESS: " + url)    
        
        print("PROC-ACTIVE CLEANUP PROCESS ")
        relax(RELAX_TIME) 
        
        # insert in session eliminating duplicate links
        for found_url in urls_links:
            if not found_url in urls_extracted:
                if not found_url in urls_visited:
                    urls_extracted.append(found_url)

        print("STARTING IMAGE EXTRACTION PROCESS ")
        relax(RELAX_TIME) 
            
        # extract image
        images_links = extract(url, html_file, "img", "src")
        
        if (images_links == None):
            continue
        
        print("IMAGE LINK EXTRACTION SUCCESS: " + url)
        
        print("Image memory verification")
        print("Verifying if the images has allready been downloaded by the spider")
        
        # insert in session eliminating duplicate links
        for img in images_links:
            if not img in images_links_processed:
                get_image(img)
                images_links_processed.append(img)
                
    # global cleanup to eliminate 
    # #links that have been visited
    cleanup()
        
    # Recursive function will never stop
    start_image_miner()

def cleanup():       
    # Save all visited urls
    
    print("Saving urls_visited.txt")
    print("Saving urls_extracted.txt")
    print("Saving urls_images.txt")
    
    save_urls(urls_visited, "urls_visited.txt")
    save_urls(urls_extracted, "urls_extracted.txt")
    save_urls(images_links_processed, "urls_images.txt")
    
    print("cleaning extracted urls memory")
    # create a clean list
    clean_list = []
    for cleanup in urls_extracted:
        if not cleanup in urls_visited:
            clean_list.append(cleanup)
    
    # Empty session url list
    urls_extracted.clear()
    
    # Rebuild the session list and reclean
    for url in clean_list:
        if not url in urls_extracted:
            if not url in urls_visited:
                urls_extracted.append(url)     
    
    print("Saving urls_images.txt")        
    save_urls(urls_extracted, "urls.txt")
    
def get_urls(filename, urls_list):
    
    # read url file 
    with open(filename) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            if not line.strip() in urls_list:
                urls_list.append(line.strip())
            
    fp.close()

    # debug - function information        
    return urls_list
   
def get(url):
    try:  
        # Getting the webpage, creating a Response object.
        response = requests.get(url)
    
        # Extracting the source code of the page.
        html_file = response.text
        
        with open("buffer.php", "w", encoding="utf-8") as file:
            file.write(html_file)
            file.close()

        return html_file
    except:
        print('MAJOR EXCEPTION - getUrl()')    
        return None

def relax(sec):
    time.sleep(sec) 

def get_image(url):
    import os
 
    relax(RELAX_TIME)  

    try:        
        ## Set up the image URL and filename
        filename = url.split("/")[-1]
        
        # Does the file have am extension
        # file name creating with timestamp
        filename = datetime.datetime.now()
        filename = filename.strftime("img-%Y%M%H%S%f")

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream = True)
        ext = get_extension(r)
        filename = filename + "." + ext
        
        if ext == "shtml":
            return False
        
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
                        
            # Because image was downloaded add it to visited links
            urls_visited.append(url)
            
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
                    
                SMART_ERROR_SWITCH = 0
                              
            except:
                print("FILE CLASSIFICATION depending of size ERROR")
                    
            print('Image successfully Downloaded: ',filename)
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
    
def extract(url, html, tag, sub_tag): 
    try:
        links = []
        
        print("PROCESSING: " + url)
        
        soup = BeautifulSoup(html, "html.parser")
        
        for link in soup.find_all(tag):
            
            link = link.get(sub_tag)
            
            if not link is None:
                root_path = ""
                if link.find("http")<0:
                    # get root https path
                    root_path = get_path(url, link)
                    urls_buffer.append(root_path + "\n")
                    
                    if link[0] == "/":
                        link = root_path + link
                    else:
                        link = root_path + "/" + link
                    
            # Debug exception
            if (link.find("javascript")>=0):
                print("invalid link javascript")
                continue
            if (link.find("#")>=0):
                print("invalid link document link")
                continue
            if (len(link)<5):
                print("invalid link length to small")
                continue
            
            # DO NOT SPIDER BEWARE OF BIG PLAYERS
            # TODO - INSERT THIS STOP SITES INTO A
            #        FILE THAT CAN BE EDITED     
            if (link.find("facebook")>=0):
                print("Link related to facebook")
                continue
            if (link.find("twitter")>=0):
                print("Link related to twitter")
                continue
            if (link.find("google")>=0):
                print("Link related to google")
                continue
            if (link.find("linkedin")>=0):
                print("Link related to linkedin")
                continue
            if (link.find("yahoo")>=0):
                print("Link related to yahoo")
                continue
            if (link.find("youtube")>=0):
                print("Link related to youtube")
                continue
            if (link.find("instagram")>=0):
                print("Link related to instagram")
                continue           
            if (link.find("pinterest")>=0):
                print("Link related to pinterest")
                continue                  
            
            if (link.find("cooldigital")>=0):
                print("Link related to cooldigital")
                continue    
            
            if (link.find("500px")>=0):
                print("Link related to 500px")
                continue    
            
            if link.find("bing")>=0:
                print("Link related to bing")
                continue   
                
                # NEED TO VISIT THIS LINKS
                # AND BLOCK SPIDER PROCESS
                # THIS PLAYERS CAN TAKE LEGAL
                # ACTION - BETTER BE CAREFUL
                # pixabay
                # unsplash
                # pikwizard
                # Pexels
                # Life of Pix 
                # Gratisography
                # SplitShire
                # Burst 
                # Rawpixel 
                # Libreshot
                # PicJumbo 
                # Kaboompics
                # Rgbstock 
                # Good Stock Photos
                # StockSnap.io
                # Fancy Crave
                # ISO Republic.
                # Startup Stock Photos 
                # MMT Stock
                # FoodiesFeed 
                # Freerange 
                # StockVault
                # Styled Stock
                # New Old Stock
                # Skitterphoto
                # NegativeSpace
                # Moose Stock Photos
                # Picspree
                        
            if (link.find("telus")>=0):
                print("Link related to telus")
                continue  
            
            if (url.find(".mp4")>=0):
                print("FOUND A MP4 - CHANGING MODE")
                get_image(url)
                continue                       
            
            if link in urls_visited:
                print("Link has all ready been downloaded in visited list memory")
                continue
 
            if link in urls_extracted:
                print("Link has all ready been extracted in extracted list memory")
                continue
              
            if not url in links:
                if (link != url):
                    links.append(link)
                    print(link)
            
        return links
    except:
        print('MAJOR EXCEPTION - extract()')
        return None

def save_urls(urls, file_name): 
    # write url in visited site file
    with open(file_name, "w", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                file.write(url + "\n") 
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

# Start image spider/miner program
start_image_miner()