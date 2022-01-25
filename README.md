**Image-Miner**

Image-Miner is an AI project. It is a smart image scraper. It's fast and robust and has basic intelligence. It uses Google, Bing and Yahoo for search results and to start image scraping operations based on keywords. You can ask for the type of image you want in a textual format. The scraper will then look for that information. It's like using a search engine: you make a query and the scrapper collects images that fit that query. Basically it verifies keyword signature in html content, image filename, image path and image alt information. It also has multiple verification and strategies for url spidering and image downloading. 

I am also working on some intelligence and learning abilities. I connected to an nlp lib called nltk and the system is building a definition dictionary, keyword relations, and learning from web pages content and queries. 

The system also keeps history for learning purposes. I also want to develop a profile that will contain user specific information to guide the searching process. So we can suggest search results depending on the user tasts, education and background.
**Miner features and functionality**
- Works with Google, Yahoo and Bing 
- It works with almost supervision
- It learns from web site 
- It learns from user input 
- It keeps a history
- It check link for keywords 
- It check images alt tag
- It check images filename
- It check keywords in the web page path 
- It learns from links, web pages and user queries
- It has a simple scoring system QS (Quality Score)
- It extracts and reads html content
- it matches stems of keywords 
- It as an simple html interface 
- It can be used as a search engine
- It as a database to keep track of information
- It build a depot of all images 

**Signature matching keywords**It matches keywords with signatures that are simple sections of the keyword. The signature matching works really well. I have it set on 3 for the minimum stem (section of word). The signature matching enables the system to read web content to make a decision to download or not the urls and images on the html page. It uses a simple Quality Score to tweak the intelligence of the scraper. Top performence depends on many factors but with a quality score of 20 the results are very impressive.

There is also one config.env file that lets you play with the parameters of the scrapper.

**Supported Image formats**
psd,apng,avif,bmp,gif,ico,cur,tif,tiff,jpg,jpeg,jfif,pjpeg,pjp,png,svg,webp,webm,ogg,wav,tiff,ico,jpg,gif,png,bmp

Database Integration is completed with sqlite.

During testing in the past 3 weeks it gathers : 65000 images and icons. 

More intelligence is on the way...

Currently working on a Web interface and web service.

**MY WISHLIST for 2022**
- Vision developpement 
- Enhance AI
  - Better searching abilities
  - Better roaming abilities

**NEXT PHASE**
Image-Miner will have the ability to judge the quality of an image.

**IMAGE-MINER IN ACTION**
Visit the web site to view some of the images Image-Miner found during the testing phase of the project. 

**Visite our Website**
https://image-miner.weebly.com/
