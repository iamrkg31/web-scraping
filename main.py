# Importing External Modules
import os
import re
import shutil
from bs4 import BeautifulSoup
basefolder = "/home/rahul/iitg.vlab.co.in/"

header = [] # used for storing file names at first level like index.html,index.html@pg=topMenu&id=5.html
subdirectory1 = [] #used for storing file names at second level like index.html@sub=58.html
subdirectory2 = [] #used for storing file names at third level like index.html@sub=58&brch=160.html
subdirectory3 = [] #used for storing file names at 4th level like index.html@sub=58&brch=160&sim=1366&cnt=2963.html
new_subdirectory1 = [] #for changing links of subdirectory1 in header files
new_subdirectory2 = []	#for changing links of subdirectory2 in subdirectory1 files
new_subdirectory2part2 = [] #for moving files in subdirectory2 to respective folder
new_subdirectory3part1 = [] #for changing links of subdirectory3 in subdirectory2 files
new_subdirectory3part2 = [] #for changing links of subdirectory3 in subdirectory1 files
new_subdirectory3part3 = [] #for moving files in subdirectory3 to respective folder

#get values of arrays defined above
for files in os.listdir(basefolder):
        if files.startswith("index.html@pg") or files.endswith("@.html") or files.endswith("index.html"):
		header.append(files)	

	if re.search(r".*sub=...html", files):
		subdirectory1.append(files)
		html_doc = open(basefolder+files, "r")		
		soup = BeautifulSoup(html_doc, 'html.parser')
		html_doc.close()
		if soup.title is not None:
			data = soup.title.string.split(":")#titles are of the form str1:str2			
			data[0]=data[0].strip() #to remove spaces from begining and end of the string 
			new_subdirectory1.append(data[0])		

	if re.search(r".*brch=....html", files):
		subdirectory2.append(files)
		html_doc = open(basefolder+files, "r")		
		soup = BeautifulSoup(html_doc, 'html.parser')
                html_doc.close()
		if soup.title is not None:
			data = soup.title.string.split(":")#titles are of the form str1:str2:str3			
			data[0]=data[0].strip() #to remove spaces from begining and end of the string 
			data[1]=data[1].strip() #to remove spaces from begining and end of the string 
			new_subdirectory2.append(data[0])
			new_subdirectory2part2.append(data[1]+"/"+data[0])		

	if (re.search(r".*cnt=.....html", files)) or (re.search(r".*cnt=....html", files)) or (re.search(r".*cnt=...html", files)) or (re.search(r".*cnt=..html", files)):
		subdirectory3.append(files)
		html_doc = open(basefolder+files, "r")		
		soup = BeautifulSoup(html_doc, 'html.parser')
		html_doc.close()
		
		if soup.title is not None:
			#titles are of the form str1:str2:str3:str4 and str1 may contain ':' so lenth5
			data = soup.title.string.split(":")		
			if len(data)==4:
                                data[0]=re.sub('\(.*?\)','', data[0])
				data[0]=data[0].strip() #to remove spaces from begining and end of the string 
                                data[1]=data[1].strip() #to remove spaces from begining and end of the string
				data[2]=data[2].strip() #to remove spaces from begining and end of the string  			           
				new_subdirectory3part1.append(data[0])	
                                new_subdirectory3part2.append(data[1]+"/"+data[0])
				new_subdirectory3part3.append(data[2]+"/"+data[1]+"/"+data[0])
				
			
			elif len(data)==5:
				data[0]=re.sub('\(.*?\)','', data[0])
				data[0]=data[0].strip() #to remove spaces from begining and end of the string 
                                data[1]=data[1].strip() #to remove spaces from begining and end of the string
				data[2]=data[2].strip() #to remove spaces from begining and end of the string
				data[3]=data[3].strip() #to remove spaces from begining and end of the string
				new_subdirectory3part1.append(data[0]+": "+data[1])	
                                new_subdirectory3part2.append(data[2]+"/"+data[0]+": "+data[1])
				new_subdirectory3part3.append(data[3]+"/"+data[2]+"/"+data[0]+": "+data[1])
#function to move files to respective folders
def move_files(input1,input2):
	for i, j in zip(input1, input2):
		if not os.path.exists(basefolder+j):
	    		os.makedirs(basefolder+j)
		shutil.move(basefolder+i,basefolder+j+"/"+i)

