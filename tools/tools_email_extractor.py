# -*- coding: UTF-8 -*-
#!/usr/bin/env pythonimport os
import os  # to save it locally
import re
import sqlite3
import sys
import time
import urllib.request
from re import I
from socket import timeout
from sqlite3 import Error
from urllib.error import HTTPError, URLError
from urllib.request import HTTPError, URLError
import requests  # to get image from the web
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import search_engine as se

MIN_WORD_SIZE = 1
MAX_WORD_SIZE = 19
MIN_URL_SIZE = 10
MAX_URL_SIZE = 180
MIN_PATTERN_SIZE = 1
LONG_KEYWORD_SIZE = 25

imageExt = ["jpeg", "exif", "tiff", "gif", "bmp", "png", "ppm", "pgm", "pbm", "pnm", "webp", "hdr", "heif", "bat", "bpg", "cgm", "svg"]
ua = UserAgent()

proxy_good = False
proxies_list = []
proxies = {
   'http': '68.188.59.198:80',
   'https': '34.138.225.120:8888',
}
count_email_in_phrase = 0

TIME_LOCK = 1
# Menú Principal

def open_url_proxy(url, i_proxy):
    global proxies_list # https://openproxy.space/list
    global proxies

    proxies = {
        'http': proxies_list[i_proxy],
        'https': proxies_list[i_proxy],
    }

    try: 
        page = requests.get(str(url), headers={'User-Agent': ua.random}, proxies=proxies, timeout=10)
        proxies = proxies
        return page
    except:
        pass

    return None

# Extraer lista de palabras claves de txt
def extractKeywordsList(txtFile):
	f = open(txtFile, 'r')
	text = f.read()
	keywordList = text.split(sep='\n')
	for key in keywordList:
    		print(key)

# Limpia la pantalla según el sistema operativo
def clear():
	try:
		if os.name == "posix":
			os.system("clear")
		elif os.name == "ce" or os.name == "nt" or os.name == "dos":
			os.system("cls")
	except Exception as e:
		print(e)
		input("Press enter to continue")
		menu()
   
def searchSpecificLink(link, listEmails, frase):
	try:

		global count_email_in_phrase

		print ("Searching in " + link)
		if(link[0:4] == 'http'):
			f = urllib.request.urlopen(link, proxies=proxies, timeout=10)
			s = f.read().decode('utf-8')
			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
			for email in emails:
				if (email not in listEmails):
					count_email_in_phrase += 1
					listEmails.append(email)
					print(str(count_email_in_phrase) + " - " + email)										
						
	except Exception as e:
		print(e)
		pass

def menu():

	file = open("/home/linux/Bureau/Programmation/image-miner-X/tools/quieries", "r")
	lines = file.readlines()

	lines.sort()
	import random
	random.shuffle(lines)
	relax(TIME_LOCK)

	get_web_page("www.google.com")

	for i in lines:
		print("Changing line...")
		print(str(i.strip()))
		print("Cleaning query")
		relax(TIME_LOCK)
		
		i = clean_text(i.strip())
		relax(TIME_LOCK)
		
		if i == None:
			continue

		print("New clean query: " + i)
		i = i.replace(" ", "+")
		relax(TIME_LOCK)
		
		extractFraseGoogle(i)
		relax(TIME_LOCK)
		
def trim(text_section):
    if text_section == None:
        return None
    if text_section == "" or " ":
        return None   
    text_section = clean_word(text_section)

    text_section = text_section.lstrip()
    text_section = text_section.rstrip()
    text_section = text_section.strip()
    return text_section

def clean_url(url):
    url = url.replace("\n", "")
    return url.strip()

def load_list(file_name, urls_list):

    # read url file
    with open(file_name, "r") as file:
        # reading each line"
        for line in file:
            url = clean_url(line)
            if (len(url)>MIN_WORD_SIZE):
                urls_list.append(str(url))
    
    clean_list = []
    for i in urls_list:
        if i == None:
            continue
        if (len(i) <= MIN_URL_SIZE):
            continue
        if (len(i) >= MAX_URL_SIZE):
            continue

        if not i in clean_list:
            clean_list.append(i)

    urls_list = []

    for i in clean_list:
        if i not in urls_list:
            urls_list.append(i)

    return urls_list
	
def find_a_working_proxy(url, proxies_list):
    
    index = 0
    error = 0
    
    proxy = ""
   
    MAX_NB_RETRIES = 10

    for i in proxies_list:
        page = open_url_proxy(url, index)
        index = index + 1
        error = error + 1

        if error > MAX_NB_RETRIES:
            return None

        print("Searching for a working proxy...")
        print(str(proxies_list[index]))
        relax(TIME_LOCK)

        if page == None:
            proxies_list.remove(i)
            continue
        else:
            proxy = i
            break

    proxies_list = save_list(proxies_list, "/home/linux/Bureau/Programmation/image-miner-X/tools/proxies")
    print("Found proxy : " + str(proxy))
    proxy_good = True
    return proxy
   


