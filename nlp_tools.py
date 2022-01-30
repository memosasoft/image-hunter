from bs4 import BeautifulSoup

import nltk
from nltk.corpus import stopwords
#nltk.download('wordnet')
#nltk.download('omw-1.4')
def get_content_freq(text):
    
    WORD_FRQ = 5
    WORD_MIN = 6
    WORD_MAX = 14
    
    stopwords.words('english')

    tokens = [t for t in text.split()]

    clean_tokens = tokens[:]

    sr = stopwords.words('english')

    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
        else: 
            if len(token) <= WORD_MIN or len(token) >= WORD_MAX:
                clean_tokens.remove(token)
            
    freq = nltk.FreqDist(clean_tokens)

    for key,val in freq.items():
        if val >= WORD_FRQ:
            if len(key) >= WORD_MIN:
                if len(key) <= WORD_MAX:
                    print(str(key) + ':' + str(val))
                
    freq.plot(20, cumulative=False)
    
def definition(keyword):
    from nltk.corpus import wordnet
    syn = wordnet.synsets(keyword)
    list = []
    for s in syn:
        list.append(s.definition())
    
    return list
    
    from nltk.corpus import wordnet

def synonyms(keyword):
    
    from nltk.corpus import wordnet   
    synonyms = []

    for syn in wordnet.synsets(keyword):

        for lemma in syn.lemmas():

            synonyms.append(lemma.name())

    return synonyms
    
    
    from nltk.corpus import wordnet

def antonyms(keyword):
    
    from nltk.corpus import wordnet   
    
    antonyms = []

    for syn in wordnet.synsets(keyword):

        for l in syn.lemmas():

            if l.antonyms():

                antonyms.append(l.antonyms()[0].name())

    print(antonyms)
    
def stem(keyword):
    from nltk.stem import PorterStemmer
    
    stemmer = PorterStemmer()
    
    return stemmer.stem(keyword)
        
#fa_url("https://en.wikipedia.org/wiki/Napoleon")
#fa_url("https://en.wikipedia.org/wiki/Military_simulation")
#fa_url("https://en.wikipedia.org/wiki/Frederick_W._Lanchester")

word = "IQ"


