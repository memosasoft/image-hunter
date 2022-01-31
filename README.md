**Image-Miner**

Image-Miner is an AI project. It implements ideas about Autonomous Agents, Machine Learning, Natural Language Processing and other Artificial Intelligence topics that interest me and I have an obsession about. Some of these ideas and concepts have been in my head for the past 25 years. 

The project is evolving very quickly. It has new features that enable users to search the net in BAZOOKA mode. 

**BAZOOKA MODE**
You can spider hundreds of websites for a quick summary and for now image retrieval needs and web page content. 

**WEB INTERFACE**
I added many web interface views giving the scrapper the ability to search a subject through a basic image search. This view will popup when the image-miner.py script is started. 

The interface is in developpement and will use Javascript. I want an advanced image viewing interface. 

If you have suggestions I am a very open personne. 

Also welcome any help in the project. 

This is a learning project too 
Well my philosophy is that everything is a learning project. 

I will soon package everything and prepare installation documentation for quick installation of the scraper-spider.

**MILESTONE**
I found a way to generate my own search results giving the scraper the ability to search with less dependency on major search engines.. 

The strength of the system comes from the archives. Memory in humain forgets things and where it has to go but the computer remembers everything if it is stored properly and efficiently. 

Storing urls and url information for later use gives the system the ability to store related searches as it is searching for specific subjects. The archive url memory enables the system to generate after some time search results it needs. 

For now this is possible only after weeks of use for now and it is still in developpement.
**DYNAMIC DISTRIBUTED SEARCH ENGINE**
But if the software is developed as a standalone application we could use every installation to save url information that can be after retransmitted anonymously to all stand alone application on the network creating a dynamic and distributed search engine that learns from its own queries and its search results. 

After weeks of learning and using Google, Bing, Yahoo, Duck and Yandex. Gathering search results on specific topics but storing search results in the archives with encoded keyword information. After 6 week of testing and development I have over 100000 urls with information about their images and the content of their webpage. 

The system is slowly becoming a search engine. It was the goal of the image retrieval project.

**OPTIMAL CONFIG**

The scraper-spider does an excellent job when it downloads everything flag is active

DOWNLOAD_EVERYTHING = ON

Also watch these parameters. 
Images under 1500 kb are not very interesting and lack resolution.

MAX_WORKSPACE_SIZE = 900000
MIN_IMAGE_SIZE = 5000
MIN_QUALITY_IMAGE_SIZE = 30000

The best strategy is to download everything and then let the intelligence make the best selection it can. 

The images that are not selected by AI are stored in the workspace directory in the archives folder. The scraper-spider then makes a selection thanks to the AI tools that are still being developed. The user can then look in the workspace at images that were not selected by the user but that may be interesting. 

Again the strengths comes archiving.
**AI STRATEGIES**

It verifies many things like : tag info, path keywords, image keywords, page content and more...

The only thing missing is the VISION module.

It is every day more and more a smart image scraper-spider and basic search engine. But it is getting more complexe and bugs are being split in. 

Still need more testing and development.
**Search Engine**

It uses Google, Bing and Yahoo.

It's like using a search engine: you make a query and the scraper collects images that fit your query. 

Basically it verifies keyword signature in html content, image filename, image path and image alt information. 

It also has multiple verification and strategies for url spidering. 

I connected the scraper to nltk and the system is building a definition dictionary, keyword relations, and learning from web pages content and queries. 

The system also keeps history for learning purposes. 

Still working on some intelligence and learning abilities. 
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

**Note don't forget to change the PROGRAM_PATH**PROGRAM_PATH = file:///home/linux/Bureau/Programmation/image-miner-X/dev/image-hunter.html**

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
Image-Miner will have the ability to judge the quality of an image. It already does a very impressive job with no visual information. 

When the vision algorithm will be ready the software will do an amazing job.

**IMAGE-MINER IN ACTION**
Visit the web site to view some of the images Image-Miner found during the testing phase of the project. 

**Visite our Website**
https://image-miner.weebly.com/
