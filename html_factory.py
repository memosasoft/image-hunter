# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from selenium import webdriver as driver
import configparser
import mimetypes  # needed for download functionality
import os
import shutil  # to save it locally
import sys
import time
# Importing Necessary Modules
import urllib.request
import uuid
import webbrowser
from distutils.command.config import dump_file
from random import random
from re import I
from sqlite3 import Error

import requests  # to get image from the web
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from googlesearch import search
from nturl2path import url2pathname

# Session url and img global_memory
urls_global_session_memory = []
images_seesion_memory = []

current_root_url = ""
current_url = ""
current_title = ""
current_html = ""
current_text = ""
current_preview = ""
current_img_keywords = ""
current_http_src = ""
current_img_src = ""
current_query = ""
current_patterns_hits = ""
current_img_size = 0
current_description = ""
current_image_alt_text_test = ""

proxies = {
    'http': '192.168.0.58:8080',
    'https': '192.168.0.58:443',
}

media_files = "psd,apng,avif,bmp,gif,ico,cur,tif,tiff,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp,webm,ogg,tiff,ico,jpg,gif,png,bmp"

html_file_name = str(uuid.uuid4())
html_img_counter = 0

img_count = 0
url_count = 0
save_count = 0
spidered_site_count = 0
approch_counter = 0

query_size = 0
quality_score = 0

# Program url buffers
urls_buffer = []  # long-term buffer =
urls_visited = []  # visited_links
urls_images = []

urls_problems = []


proxies_list = []
proxy_good = False

# search urls from google
search_urls = []

# SORRY STILL WORKING
# IN DEVELOPPEMENT
# Ideas to cheat intelligence
# adding specific keywords under de hood
# to get better searching and matching
search_boost = [
    "photo,image,picture,gallery,wallpaper,art,digital,svg,jpg,jpeg"]
match_boost = [
    "photo,image,picture,gallery,pic,art,digital,svg,jpg,jpeg,web,ogg,gif,png,bmp"]

match_query = ""
pattern_memory = []

# keywords container for query
query_history = []

# Learning component
dictionary = []
synonyms = []
learned_relations = []
spam_filter = []

# Learning array for text the system reads
learned_keywords = []

# Fake user agent
ua = UserAgent()
user_profil = []

# stop words and urls
stop_words = []
stop_urls = []

spidered_site_count = 0

configuration = configparser.ConfigParser()
configuration.read('config.env')

CLEAN_START = str(configuration.get('CONFIG', 'CLEAN_START'))
TIME_LOCK = float(configuration.get('CONFIG', 'TIME_LOCK'))

QUALITY_SCORE = float(configuration.get('CONFIG', 'QUALITY_SCORE'))
KEYWORDS_IN_LINK = str(configuration.get('CONFIG', 'KEYWORDS_IN_LINK'))
NUMBER_OF_KEYWORDS_IN_LINK = int(configuration.get(
    'CONFIG', 'NUMBER_OF_KEYWORDS_IN_LINK'))
MIN_URL_SIZE = int(configuration.get('CONFIG', 'MIN_URL_SIZE'))
MAX_URL_SIZE = int(configuration.get('CONFIG', 'MAX_URL_SIZE'))
MAX_WORD_SIZE = int(configuration.get('CONFIG', 'MAX_WORD_SIZE'))
MIN_WORD_SIZE = int(configuration.get('CONFIG', 'MIN_WORD_SIZE'))
MIN_STEM_SIZE = int(configuration.get('CONFIG', 'MIN_STEM_SIZE'))
LONG_KEYWORD_SIZE = int(configuration.get('CONFIG', 'LONG_KEYWORD_SIZE'))
MIN_PATTERN_SIZE = int(configuration.get('CONFIG', 'MIN_PATTERN_SIZE'))

NB_OF_SITE_TO_SPIDER = int(configuration.get('CONFIG', 'NB_OF_SITE_TO_SPIDER'))
IMG_ALT_VERIFICATION = str(configuration.get('CONFIG', 'IMG_ALT_VERIFICATION'))
IMG_ALT_QS = int(configuration.get('CONFIG', 'IMG_ALT_QS'))
STEP_SCAN = int(configuration.get('CONFIG', 'STEP_SCAN'))

