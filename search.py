
import requests


memory = []

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

listUrl = []

def search_google(query):
    # will contain de search URL's
    global listUrl

    if(query == None) or (query == ""):  
        return listUrl

    # print("Starting with Google Search")
    # googlesearch-python 1.0.1
    # https://pypi.org/project/googlesearch-python/
    # list = search(str: term, int: num_results=10, str: lang="en")
    #for url in search(query, 40, lang="en"):
    query = query.replace(" ","+")
    final = []
    urls = []
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    
    # to search
  
    try:  
        for j in search(query, num=10, stop=30, pause=2):
            print(j)
            urls.append(j)
    except:
        pass
    try:

        for url in search(query, 20, lang="en"):
            urls.append(url)
    except:
        pass
    
    try:

      
        url = 'https://www.google.com/search?q=' + query
        custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        url = url.replace(" ","+")
        
        page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
        html_file = page.text
        vidlinks = re.findall("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html_file) #find all between the two parts in the data
        final = extract_link(vidlinks)
        
        for url in urls:
            final.append()
            print(url)
    except:
        pass
    return final

def search_bing(query):

    global listUrl
    
    if(query == None) or (query == ""):  
        return listUrl
    
    query = query.replace(" ", "+")
    url = 'https://www.bing.com/search?q=' + query + "&form=QBLH&sp=-1&pq=" + query+ "&sc=9-8&qs=n&sk=&cvid=0CA2568E657449DB85DDC78EA7C248CE&rdr=1&rdrig=2C1AEA4D33FA44DBA6D797B0BA909C87"
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:45.0) Gecko/20100101 Firefox/47.0"
    
    page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
    html_file = page.text
    vidlinks = re.findall("(http|ftp|https|www):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html_file) #find all between the two parts in the data
    final = extract_link(vidlinks)
    return final

import re
    
def search_yahoo(query):
    list_x = []
    html = requests.get('https://search.yahoo.com/search?p='+ query + "&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8" , timeout=10)
    vidlinks = re.findall("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html.text) #find all between the two parts in the data
    final = extract_link(vidlinks)
    return final

def extract_link(links_blob):
       
    final = []

    for i in links_blob:
        #print(i)
        xx = ""
        for x in i:
            xx = xx + x
        
        xx = xx.replace("https","https://")
        final.append(xx)
        print(xx)
    
    return final