def save_list(urls_list_x, file_name_x):
    # write url in visited site file
    if urls_list_x == None:
        return False

    try:
        str_formated_urls="\n"
        str_formated_urls = str_formated_urls.join(urls_list_x)
        # print(str_formated_urls)
    except:
        pass
        
    with open(file_name_x, "w", encoding="utf-8") as file:
        file.writelines(str_formated_urls)
        file.close()
    return urls_list_x

def open_url(url):
    global proxies_list # https://openproxy.space/list
    global proxies

    try: 
        page = requests.get(str(url), headers={'User-Agent': ua.random}, proxies=proxies, timeout=10)
        proxies = proxies
        return page
    except:
        pass

    return None

def get_web_page(url):    
    
	global i_proxy
	global proxies_list
	global proxy_good
    
	proxies_list = load_list("/home/linux/Bureau/Programmation/image-miner-X/tools/proxies", proxies_list)
	
	if not proxy_good:
		page = find_a_working_proxy(url, proxies_list)
		if (page==None):
			return None
		try:
			page = open_url(url)

			if page.status_code == 200:
				proxy_good = True
			else:
				pass
		except:
			pass
	relax(TIME_LOCK)
	return page

        
def relax(sec):
    time.sleep(sec)

def clean_word(word):
    if word == None:
        return None
    # Normalize the string
    word  = word.lower()
    for char in word:
        # String character cleansing
        if char in "…[]#&\':–(){};|*#/+\"\\~–":
            word = word.replace(char, " ")
    return word

def clean_text(text):

	if text==None:
		return None
		
	items = ["\xa0","|","(",")","[", \
		"]","{","}","  ","…","[","]","?", \
			"","»","#",":","–","©",",",".","\t", \
				"#","*","/","\\","~","–"]
	text = text.lower()
	
	for filter in items:
		text = text.replace(filter, " ")
		
	text = text.replace("\n", " ")
	text = text.replace("\t", " ")
	text = text.replace("\r", " ")
	while "  " in text:
		text = text.replace("  ", " ")
		
	for i in text.split():
		if len(i) > MAX_WORD_SIZE:
			text = text.replace(i," ")
			continue
		if len(i) < MIN_PATTERN_SIZE:
			text = text.replace(i," ")
			continue
		if len(i) > LONG_KEYWORD_SIZE:
			text = text.replace(i," ")
			continue
		
	return text

def run_original_options(opcion):	
	#opcion = input("Enter option - Ingrese Opcion: ")
	try:
		if (opcion == "1"):
			print("")
			print ("Example URL: http://www.pythondiario.com")
			url = str(input("Enter URL - Ingrese URL: "))
			extractOnlyUrl(url)
			input("Press enter key to continue")
			menu()

		if (opcion == "2"):
			print("")
			print ("Example URL: http://www.pythondiario.com")
			url = str(input("Enter URL - Ingrese URL: "))
			extractUrl(url)
			input("Press enter key to continue")
			menu()

		elif (opcion == "3"):
			print("")
			#frase = str(input("Enter a phrase to search - Ingrese una frase a buscar: "))
			print ("***Warning: The amount of results chosen impacts the execution time***")
			print ("*** Advertencia: La cantidad de resultados elejidos impacta el tiempo de ejecucion")
			#cantRes = int(input("Number of results in Google - Cantiad de resultados en Google: ")) 
			print ("")
			#extractFraseGoogle(i, 9)		
			#input("Press enter key to continue")
			menu()

		elif (opcion == "4"):
			#extractKeywordsList("KeywordsList.txt")
			print("Developing...")
			input("Press enter key to continue")
			menu()
		
		elif (opcion == "5"):
			print ("")
			print ("1 - Select a phrase - Seleccionar una frase")
			print ("2 - Insert a URL")
			print ("3 - All emails - Todos los correos")
			opcListar = input("Enter option - Ingrese Opcion: ")
			
			if (opcListar == "1"):
				listarPorFrase("Emails.db")

			elif (opcListar == "2"):
				listarPorUrl("Emails.db")

			elif (opcListar == "3"):
				listarTodo("Emails.db")

			else:
				print("Incorrect option, return to the menu...")
				time.sleep(2)
				menu()

		elif (opcion == "6"):
			print("")
			print("1 - Save emails from a phrase - Guardar correos de una frase")
			print("2 - Save emails from a URL - Guardar correos de una URL")
			print("3 - Save all emails - Guardar todos los correos")
			opcGuardar = input("Enter Option - Ingrese Opcion: ")
			
			if(opcGuardar == "1"):
				frase = str(input("Enter phrase: "))
				guardarFrase("Emails.db", frase)
				
			elif(opcGuardar == "2"):
				print("Example URL: http://www.pythondiario.com")
				url = str(input("Insert URL: "))
				guardarUrl("Emails.db", url)
				
			elif(opcGuardar == "3"):
				guardarAll("Emails.db")
				
			else:
				print("Incorrect option, return to the menu...")
				time.sleep(2)
				menu()

		elif (opcion == "7"):
			print("")
			print("1 - Delete emails from a especific URL")
			print("2 - Delete emails from a especific phrase")
			print("3 - Delete all Emails")
			op = input("Enter option: ")

			if(op == "1"):
				print("Example URL: http://www.pythondiario.com")
				url = str(input("Insert URL: "))
				deleteUrl("Emails.db", url.strip())
			
			elif(op == "2"):
				phrase = str(input("Insert Phrase: "))
				deletePhrase("Emails.db", phrase.strip())

			elif(op == "3"):
				deleteAll("Emails.db")

			else:
				print("Incorrect option, return to the menu...")
				time.sleep(2)
				menu()
		
		elif (opcion == "8"):
			sys.exit(0)

		else:			
			print("")
			print ("Select a correct option - Seleccione un opcion correcta")
			time.sleep(3)
			clear()
			menu()
	except Exception as e:
		menu()

