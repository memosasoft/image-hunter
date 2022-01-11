
import webbrowser
from os import truncate
from urllib.parse import urlunparse
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search
from bs4 import BeautifulSoup
import requests, lxml

memory = []
ua = UserAgent()

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
    # search(str: term, int: num_results=10, str: lang="en")
    
    i_counter = 1
    for url in search(query, 50, lang="en"):
        listUrl.append(url)
        # print(str(i_counter) + " - " + url)
        i_counter = i_counter + 1

    return listUrl

def search_bing(query):

    global listUrl
    
    if(query == None) or (query == ""):  
        return listUrl
    
    query = query.replace(" ", "+")

    url = 'https://www.bing.com/search?q=' + query
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    url = url.replace(" ","+")
    
    page = requests.get(url, headers={'User-Agent': custom_user_agent}, timeout=105)  
    html_file = page.text
    
    vidlinks = re.findall("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html_file) #find all between the two parts in the data

    for rc in vidlinks:
         url1, url2, url3 = rc
         url = url1 + "://" + url2 + url3
         if url != None:
            listUrl.append(str(url))
        
    return listUrl

import re
    
def search_yahoo(query):
    list_x = []
    html = requests.get('https://search.yahoo.com/search?p='+ query + "&fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8" ,headers={'User-Agent': ua.random}, timeout=10)
    vidlinks = re.findall("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", html.text) #find all between the two parts in the data

    for rc in vidlinks:
        try:
            #print("URL FOUND")
            url1, url2, url3 = rc
            url = url1 + "://" + url2 + url3
            #print("URL: " + url)
            if url != None:
                list_x.append(str(url))
        except:
            pass
    return list_x

def open_web(url):  # first import the module
    webbrowser.open(url)