#function to modify links of the files which are being moved to their respective folders
def modify_link1(input1,input2,files):
	html_doc = open(basefolder+files, "r")		
	soup = BeautifulSoup(html_doc, 'html.parser')		
	html_doc.close()	

	for link in soup.find_all('a'):			
		for i, j in zip(input1, input2):
			if link.get('href')==i:						
				link['href'] = link['href'].replace(link.get('href'), j+"/"+link.get('href'))

	html = soup.prettify("utf-8")
	with open(basefolder+"output.html", "a") as file:
		file.write(html)
	os.remove(basefolder+files)
	os.rename(basefolder+"output.html",basefolder+files)

#return numbers of  ../ to be added in front of links
def link_editor(title_string):
	string = ""
	x1 = title_string.count(':')
	if x1==4:
		return "../../../"
	for i in range(0, x1, 1):
		string = "../"+string
	return string

#function to modify other links in the files (like external links, images, css, js etc)
def modify_link2(files):
	html_doc = open(basefolder+files, "r")		
	soup = BeautifulSoup(html_doc, 'html.parser')		
	html_doc.close()	

	#for the links to go back like:- you are here->home->chemichal engineering->virtual mass transfer lab
	if re.search(r".*brch=....html", files):
		for link in soup.find_all('a'):
			for i in subdirectory1:
				if link.get('href')==i:					
					link['href'] = link['href'].replace(link.get('href'), "../"+link.get('href'))

	if (re.search(r".*cnt=.....html", files)) or (re.search(r".*cnt=....html", files)) or (re.search(r".*cnt=...html", files)) or (re.search(r".*cnt=..html", files)):
		for link in soup.find_all('a'):
			for i in subdirectory1:
				if link.get('href')==i:					
					link['href'] = link['href'].replace(link.get('href'), "../../"+link.get('href'))
			for i in subdirectory2:
				if link.get('href')==i:					
					link['href'] = link['href'].replace(link.get('href'), "	../"+link.get('href'))

	#changing links
	for css in soup.find_all('link', attrs={'rel': re.compile("stylesheet")}):
            	css['href'] = css['href'].replace(css.get('href'), link_editor(soup.title.string) + css.get('href'))

	for javascript in soup.find_all('script', attrs={'src': True}):
    		javascript['src'] = javascript['src'].replace(javascript.get('src'), link_editor(soup.title.string)+ javascript.get('src'))

	for image in soup.find_all('img'):
    		image['src'] = image['src'].replace(image.get('src'),link_editor(soup.title.string)+ image.get('src'))

	for video in soup.find_all('iframe', attrs={'src': True}):
            video['src'] = video['src'].replace(video.get('src'), link_editor(soup.title.string) + video.get('src'))

	for ext_link in soup.find_all('a', attrs={'href': re.compile("external")}):
        	ext_link['href'] = ext_link['href'].replace(ext_link.get('href'), link_editor(soup.title.string) + ext_link.get('href'))

	for link in soup.find_all('a', attrs={'href': re.compile("index.php")}):
		link['href'] = link['href'].replace("index.php", "index")

	for link in soup.find_all('a'):			
		for i in header:
			if link.get('href')==i:					
				link['href'] = link['href'].replace(link.get('href'), link_editor(soup.title.string)+link.get('href'))	

	html = soup.prettify("utf-8")
	with open(basefolder+"output.html", "a") as file:
		file.write(html)
	os.remove(basefolder+files)
	os.rename(basefolder+"output.html",basefolder+files)

#modify links of the files which are being moved to their respective folders
for files in os.listdir(basefolder):
	if files.startswith("index.html@pg") or files.endswith("@.html") or files.endswith("index.html"):		
		modify_link1(subdirectory1, new_subdirectory1,files)				

	if re.search(r".*sub=...html", files):	
		modify_link1(subdirectory2, new_subdirectory2,files)	
		modify_link1(subdirectory3, new_subdirectory3part2,files)				
		
	if re.search(r".*brch=....html", files):		
		modify_link1(subdirectory3, new_subdirectory3part1,files)
	
#modify other links in the files (like external links, images, css, js etc)
for files in os.listdir(basefolder):
	if files.startswith("index.html"):
		modify_link2(files)
		
#move files to respective folders
move_files(subdirectory3, new_subdirectory3part3)
move_files(subdirectory2, new_subdirectory2part2)
move_files(subdirectory1, new_subdirectory1)


