import requests
from bs4 import BeautifulSoup
import os
import getpass

#Gets chapter links
def get_chapter_links(index_url):
    r = requests.get(index_url)
    soup = BeautifulSoup(r.content, 'lxml')
    links = soup.find_all('a')
    url_list = []
    for url in links:
        if 'http://www.wuxiaworld.com/cdindex-html/book' in str(url):
            url_list.append((url.get('href')))
    return url_list

#Gets chapter content
def get_chapters(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    chapter_text = soup.find_all('div',{'class':"entry-content"})
    #Puts chapter text into 'chapter'-variable
    chapter = ''
    for c in chapter_text:
      #Removing 'Previous Next Chapter'
      content = c.text.strip()                              # strip??
      chapter += content.strip('Previous Next Chapter')     # strip??
    return chapter

#Gets title of chapter
def get_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    title = soup.find_all('h1',{'class':'entry-title'})
    chapter_title = ''
    for l in title:
       chapter_title += l.text
    return chapter_title

#Gets title of story
def get_story_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    story = soup.find_all('h1',{'class':"entry-title"})
    story_title = ''
    for content in story:
       story_title += content.text
    return story_title



#url on which links can be found
links = 'http://www.wuxiaworld.com/cdindex-html/'


#Checks whether a directory already exists and creates a new one if necessary
story_title = get_story_title(links)
path = '/users/{}/documents/'.format(getpass.getuser())+'{}'.format(story_title)
if not os.path.isdir(path):
    os.mkdir(path)
link_list = get_chapter_links(links)


#Copiess chapters into text file
file2_out = open(path + '/url_list.txt', 'a') #local url list for chapter check
for x in link_list:
    #Checking chapter existance in folder and downloading chapter
    if x not in open(path + '/url_list.txt').read(): #Is url of chapter in local url list?
        chapter_title = get_title(str(x)).replace(',','') + '.txt'
        chapter_text = get_chapters(str(x))
        file = open(path + '/' + chapter_title, 'w')
        file.write(chapter_text)
        file.close()
        
        file2_out.write('{}\n'.format(x)) #adding downloaded chapter to local url list
        print('{} saved.'.format(chapter_title.replace(',','')))


file2_out.close()


print('All chapters are up to date.')




#TODO If  files gets deleted, script won't know because only way of checking is throught the local list
