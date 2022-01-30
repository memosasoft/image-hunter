**Image-Miner**

Image-Miner is an AI project. It is evolving very quickly. It has new features that enable users to search the net in BAZOOKA mode. You can spider hundreds of websites for a quick summary and for image retrieval needs. I added many web interfaces view giving the scrapper the ability to search a subject through a basic image search. The interface is in developpement and will be use Javascript.

The scrapper does an excellent job when it downloads everything flag is active

DOWNLOAD_EVERYTHING = ON

Also watch these parameters. 
Images under 1500 kb a not very intresting aand lack resolution.

MAX_WORKSPACE_SIZE = 900000
MIN_IMAGE_SIZE = 5000
MIN_QUALITY_IMAGE_SIZE = 30000

The scraper-spider then makes a selection thanks to the AI tools that are still being developed.

It verifies many thing like : tag info, path keywords, image keywords, page content and more...

The only thing missing is the VISION module.

It is every day more and and more a smart image scraper-spider and basic search engine. 

But it is getting more complexe and bugs are being slipts in...

Still need more testing and developpement.

**Search Engine**

It uses Google, Bing and Yahoo.

It's like using a search engine: you make a query and the scraper collects images that fit your query. 

Basically it verifies keyword signature in html content, image filename, image path and image alt information. 

It also has multiple verification and strategies for url spidering. 

I am also working on some intelligence and learning abilities. I connected the scraper to nltk and the system is building a definition dictionary, keyword relations, and learning from web pages content and queries. 

The system also keeps history for learning purposes. 

I also want to develop a profile component that will contain user specific information to guide the searching process. 

**Miner features and functionality**
- Works with Google, Yahoo and Bing 
- It learns from web site and user input 
- It check link, images alt tag, images filename and web page path 
- It has a simple scoring system QS (Quality Score)
- It extracts and reads html content
- It as an simple html interface
- It as a database to keep track of information
- It build a depot of all images 
- It keeps a history

There is also one config.env file that lets you play with the parameters of the scrapper.

[CONFIG]
ANALYSIS_MAX_WORDS = 1000
DEEP_ANALYSIS = OFF
PREVIEW_SIZE = 500

QUALITY_SCORE = 12
KEYWORDS_IN_LINK = ON
NUMBER_OF_KEYWORDS_IN_LINK = 1
LEARNING_TFQST = 40
LEARN_TO_BLOCK_URL = 0
IMG_ALT_VERIFICATION = ON
IMG_ALT_QS = 4

MATCH_BOOST = OFF
SEARCH_BOOST = OFF
QUERY_BOOST = OFF

DOWNLOAD_HTML = ON
MAX_WORKSPACE_SIZE = 900000
MIN_IMAGE_SIZE = 5000
MIN_QUALITY_IMAGE_SIZE = 30000
DIG_FOR_URLS = OFF
DOWNLOAD_EVERYTHING = ON
SPIDER_ALL_IMAGES = ON
SAVE_SUBJECT_KEYWORDS = ON

MIN_URL_SIZE = 10
MIN_STEM_SIZE = 3
MIN_WORD_SIZE = 2
MAX_WORD_SIZE = 20
MIN_PATTERN_SIZE = 4
LONG_KEYWORD_SIZE = 18
MAX_URL_SIZE = 170
MAX_FILE_NAME_SIZE = 80

TIME_LOCK = 5
STEP_SCAN = 3
SAVE_CYCLE = 10

DEBUG_CONSOLE = ON
DEBUG_LOG = OFF

CLEAN_START = ON
FREELY_GRAB_URLS = ON

RANDOM_START = 200
URL_LIMIT_AMOUNT = 1000
HTML_IMAGE_PER_PAGE = 50
NB_OF_SITE_TO_SPIDER = 100

PROGRAM_PATH = file:///home/linux/Bureau/Programmation/image-miner-X/dev/image-hunter.html

Web server version is being implemented.
 
**Signature matching keywords**

It matches keywords with multiple pattern hits that are simple sections of the keyword. 

Top performance depends on many factors but with a quality score of about 20 and decent queries the results are very impressive. As long as the search results are good the scrapper does an amazing job. 

The pattern matching works really well.

**Supported Image formats**
psd,apng,avif,bmp,gif,ico,cur,tif,tiff,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp,webm,ogg,wav,tiff,ico,jpg,gif,png,bmp

**Database with SQLite3**
Database Integration is completed with sqlite.

**Image depot**
During testing in the past 4 weeks it gathers : 85000 images and icons. 

**Learning to learn**
More intelligence is on the way...

**MY WISHLIST for 2022**
- Better search results
  -  Search API   
- Vision developpement 
- Enhance AI
  - Better searching
  - Better roaming 

**NEXT PHASE**
Image-Miner will have the ability to judge the quality of an image. It all ready does a very impressive job with no visual information. 

When the vision algorithm will be ready the software will do an amazing job.

**IMAGE-MINER IN ACTION**
Visit the web site to view some of the images Image-Miner found during the testing phase of the project. 

**Visite our Website**
https://image-miner.weebly.com/
