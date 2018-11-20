
# coding: utf-8


from selenium import webdriver
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import datetime
import csv

driver_path = '' #put the path of your browser driver here

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def txtClean(txt):
    txt = str(txt)
    txt = cleanhtml(txt)
    txt = txt.lower()
    #txt = re.sub(r'http\S+', '', txt) #remove url
    #txt = re.sub(r'pic\S+', '', txt)
    #txt = re.sub(r'@', '', txt)
    #txt = txt.replace('’',' ')
    txt = txt.replace('[',' ')
    txt = txt.replace(']',' ')
    #txt = txt.replace(r'\xa0',' ',txt)
    
    #txt = re.sub(r'^https?:\/\/.*[\r\n]*', '', txt, flags=re.MULTILINE)
    
    #txt = txt.replace('&amp','')
    #txt = txt.replace('ly…','')
    #txt = txt.replace('ht…','')
    
    '''
    p = string.punctuation
    d = string.digits
    table_p = str.maketrans(p, len(p)*' ')
    table_d = str.maketrans(d, len(d)*' ')
    txt = txt.translate(table_p)
    txt = txt.translate(table_d)
    '''
    
    #words = nltk.word_tokenize(txt)
    #words = [w for w in words if w not in stopwords]
    #tag = nltk.pos_tag(words)
    #for k,v in tag:
        #words = [lmtzr.lemmatize(k, getPos(v)) for k in words]    
    #cleaned = [w for w in words if w not in stopwords]
    #final = ' '.join(cleaned)
    final = txt
    
    return final

def timeClean(t):
    #t = re.search(r'(?<=title=\")(.*)(?=\")', t).group(0)
    t = re.search(r'title\=\"(.+?)\"', str(t)).group(0)
    t = re.sub(r'title=','',t)
    t = re.sub(r'\"', '', t)
    t = t.split(' - ')
    return t

def userClean(user):
    t=re.search(r'part\=\"\"\>(.+?)\<', str(user)).group(0)
    t=re.sub(r'part=""','',t)
    t = re.sub(r'\>', '', t)
    t = re.sub(r'\<', '', t)
    return t

def screenClean(name):
    t = re.search(r'\<b\>(.+?)\<\/b\>', str(name)).group(0)
    #t=re.sub(r'part=""','',t)
    t = re.sub(r'\<b\>', '', t)
    t = re.sub(r'\<\/b\>', '', t)
    t = '@'+t
    return t

#find the real screenname of this tweet
def trueName(name):
    for n in name:
        if 'data-aria-label-part' in str(n):
            return screenClean(n)
        else:
            return 'NameError'
        
#find the id of this tweet from the full raw tweet
def tweetidFind(fulltweet):
    t = re.search(r'data-item-id=\"(.+?)\"', str(fulltweet)).group(0)
    t = re.sub(r'data-item-id=\"','',t)
    t = re.sub(r'\"', '', t)
    return t


import csv

f = open('tweets_selenium.txt','w', encoding='utf-8')
c = csv.writer(f)
c.writerow(['id', 'time', 'date', 'username', 'screenname', 'text'])

try: #use try function to avoid error. This is not necessary
    #set browser and browser driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(executable_path='driver_path', chrome_options=options) #path of driver
    
    date = datetime.datetime(2015,1,1,0,0,0) #starting date
    while date <= datetime.datetime(2018,12,31,0,0,0): #stop date
        keyword1 = ''
        keyword2 = '' #add more keywords as you wish
        url = 'https://twitter.com/search?f=tweets&q='+keyword1+'%20'+keyword2+'%20since%3A'+\
        str(date)[:10]+'%20until%3A'+str(date+datetime.timedelta(days=1))[:10]+'&src=typd&lang=en'
        #add '%20' between every keyword
        date += datetime.timedelta(days=1) #set the days of increment
    
        #load the webpage
        driver.get(url)
        
        #start scroll function
        SCROLL_PAUSE_TIME = 4

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
    
        print('collecting tweets from '+str(date)[:10]+' to '+str(date+datetime.timedelta(days=1))[:10])
    
        with tqdm() as pbar:
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
            
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                pbar.update()
        #end scroll function
        
        html_source = driver.page_source #save html file of target page
        sourcedata = html_source.encode('utf-8') #save the page content into readable text
        soup = BeautifulSoup(sourcedata, 'html.parser') #make the page a beautifulcoup object
        
        #locate all tweets
        raw_tweet = soup.body.find_all('li', {'class':"js-stream-item stream-item stream-item "})
        
        for i in range(len(raw_tweet)):
            td = raw_tweet[i].find_all('a', {'class':'tweet-timestamp'})
            texts = raw_tweet[i].find_all('p',{'TweetTextSize'})
            usr_name = raw_tweet[i].find_all('span', {'class':'FullNameGroup'})
            screen_name = raw_tweet[i].find_all('span',{'class':'username u-dir u-textTruncate'})
            
            tweet_id = tweetidFind(raw_tweet[i])
            
            time_list = timeClean(str(td))
            usr = userClean(usr_name)
            sname = screenClean(screen_name)
            text = txtClean(texts)
            row = [tweet_id, time_list[0], time_list[1], usr,
                   sname, text]
            c.writerow(row)
                
except Exception as e:
    pass
finally:
    driver.close()
        
f.close()
print('done')