# Insertar correo, frase y Url en base de datos
def insertEmail(db_file, email, frase, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		c.execute("INSERT INTO emails (phrase, email, url) VALUES (?,?,?)", (frase, email, url))
		conn.commit()
		conn.close()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

# Buscar correo en la base de datos
def searchEmail(db_file, email, frase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails where email LIKE "%' + str(email) + '%" AND phrase LIKE "%' + str(frase) + '%"'
		result = c.execute(sql).fetchone()
		conn.close()

		return (result[0])

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

# Crea tabla principal		
def crearTabla(db_file, delete = False):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		if(delete == True):
			c.execute('drop table if exists emails')			

		sql = '''create table if not exists emails 
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				 phrase varchar(500) NOT NULL,
				 email varchar(200) NOT NULL,
				 url varchar(500) NOT NULL)'''

		c.execute(sql)
		conn.close()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

# Guardar por URL en un archivo .txt
def guardarUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = "' + url.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE url = "' + url.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Press enter to continue")
		menu()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Guardar por frase en un archivo .txt
def guardarFrase(db_file, frase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = "' + frase.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE phrase = "' + frase.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Press enter to continue")
		menu()
			
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Guardar todos los correos en un archivo .txt
def guardarAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile + ".txt", "w")
		
			c.execute('SELECT * FROM emails')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		
		input("Press enter to continue")
		menu()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos de una URL específica
def deleteUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = ' + '"' + url + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE url = " + '"' + url + '"')
				conn.commit()

				print("Emails deleted")
				input("Press enter to continue")
				menu()
				
			elif(option == "N" or option == "n"):
				print("Canceled operation, return to the menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Select a correct option")
				time.sleep(2)
				deleteUrl(db_file, url)
				
		conn.close()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos de una Frase específica
def deletePhrase(db_file, phrase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = ' + '"' + phrase + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE phrase = " + '"' + phrase + '"')
				conn.commit()

				print("Emails deleted")
				input("Press enter to continue")
				menu()
				
			elif(option == "N" or option == "n"):
				print("Canceled operation, return to the menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Select a correct option")
				time.sleep(2)
				deleteUrl(db_file, phrase)
				
		conn.close()
				
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos
def deleteAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
		
		
		else:			
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails")
				conn.commit()
				crearTabla("Emails.db", True)
				print("All emails were deleted")
				input("Press enter to continue")
				menu()

			elif(option == "N" or option == "n"):
				print("Canceled operation, return to the menu ...")
				time.sleep(2)
				menu()

			else:
				print("Select a correct option")
				time.sleep(2)
				deleteAll(db_file)
				
		conn.close()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

# Lista correos por frase
def listarPorFrase(db_file):
	try:
		phrase = str(input("Inserter phrase: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("No results for the specified url")
				input("Press enter to continue")
				menu()
				
		else:
			c.execute('SELECT * FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Press enter key to continue")
		menu()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
	
	finally:
		conn.close()

# Lista correos por URL
def listarPorUrl(db_file):
	try:
		print("Example URL: http://www.pythondiario.com ")
		url = str(input("Insert a Url: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails WHERE url LIKE "%' + url.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("No results for the specified url")
				input("Press enter to continue")
				menu()

		else:
			c.execute('SELECT * FROM emails WHERE url LIKE "%' + url.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Press enter key to continue")
		menu()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Lista todos los correos
def listarTodo(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("The data base is Empty")
			input("Press enter to continue")
			menu()

		c.execute("SELECT * FROM emails")

		for i in c:

			print ("")
			print ("Number: " + str(i[0]))
			print ("Phrase: " + str(i[1]))
			print ("Email: " + str(i[2]))
			print ("Url: " + str(i[3]))
			print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Press enter key to continue")
		menu()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

# Extrae los correos de una única URL
def extractOnlyUrl(url):
	try:
		print ("Searching emails... please wait")

		count = 0
		listUrl = []

		req = urllib.request.Request(
    			url, 
    			data=None,
				proxies=proxies, 
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
    	
			raise ValueError('Bad Url...')


		html = conn.read().decode('utf-8')

		emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)

		for email in emails:
			if (email not in listUrl and email[-3:] not in imageExt):
				count += 1
				print(str(count) + " - " + email)
				listUrl.append(email)
				if(searchEmail("Emails.db", email, "Especific Search") == 0):
					insertEmail("Emails.db", email, "Especific Search", url)

		print("")
		print("***********************")
		print(str(count) + " emails were found")
		print("***********************")

	except KeyboardInterrupt:
		input("Press return to continue")
		menu()

	except Exception as e:
		print (e)
		input("Press enter to continue")
		menu()

# Extrae los correos de una Url - 2 niveles
def extractUrl(url):
	print ("Searching emails... please wait")
	print ("This operation may take several minutes")
	try:
		count = 0
		listUrl = []
		req = urllib.request.Request(
    			url, 
    			data=None, 
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
    		
			raise ValueError('Bad Url...')

		html = conn.read().decode('utf-8')
		
		emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)
		print ("Searching in " + url)
		
		for email in emails:
			if (email not in listUrl and email[-3:] not in imageExt):
					count += 1
					print(str(count) + " - " + email)
					listUrl.append(email)

		soup = BeautifulSoup(html, "lxml")
		links = soup.find_all('a')

		print("They will be analyzed " + str(len(links) + 1) + " Urls..." )
		time.sleep(2)

		for tag in links:
			link = tag.get('href', None)
			if link is not None:
				try:
					print ("Searching in " + link)
					if(link[0:4] == 'http'):
						req = urllib.request.Request(
							link, 
							data=None, 
							headers={
							'User-Agent': ua.random
							})

						try:
							f = urllib.request.urlopen(req, timeout=10)

						except timeout:
							print("Bad Url..")
							time.sleep(2)
							pass

						except (HTTPError, URLError):
							print("Bad Url..")
							time.sleep(2)
							pass

						status = f.getcode()
						contentType = f.info().get_content_type()

						if(status != 200 or contentType == "audio/mpeg"):
							print("Bad Url..")
							time.sleep(2)
							pass
						
						s = f.read().decode('utf-8')

						emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)

						for email in emails:
							if (email not in listUrl and email[-3:] not in imageExt):
								count += 1
								print(str(count) + " - " + email)
								listUrl.append(email)
								if(searchEmail("Emails.db", email, "Especific Search") == 0):
									insertEmail("Emails.db", email, "Especific Search", url)

				# Sigue si existe algun error
				except Exception:
					pass
		
		print("")
		print("***********************")
		print("Finish: " + str(count) + " emails were found")
		print("***********************")
		#input("Press return to continue")
		menu()

	except Exception as e:
		print(e)
		input("Press enter to continue")
		menu()

i_proxy = 0
# Extrae los correos de todas las Url encontradas en las busquedas
# De cada Url extrae los correo - 2 niveles
def extractFraseGoogle(query):
	print ("Searching emails... please wait")
	print ("This operation may take several minutes")
	print ("With query: " + query)
	
	listEmails = []

	try:
		print("query: " + str(query))
		list = se.search_google(query)
		for i in list:	
			print(str(i))
			try:
				req = urllib.request.Request(
							i, 
							data=None, 
							proxies=proxies,
							headers={
							'User-Agent': ua.random
							})
				try:
					conn = urllib.request.urlopen(req)
				except timeout:
					print("Bad Url..")
					continue
				try:
			
					status = conn.getcode()
					contentType = conn.info().get_content_type()

					if(status != 200 or contentType == "audio/mpeg"):
						print("Bad Url..")
						continue

					html = conn.read()

				except timeout:
					print("Bad Url..")
					continue

				try:
					soup = BeautifulSoup(html, "lxml")
					links = soup.find_all('a')

					print("They will be analyzed " + str(len(links) + 1) + " Urls..." )
					time.sleep(2)

					for tag in links:
						link = tag.get('href', None)
						if link is not None:
							# Fix TimeOut
							searchSpecificLink(link, listEmails, query)
			
				except Exception as e:
					print(e)
					pass
			except Exception as e:
				print(e)
				pass
	except Exception as e:
		print(e)
		pass

# Inicio de Programa
def Main():
	menu()

Main()
