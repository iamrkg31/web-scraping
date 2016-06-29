# Importing External Modules
from bs4 import BeautifulSoup
import re
import os
import sys

# Working folder 
basefolder = "/home/rahul/iitg.vlab.co.in/"

# Check if the External folder exists or not.
if not os.path.exists(basefolder + "external/"):
    print "external folder unavailable or unreachable :" + basefolder + "external/"
    sys.exit("Please create the external folder to Continue. Exiting...")

# Creating need_internet_connection.html in external folder.
print "Creating " + basefolder + "external/need_internet_connection.html"
os.chdir(basefolder + "external/")
f1 = open("need_internet_connection.html", "a")
text = "Internet connection required to view this page."
f1.write(text)
f1.close()

for files in os.listdir(basefolder):
	if files.startswith("index.html"):		
		html_doc = open(basefolder+files, "r")		
		soup = BeautifulSoup(html_doc, 'html.parser')		
		html_doc.close()

		# Changing external image links
		for image in soup.find_all('img', attrs={'src': re.compile("^http")}):
		    image['src'] = image['src'].replace("http://", "external/")

		    if not os.path.exists(basefolder + image['src']):		       
		        image['src'] = image['src'].replace(str(image.get('src')), "external/no_image.jpeg")

		# Changing external video links
		for video in soup.find_all('iframe', attrs={'src': True}):
		    video['src'] = video['src'].replace("http://", "external/")

		# Changing external js links
		for javascript in soup.find_all('script', attrs={'src': True}):
		    javascript['src'] = javascript['src'].replace("http://", "external/")		       

		# Changing external links
		for link in soup.find_all('a', attrs={'href': re.compile("^http")}):
		    link['href'] = link['href'].replace("http://", "external/")
		    if not os.path.exists(basefolder + link['href']):		       
		        link['href'] = link['href'].replace(str(link.get('href')), "external/need_internet_connection.html")

		# Creating output.html and saving the changes made to current file
		html = soup.prettify("utf-8")
		with open(basefolder+"output.html", "a") as file:
			file.write(html)
		os.remove(basefolder+files)
		os.rename(basefolder+"output.html",basefolder+files)


