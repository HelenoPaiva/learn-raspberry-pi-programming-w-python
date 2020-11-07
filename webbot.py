from bs4 import BeautifulSoup
import mechanize
import time
import os
import urllib.request


start = "http://" + input("Initial website: \n")
file_type = input("file extension: \n")

num_slash = start.count('/') #slash counting after third
slash_list = [i for i, ind in enumerate(start) if ind == '/'] #list of slashes

if (len(slash_list) >= 3): #if there are more than 3 slashes, there will be the cut.
    third = slash_list[2]
    base = start[:third] #base is everything untill third slash
else:
    base = start

br = mechanize.Browser()
r = br.open(start)
html = r.read()
soup = BeautifulSoup(html, 'xml')
#print(soup.prettify()) #nice web structure


link_list = []

def download_files(html, base, file_type, link_list):
    soup = BeautifulSoup(html, 'xml')
    for link in soup.find_all('a'): #finding all links (most common soup command
        link_text = str(link) 
        file_name = str(link.get('href'))
        if file_type in link_text: #creating directories
            slash_list = [i for i, ind in enumerate(link_text) if ind == '/']
            directory_name = link_text[(slash_list[0]+1):slash_list[1]]
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)
                
        #if file_type in file_name: #this was an intermediate command. it is no longer needed.
            #image = urllib.request.urlopen(start)    #that is no longer necessary after importing urllib.request
            link_get = base + file_name
            file_save = str.lstrip(file_name, '/')
            urllib.request.urlretrieve(link_get, file_save)
        elif "htm" in file_name:
            link_list.append(link) 
        #this function download files, if the link is not the desired file, it'll go to this link list, and next these links will be evaluated for files.
            
            
print("Parsing " + start)    #let's just have some status messages on terminal      
download_files(html, base, file_type, link_list)

for left_over in link_list:
    time.sleep(0.1) #this is here to avoid server overload. polite bot.
    link_text = str(left_over.get('href'))
    print ("Parsing " + base + link_text)
    br = mechanize.Browser()
    r = br.open(base + link_text)
    html = r.read()
    link_list = []
    download_files(html, base, file_type, link_list)
