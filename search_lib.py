
import webbrowser
from os import truncate
from urllib.parse import urlunparse
from urllib.request import Request, urlopen

import lxml
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search

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

    print("Starting with Google Search")

    # googlesearch-python 1.0.1
    # https://pypi.org/project/googlesearch-python/
    # search(str: term, int: num_results=10, str: lang="en")
    i_counter = 1
    for url in search(query, 20, lang="en"):
        listUrl.append(url)
        # print(str(i_counter) + " - " + url)
        i_counter = i_counter + 1

    return listUrl

def search_bing(query):
    url = 'https://www.bing.com/search?q=' + query
    custom_user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

    url = url.replace(" ","+")
    req = Request(url, headers={"User-Agent": custom_user_agent})
    page = urlopen(req)

    soup = BeautifulSoup(page.read(),features="lxml")
    links = soup.findAll("cite")

    for i in links:
        #print("FIRST LEVEL")
        # print(str(i))
        tampon = str(i)

        tampon = tampon.replace("<strong>", "")
        tampon = tampon.replace("</strong>", "")
        tampon = tampon.replace("<cite>", "")
        tampon = tampon.replace("</cite>", "")

        # Print the soup tag
        #print("GOT THE LINK")
        #print(tampon)
        listUrl.append(tampon)
    return listUrl

# MIX search
def xsearch(query):

    print("Entering Mix Search")
    print("Top search from")
    print("Google, Bing and Yahoo")

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
    
    print("Exiting Mix Search")
    print("Thank you")
    print("Google, Bing and Yahoo")

    return listUrl

def search_yahoo(query):

    html = requests.get('https://search.yahoo.com/search?p=' +
                        query+' 5', headers=headers, ).text
    soup = BeautifulSoup(html, 'lxml')

    for result in soup.find_all('div', class_='layoutMiddle'):
        title = result.find('h3', class_='title tc d-ib w-100p')
        link = result.find('h3', class_='title tc d-ib w-100p')
        displayed_link = result.select_one('.compTitle div')
        snippet = result.find('div', class_='compText aAbs')
        #print("title: " + title)
        #print("\n\n\nlink: " + link)
        #print("\n\n\ndisplayed_link: " + displayed_link)
        #print("\n\n\nsnippet: " + snippet)
        listUrl.append(link)
    
    return listUrl

def open_web(url):  # first import the module
    webbrowser.open(url)

query = input("What are you looking for? ")

# working
search_google(query)

# working
search_yahoo(query)

# working
search_bing(query)

print("PRINTING ALL SEARCHE RESULTS")

for i in listUrl:
    print(i)
# not tested
# search_yahoo_organic_results(query)