LEARNING_TFQST = int(configuration.get('CONFIG', 'LEARNING_TFQST'))
LEARN_TO_BLOCK_URL = int(configuration.get('CONFIG', 'LEARN_TO_BLOCK_URL'))
DOWNLOAD_EVERYTHIING = str(configuration.get('CONFIG', 'DOWNLOAD_EVERYTHIING'))
DEEP_ANALYSIS = str(configuration.get('CONFIG', 'DEEP_ANALYSIS'))
ANALYSIS_MAX_WORDS = int(configuration.get('CONFIG', 'ANALYSIS_MAX_WORDS'))
SPIDER_ALL_IMAGES = str(configuration.get('CONFIG', 'SPIDER_ALL_IMAGES'))

SEARCH_BOOST = str(configuration.get('CONFIG', 'SEARCH_BOOST'))
MATCH_BOOST = str(configuration.get('CONFIG', 'SEARCH_BOOST'))
QUERY_BOOST = str(configuration.get('CONFIG', 'QUERY_BOOST'))

PREVIEW_SIZE = int(configuration.get('CONFIG', 'PREVIEW_SIZE'))
DOWNLOAD_HTML = str(configuration.get('CONFIG', 'DOWNLOAD_HTML'))
HTML_IMAGE_PER_PAGE = int(configuration.get('CONFIG', 'HTML_IMAGE_PER_PAGE'))
SAVE_CYCLE = int(configuration.get('CONFIG', 'SAVE_CYCLE'))
MIN_IMAGE_SIZE = int(configuration.get('CONFIG', 'MIN_IMAGE_SIZE'))
MAX_FILE_NAME_SIZE = int(configuration.get('CONFIG', 'MAX_FILE_NAME_SIZE'))
DEBUG_CONSOLE = str(configuration.get('CONFIG', 'DEBUG_CONSOLE'))
DEBUG_LOG = str(configuration.get('CONFIG', 'DEBUG_LOG'))
FREELY_GRAB_URLS = str(configuration.get('CONFIG', 'FREELY_GRAB_URLS'))
MAX_WORKSPACE_SIZE = int(configuration.get('CONFIG', 'MAX_WORKSPACE_SIZE'))
MIN_QUALITY_IMAGE_SIZE = int(configuration.get(
    'CONFIG', 'MIN_QUALITY_IMAGE_SIZE'))
URL_LIMIT_AMOUNT = int(configuration.get('CONFIG', 'URL_LIMIT_AMOUNT'))
SAVE_SUBJECT_KEYWORDS = str(configuration.get(
    'CONFIG', 'SAVE_SUBJECT_KEYWORDS'))

RANDOM_START = int(configuration.get('CONFIG', 'RANDOM_START'))
DIG_FOR_URLS = str(configuration.get('CONFIG', 'DIG_FOR_URLS'))
PROGRAM_PATH = str(configuration.get('CONFIG', 'PROGRAM_PATH'))
PROXY_ACTIVATED = 'OFF'

def x_print(data):
    # consol, log file and interface
    if DEBUG_CONSOLE == "ON":
        print(data)
    if DEBUG_LOG == "ON":
        debug_info(data)


def debug_info(info):
    # print to screen
    from datetime import datetime
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = open("debug", "a")
    f.write("\n" + str(time))
    f.write(str(info))
    f.close()


