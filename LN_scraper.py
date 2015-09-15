import requests
from bs4 import BeautifulSoup
import os



#Gets chapter links
def get_chapter_links(index_url):
    r = requests.get(index_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all('a')
    url_list = []
    for url in links:
        if 'http://www.wuxiaworld.com/cdindex-html/book' in str(url):
            url_list.append((url.get('href')))
    return url_list

#Gets chapter content
def get_chapters(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
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
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find_all('h1',{'class':'entry-title'})
    chapter_title = ''

    for l in title:
       chapter_title += l.text
    return chapter_title

#Gets title of story
def get_story_title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    story = soup.find_all('h1',{'class':"entry-title"})

    story_title = ''
    for content in story:
       story_title += content.text
    return story_title



#url on which links can be found
links = 'http://www.wuxiaworld.com/cdindex-html/'


#Checks whether a directory already exists and creates a new one if necessary
#TODO Find way to create directory unrelated from position of script
story_title = get_story_title(links)
if not os.path.isdir('{}'.format(story_title)):
    os.mkdir('{}'.format(story_title))

#Copys chapters into text file
for x in get_chapter_links(links):
    #Checks whether chapter already exists
    #TODO Make checking process quicker
    chapter_title = get_title(str(x)).replace(',','') + '.txt'
    if not os.path.isfile('{}'.format(story_title) + '/' + chapter_title):
        story_title = get_story_title(links)
        chapter_text = get_chapters(str(x))
        file = open('{}/'.format(story_title) + chapter_title, 'w')
        file.write(chapter_text)
        file.close()
        print('{} saved.'.format(chapter_title.replace(',','')))




