**Image-Miner**

Image-Miner is an AI project. It is a smart image scraper. 

It uses Google, Bing and Yahoo.

It's like using a search engine: you make a query and the scraper collects images that fit your query. 

Basically it verifies keyword signature in html content, image filename, image path and image alt information. 

It also has multiple verification and strategies for url spidering. 

I am also working on some intelligence and learning abilities. I connected the scraper to nltk and the system is building a definition dictionary, keyword relations, and learning from web pages content and queries. 

The system also keeps history for learning purposes. 

I also want to develop a profil component that will contain user specific information to guide the searching process. 

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
Image-Miner will have the ability to judge the quality of an image. It all ready does a very impressif job with no visual information. 

When the vision algorithm will be ready the software will do an amazing job.

**IMAGE-MINER IN ACTION**
Visit the web site to view some of the images Image-Miner found during the testing phase of the project. 

**Visite our Website**
https://image-miner.weebly.com/