def first_dump(current_query):
    html = ""
    html = html = '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="30" /><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>'
    html = html + '<center><form action = "search.html" method = "POST"><input type = "submit" value = "Let go again!!!"></form><br></center>'
    html = html + '<center>Results for ' + current_query + \
        '</center><br><center>The system is searching real-time the net, learning and thinking...</center><br><br></body></html>'

    html_code = '<!DOCTYPE html><html lang="en"><body><center><h1>Image-Hunter</h1><h4>Playing around for learning reasons<br>with AI and Images</h4><img src="NpTzUs.webp" style="display:inline-block;width:500px;height:auto;object-fit:contain;" border="2"><p>The page will refresh when results are ready.</p><p>Or follow this <a href="../interface/">link </a><p><a href="image-hunter-img-view.html">Image view </a>, <a href="image-hunter.html">Detailed view </a>or <a href="image-hunter-search.html">Search Results</p></form></center></body></html>'
    f = open("./dev/image-hunter.html", "w")
    f.write(str(html_code))
    f.close()

    f = open("./dev/image-hunter-original.html", "w")
    f.write(str(html_code))
    f.close()

    f = open("./dev/image-hunter-img-view.html", "w")
    f.write(str(html_code))
    f.close()

    f = open("./dev/image-hunter-search.html", "w")
    f.write(str(html_code))
    f.close()

def dump_html(img, img_src):
    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_size
    global current_query
    global current_root_url
    global html_file_name
    global html_img_counter
    global current_patterns_hits

    query_foler = current_query.replace(" ", "-")

    if HTML_IMAGE_PER_PAGE < html_img_counter:
        closing_html_dump(img_src, current_url)
        html_img_counter = 0
        html_file_name = str(uuid.uuid4())
        current_query = query_history[0]
        query_foler = current_query.replace(" ", "-")

    html_img_counter = html_img_counter + 1

    # GLOBAL THUMBNAIL VIEW
    #file_name = str(uuid.uuid4())
    # dump_thumbnail_html(img_src,file_name)

    html = '<a href="' + img_src + '"><img border="2" src="' + img_src + \
        '" style="display:inline-block;width:15%;height:15%;object-fit:contain;" /></a>'
    f = open("./interface/global-view-" + html_file_name+".html", "a")
    f.write(str(html))
    f.close()

    closing_html_dump(img_src, current_url)

    global current_image_alt_text_test
    hit = False

    if (current_image_alt_text_test == True) and (MIN_QUALITY_IMAGE_SIZE < current_img_size):
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-BEST-IMG-SIZE-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (current_image_alt_text_test == True):
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (MIN_QUALITY_IMAGE_SIZE < current_img_size):
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BIG-SIZE-"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if quality_score > IMG_ALT_QS and MIN_QUALITY_IMAGE_SIZE < current_img_size:
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BIG-SIZE-TEXT-ALT-MATCH-QS-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if quality_score > IMG_ALT_QS:
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/TEXT-ALT-MATCH-QS"+html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if quality_score > IMG_ALT_QS and current_image_alt_text_test == True and MIN_QUALITY_IMAGE_SIZE < current_img_size:
        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/SIZE-TEXT-ALT-MATCH-" +
                 html_file_name+".html", "a")
        f.write(str(html))
        f.close()

        hit = True

    if (hit == True):

        html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
        f = open("./interface/BEST-RESULTS-" + query_foler +
                 "-" + html_file_name + ".html", "a")
        f.write(str(html))
        f.close()

        if img.find("webp") >= 0:
            shutil.copy(img, "./dev/NpTzUs.webp")

        html = '<center><a href="' + current_root_url + '"><img src="' + img_src + ' " alt="' + current_preview + \
            '" style="display:inline-block;width:40%;height:auto;object-fit:contain;"></a></center>'
        html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + current_root_url + \
            '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + \
            current_img_keywords.upper() + " [...] " + '</center>'
        f = open("./dev/results.html", "a")
        f.write(str(html_code))
        f.close()

        html_code = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
            '" style="display:inline-block;width:14%;height:14%;object-fit:contain;" /></a>'
        f = open("./dev/image-hunter-img-view.html", "a")
        f.write(str(html_code))
        f.close()

        html = '<center><a href="' + current_root_url + '"><img src="' + img_src + ' " alt="' + current_preview + \
            '" style="display:inline-block;width:40%;height:auto;object-fit:contain;"></a></center>'
        html_code = html + '<center><b>TITLE: ' + current_title.capitalize() + '</b></center><center><a href="' + current_root_url + \
            '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + \
            current_img_keywords.upper() + " [...] " + '</center>'
        f = open("./dev/image-hunter.html", "a")
        f.write(str(html_code))
        f.close()

        html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + \
            '</b></center><a href="' + current_root_url + \
            '">' + current_root_url + '</a></center>'
        f = open("./dev/image-hunter-search.html", "a")
        f.write(str(html_code))
        f.close()

    html = '<a href="' + img_src + '"><img  border="2" src="' + img_src + \
        '" style="display:inline-block;width:180px;height:180px;object-fit:contain;" /></a>'
    f = open("./interface/EVERYTHING-" + query_foler +
             "-" + html_file_name + ".html", "a")
    f.write(str(html))
    f.close()


