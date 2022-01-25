# -*- coding: UTF-8 -*-
#!/usr/bin/env python
def main(query):
    miner.main(query)

def start_html():
    return '<html>'

def end_html():
    return '</html>'

def print_html(text):
    text = str(text)
    text = text.replace('\n', '<br>')
    return '<p>' + str(text) + '</p>'

if __name__ == '__main__':
    import sys
    import threading
    import image_miner as miner
    query_memory = ""
    while (True):

        print("In the loop waiting...")
        
        file = open("data.txt", "r")
        query = file.readlines()
    
        try:
                
            if (query_memory != query):
                #Created the Threads
                t1 = threading.Thread(target=main(query[len(query)-1]))
                t1.run()
                t1.join()
                t1.isDaemon(True)
        except:
            pass
        miner.relax(1)
        query_memory = query
    

