
from image_miner import MIN_WORD_SIZE
from image_miner import MAX_WORD_SIZE

def clean_keywords_lists():
    import os
    your_path = './intelligence/keywords_memory/'
    files = os.listdir(your_path)

    keywords = []
    for file in files:
        if os.path.isfile(os.path.join(your_path, file)):
            f = open(os.path.join(your_path, file),'r')
            for x in f:
                for keyword in x.split(" "):
                    if not keyword in keywords:
                        if (len(keyword)<=MIN_WORD_SIZE):
                            continue
                        
                        if (len(keyword)>=MAX_WORD_SIZE):
                            continue
                        import image_miner as miner
                        stop_words = []
                        stop_words = miner.load_list("./intelligence/stop_words", stop_words)
                        if keyword in stop_words:
                            continue
                        keywords.append(keyword.replace("\n", ""))
            f.close()

            f = open(os.path.join(your_path, file),'w')

            keywords.sort()
            for keyword in keywords:
                f.write(keyword + "\n")

            f.close()
    pass


def clean_lists_of_keyword(keyword):
    import image_miner as miner
    learned_keywords = []
    learned_keywords = miner.load_list("./intelligence/learned_keywords", learned_keywords)
    for i in learned_keywords:
        for t in i.split(' '):
            if t == ' ' or t == '' or t == None:
                continue
            if t[0:int(len(t))] == keyword[0:int(len(t))]:
                learned_keywords.remove(i)

                i = i.replace(t," ")
                i = miner.clean_text(i)
                learned_keywords.append(i)
            
    learned_keywords.sort()
    learned_keywords = miner.save_list(learned_keywords, "./intelligence/learned_keywords")
    
    learned_relations = []
    learned_relations = miner.load_list("./intelligence/learned_relations", learned_relations)
    for i in learned_relations:
        for t in i.split(' '):
            if t == ' ' or t == '' or t == None:
                continue
            if t[0:int(len(t))] == keyword[0:int(len(t))]:
                learned_relations.remove(i)

                i = i.replace(t," ")
                i = miner.clean_text(i)
                learned_relations.append(i)
    learned_relations = miner.save_list(learned_relations, "./intelligence/learned_relations")  

def sorting():
    import image_miner as miner
    learned_relations = []
    learned_relations = miner.load_list("./intelligence/learned_relations", learned_relations)
    learned_relations.sort()
    learned_relations = miner.save_list(learned_relations, "./intelligence/learned_relations")
    
    dictionary = []
    dictionary = miner.load_list("./intelligence/dictionary", dictionary)
    dictionary.sort()
    dictionary = miner.save_list(dictionary, "./intelligence/dictionary") 
    
    stop_urls = []
    stop_urls = miner.load_list("./intelligence/stop_urls", stop_urls)
    stop_urls.sort()
    stop_urls = miner.save_list(stop_urls, "./intelligence/stop_urls") 
    
    stop_urls = []
    stop_urls = miner.load_list("./intelligence/stop_urls", stop_urls)
    stop_urls.sort()
    stop_urls = miner.save_list(stop_urls, "./intelligence/stop_urls") 

    learned_relations = []
    learned_relations = miner.load_list("./intelligence/learned_relations", stop_urls)
    learned_relations.sort()
    learned_relations = miner.save_list(learned_relations, "./intelligence/learned_relations") 
     
def search_keywords_in_file(keyword):
    import os
    your_path = './intelligence/keywords_memory/'
    files = os.listdir(your_path)
    keyword = 'your_keyword'
    for file in files:
        if os.path.isfile(os.path.join(your_path, file)):
            f = open(os.path.join(your_path, file),'r')
            for x in f:
                if keyword in x:
                    return True
            f.close()
    return False

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search
# Fake user agent 
ua = UserAgent()

def get_related_word(keyword):
    
    try:
        list_related_keywords = []
        url = "https://wordtype.org/of/"+keyword
        page = requests.get(str(url), headers={
            'User-Agent': ua.random}, timeout=20)

        if page.status_code == 200:
            print(page.text)
            soup = BeautifulSoup(page.text, 'html.parser')
            raw = soup.find_all('div', class_='term').text
            print(raw)


        else:
            pass
    except:
        #x_print(e)
        pass
    

def search_query_history(query):
    pass

def search_learned_keywords(query):
    pass

def learn_from_query_history(query):
    pass

def learn_from_learned_keywords(query):
    pass

#clean_keywords_lists()
sorting()
#clean_lists_of_keyword("yahoo")
#clean_lists_of_keyword("search")
#clean_lists_of_keyword("results")
#clean_lists_of_keyword(" - ")
#clean_lists_of_keyword(",")
#clean_lists_of_keyword("google")
#clean_lists_of_keyword("microsoft")
get_related_word("art")