def closing_html_dump(img_src, url):

    global current_title
    global current_url
    global current_root_url
    global current_query
    global current_text
    global current_img_src
    global current_img_keywords
    global current_patterns_hits
    global quality_score

    html = '<center><a href="' + current_root_url + '"><img border="1" src="' + img_src + \
        '" style="display:inline-block;width:50%;height:50%;object-fit:contain;" /></a></center>'
    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + \
        current_root_url + '">' + current_root_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + current_img_keywords.capitalize() + " [...] " + '</center><center><b>PREVIEW:</b>' + current_preview.capitalize() + " [...] " + '</center><center><a href="' + \
        img_src + '">' + img_src + '</a></center><br>QUALITY SCORE: ' + str(quality_score) + '<br>QUERY: ' + str(
            current_query) + ' <br>IMAGE Keywords: ' + str(current_img_keywords) + ' <br>PATTERNS: ' + str(current_patterns_hits) + '<div><hr>'
    f = open("./interface/main-" + html_file_name + ".html", "a")
    f.write(str(html_code))
    f.close()


file = str(uuid.uuid4())


def dump_url_html(url):
    global file
    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_keywords
    global html_file_name
    global html_img_counter
    global current_patterns_hits
    global quality_score

    html = '<center><center><b>' + current_title.capitalize() + ' QS SCORE: ' + \
        str(quality_score) + ' </b></center>'
    html_code = html + '<center><a href="' + \
        str(url) + '">' + url + '</a></center><br>'
    #html_code = html + '<center> ' + current_text + '</center>'
    f = open("./interface/URLS-" + file + ".html", "a")
    f.write(str(html_code))
    f.close()

    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + \
        '</b></center><a href="' + current_root_url + \
        '">' + current_root_url + '</a></center>'
    f = open("./dev/image-hunter-search.html", "a")
    f.write(str(html_code))
    f.close()


def dump_thumbnail_html(img_src, file_name):

    global current_title
    global current_url
    global current_text
    global current_img_src
    global current_img_keywords
    global html_file_name
    global html_img_counter
    global current_patterns_hits
    global quality_score

    html = '<center><a href="' + str(img_src) + '.html"><img border="2" src="' + img_src + \
        '" style="display:inline-block;width:25%;height:25%;object-fit:contain;" /></a></center>'
    html_code = html + '<center><center><b>TITLE: ' + current_title.capitalize() + '</b></center><a href="' + \
        current_url + '">' + current_url + '</a></center><center><b>IMAGE KEYWORDS:</b>' + current_img_keywords.capitalize() + " [...] " + '</center><center><b>PREVIEW:</b>' + current_preview.capitalize() + " [...] " + '</center><center><a href="' + \
        img_src + '">' + img_src + '</a></center><br>QUALITY SCORE: ' + str(quality_score) + ' <br>IMAGE Keywords: ' + str(
            current_img_keywords) + ' <br>PATTERNS: ' + str(current_patterns_hits) + '<div><hr>'
    f = open("./interface/" + file_name + ".html", "a")
    f.write(str(html_code))
    f.close()


def intro_html_dump():

    global current_title
    global current_url
    global current_text
    global html_file_name

    html_code = '<link rel="stylesheet" type="text/css" href="../archive/interface/style.css" media="screen" /><div id="main">'
    f = open("./interface/main-" + html_file_name + ".html", "a")
    f.write(str(html_code))
    f.close()

