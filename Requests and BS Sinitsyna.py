
# coding: utf-8

# In[1]:


import requests 
from bs4 import BeautifulSoup
import re
import time


# In[50]:


class SomeArticles:
    
    def __init__(self):
        self.articles=[]

    def getnytarticle(self, url):

        findheaders = re.compile('<h1 itemprop="name">(.+)</h1>', re.S)
        whole_article = re.compile('<div itemprop="description">(.+)<div class="post-tags">', re.S)
        delscript = re.compile("<script.*?>.+?</script>", re.S)
        art=requests.get(url)
        title = findheaders.findall(art.text)[0]
        article = whole_article.findall(art.text)[0]
        article = "".join(delscript.split(article))

        replacement = {'&raquo;' : '"', '&laquo;' : '"', '\xa0' : ' ', '\n' : '', '\t' : '', '&nbsp;' : '', '&mdash;' : ' -'}
        def replace_all(text, dic):
            for i, j in dic.items():
                text = text.replace(i, j)
            return text

        article = replace_all(article, replacement)
        title = replace_all(title, replacement)

        self.articles.append(re.sub("<.*?>", " ", title+"\n-----\n"+article+'\nКонец статьи\n\n'))

    def getlotsofarticles(self, url, n):
        res = ''
        try:
            for page in range(1, n+1):
                links = BeautifulSoup(requests.get("https://theins.ru/category/news/page/{}".format(page)).text, "html5lib").find_all('h3')
                links = [l.find_all("a")[0]["href"] for l in links]
                print(links)
                for l in links:
                    self.getnytarticle(l)
                    time.sleep(0.3)
                for art in self.articles:
                    res+=art
        except:
            pass    
        return res

    def writetotxt(self, url, n, filename):
        txt = open(filename, 'w', encoding = 'utf-8')
        txt.write(self.getlotsofarticles(url, n))
        return 'Now all of the articles are in {}'.format(filename)

    def readtxt(self, filename):
        arts = open(filename, 'r', encoding = 'utf-8').read()


# In[51]:


myarticles = SomeArticles()
myarticles.writetotxt("https://theins.ru/category/news/page/", 1, 'try_for_real.txt')


# In[52]:


myarticles.readtxt('try_for_real.txt')

