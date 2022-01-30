
import requests
import image_miner as miner


memory = []

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

listUrl = []

def search_google(query):
    # will contain de search URL's
    # print("Starting with Google Search")
    # googlesearch-python 1.0.1
    # https://pypi.org/project/googlesearch-python/
    # list = search(str: term, int: num_results=10, str: lang="en")
    #for url in search(query, 40, lang="en"):
    query = query.replace(" ","+")
    query = query.replace("++","+")
    urls = []
    try:
        from googlesearch import search
        for j in search(query, num=10, stop=10, pause=5):
            print(j)
            urls.append(j)
    except ImportError:
        print("No module named 'google' found")
    except:
        pass
    return urls

def search_yandex(query):
    url = 'https://yandex.com/search/?text=' + query + "&lr=103616"
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:45.0) Gecko/20100101 Firefox/47.0"
    
    page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
    html_file = page.text
    vidlinks = re.findall("(http|ftp|https|www):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html_file) #find all between the two parts in the data
    final = extract_link(vidlinks)
    return final


def search_bing(query):
    query = query.replace(" ", "+")
    url = 'https://www.bing.com/search?q=' + query + "&form=QBLH&sp=-1&pq=" + query+ "&sc=9-8&qs=n&sk=&cvid=0CA2568E657449DB85DDC78EA7C248CE&rdr=1&rdrig=2C1AEA4D33FA44DBA6D797B0BA909C87"
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:45.0) Gecko/20100101 Firefox/47.0"
    
    page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
    html_file = page.text
    vidlinks = re.findall("(http|ftp|https|www):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html_file) #find all between the two parts in the data
    final = extract_link(vidlinks)
    return final

import re
    
def search_duck(query):
    url = 'https://duckduckgo.com/?t=ffab&q='+ query + "&atb=v305-1&ia=web"
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:45.0) Gecko/20100101 Firefox/47.0"
    page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
    vidlinks = re.findall("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", page.text) #find all between the two parts in the data
    final = extract_link(vidlinks)
    return final


def search_yahoo(query):
    
    url = 'https://search.yahoo.com/search?p='+ query + "&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8"
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:45.0) Gecko/20100101 Firefox/47.0"
    page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
    vidlinks = re.findall("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", page.text) #find all between the two parts in the data
    final = extract_link(vidlinks)
    return final

def extract_link(links_blob):
       
    final = []

    for i in links_blob:
        #print(i)
        new_url = ""
        for x in i:
            new_url = new_url + x
        
        new_url = new_url.replace("https","https://")
        new_url = new_url.replace("httpwww","http://www")
        new_url = new_url.replace("://://","://")
        
        #result = miner.check_stop_words_in_urls(xx)
        #if result:
        #    continue
        # We want links not images
        if not check_if_image(new_url):
            final.append(new_url)
            print(new_url)
    
    return final

def check_if_image(url):
    check = ["/2000/svg","1999/xhtml",".jpeg",".jpg","bing","live","yandex","captcha","google","yahoo","microsoft",".gif",".png",".svg",".js",".css","#", "sp.yimg.com","help.yahoo.com", "cbclk2","//search.yahoo.com/search"]

    for chk in  check:
        if (url.find(chk)>=0):
            MAX_URL_SIZE = 170
            if len(url)<MAX_URL_SIZE:
                return True  

    

    return False