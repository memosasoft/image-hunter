from cv2 import minAreaRect

wiki_data = []


def get_title(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title != None:
        title = soup.title.get_text()
        return title
    return None

def get_text(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    if soup.body != None:
        text = soup.body.get_text()
        return text
    return None

def search_wiki(query):
    import image_miner as miner
    # need to be properly programmed
    query = " wikipedia " + query + " wikipedia description"
    query = miner.prepare_query(query)   
    search_urls = miner.get_search_urls(query)

    for i in search_urls:
        if i.find("wikipedia")>=0:
            pass
        else:
            search_urls.remove(i)
    return search_urls

def extract_title_from_url(html):
    title = get_title(html)
    return title

def extract_text_from_url(html):
    text = get_text(html)
    return text

def request(url):
    import requests  # to get image from the web
    
    try:
        r = requests.get(str(url),  timeout=10)
        return r
    except:
        try:
            r = requests.get(str(url),  timeout=10)
            return r
        except:
            pass
    return None

def get_information(query):
    import image_miner as miner
    global wiki_data
  
    urls = search_wiki(query)  

    for url in urls:
        page = request(url)

        if page!=None:
        
            title = extract_title_from_url(page.text)
            text = extract_text_from_url(page.text)
            if (text != None):
                while text.find("\n")>=0: text.replace("\n"," ")
            save_information(query, title, text)
    
    for i in wiki_data:
        if len(i) < 160:
            wiki_data.remove(i)

    wiki_data.sort()
    wiki_data = miner.save_list(wiki_data, "./intelligence/wiki_data")


def save_information(query, title, text):
    import image_miner as miner
 
    global wiki_data
    if query != None and title != None and text != None:
        data = str(title) + ' : ' + str(text)
        wiki_data.append(data)
    
def generate_text(query, length):
    import image_miner as miner
    global wiki_data
    wiki_data = miner.load_list("./intelligence/wiki_data", wiki_data)
    wiki_data.sort()
    text = []
    for i in wiki_data:
        if len(i) < 100:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find("]")>=0:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find("}")>=0:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find("\\")>=0:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find(";")>=0:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find("==")>=0:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find("!=")>=0:
            wiki_data = wiki_data.remove(i)
            continue
        if i.find(query[0:int(len(query)/2)])>=0:
            text.append(i)

    wiki_data = miner.save_list(wiki_data, "./intelligence/wiki_data")
    print(text)
