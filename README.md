**Image-Hunter**
The new name for Image-Miner

Image-Hunter is an AI project. It implements ideas about autonomous agents, machine learning, natural language processing and many other artificial intelligence topics that are of interest. Some of the ideas being developed in this project have been in my head for more than 25 years. They come from my work in IT. I had the privilege to work with many gifted engineers and developers and I've been in contact with these ideas for a long time. The project is evolving very quickly.

Image-Hunter is more and more a search engine than a simple scraper. It has new features that enable users to search the net in BAZOOKA mode.

**BAZOOKA MODE**
You can spider hundreds of websites for a quick summary and for now image retrieval needs and web page content. This is not recommended because in the long term you will be penalized and blocked and even maybe hacked. It is better to go slow and gather the information with patience.

**WEB INTERFACE**
I added many web interface views giving the scrapper the ability to search a subject through a basic written image search. You just enter a query or phrase and the system retrieves the information related to your search query. The HTML views will popup when the image-hunter.py script is started. The interface is in development and will use JavaScript. I want an advanced image viewing interface.

If you have suggestions I am very open.  I also welcome any help in the project. This is a learning project too. Well my philosophy is that everything is a learning project. I will soon package everything and prepare installation documentation for quick installation of the scraper-spider.

The system is slowly becoming a search engine. It was the goal of the image retrieval project.

**INSTALLING THE SOFTWARE**
Image-hunter is the new name of Image-miner

https://github.com/memosasoft/image-miner

OPTIMAL CONFIG

The scraper-spider does an excellent job when it downloads everything flag is active

DOWNLOAD_EVERYTHING = ON

Also watch these parameters. Images under 1500 kb are not very interesting and lack resolution.

MAX_WORKSPACE_SIZE = 900000
MIN_IMAGE_SIZE = 5000
MIN_QUALITY_IMAGE_SIZE = 30000

The best strategy is to download everything and then let the intelligence make the best selection it can.

The images that are not selected by AI are stored in the workspace directory in the archives folder. 

**AI STRATEGIES**

It verifies many things like : tag info, path keywords, image keywords, page content and more...

The only thing missing is the VISION module.

**Miner features and functionality**

    Works with Google, Yahoo and Bing
    It learns from web site and user input
    It check link, images alt tag, images filename and web page path
    It has a simple scoring system QS (Quality Score)
    It extracts and reads html content
    It as an simple html interface
    It as a database to keep track of information
    It build a depot of all images
    It keeps a history

There is also one config.env file that lets you play with the parameters of the scrapper.

Note don't forget to change the PROGRAM_PATH

PROGRAM_PATH = file:///home/linux/Bureau/Programmation/image-miner-X/dev/image-hunter.html

**WEB SERVER ON THE WAY**
Web server version is being implemented.  

**Supported Image formats**
psd,apng,avif,bmp,gif,ico,cur,tif,tiff,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp,webm,ogg,wav,tiff,ico,jpg,gif,png,bmp

**Database with SQLite3**
Database Integration is completed with sqlite.

**Image depot**
During testing in the past 4 weeks it gathers : 85000 images and icons.

**Learning to learn**
More intelligence is on the way...

**MY WISH LIST for 2022**

    Search library optimization
    Automatic Search Results
    Archiving development  
    DB development
    Vision development
    Enhance AI  
    Smarter search algorithms
    Better roaming and crawling

**NEXT PHASE**
Image-Hunter will have the ability to judge the quality of an image. It already does a very impressive job with no visual information.

When the vision algorithm will be ready the software will do an amazing job.
