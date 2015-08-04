# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from urllib import request
import lxml
import re
import numpy as np
import nltk as nlp
import os

class FetchArticles():

    """Fetches and normalizes an url or a list of urls"""
    __pattern = "\\n|<.*>|\\xa0|\\r"

    def __normalize_text(self, text):
        """Normlizes the the article

        :article: Article dict
        :returns: The normalized text

        """
        # Normalize text

        # Problem with stemming and special german chars
        text = re.sub("ß","ss",text)
        text = re.sub("ö","oe",text)
        text = re.sub("ä","ae",text)
        text = re.sub("ü","ue",text)
        # Finds and deletes all urls in the text
        text = re.sub("(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?","",text)

        return text


    # Different Wrappers
    # Krone Zeitung
    def __get_krone_article(self, url):
        html = request.urlopen(url).read()

        # Get html as object
        soup = bs(html, "lxml", from_encoding="ISO-8859-1")

        # Article title
        title = re.sub(self.__pattern,"",soup.title.get_text())

        # Article excerpt
        excerpt = re.sub(self.__pattern, "", soup.find("div","content_lead").get_text())

        # Article text
        content = re.sub(self.__pattern, "", soup.find("div","content_text").get_text())

        content = self.__normalize_text(content)
        
        return {"title":title, "excerpt":excerpt, "content":content}



    # Zeit Online 
    def __get_zeit_article(self, url, pages = 1):

        # Text parser
        def has_no_class(tag):
            return not tag.has_attr('class') and tag.name == "p"

        # Initialize variables
        content_sets = []
        title = ""
        excerpt = ""

        # Get objects
        for i in range(1,pages+1):
            if(i == 1):
                html = request.urlopen(url).read()
                soup = bs(html, "lxml", from_encoding="utf-8")

                # Article title
                title = soup.title.get_text()

                # Get excerpt
                excerpt = soup.find("p","excerpt").get_text()

                # Get content text objects
                content_sets.extend([tag.find_all(has_no_class) for tag in soup.find_all("div",{"class":"article-body"}) ])
            if(i>1):
                html = request.urlopen(url+"/seite-"+str(i)).read()
                soup = bs(html, "lxml", from_encoding="utf-8")

                content_sets.extend([tag.find_all(has_no_class) for tag in soup.find_all("div",{"class":"article-body"}) ])

        # Normalize
        title = re.sub(self.__pattern, " ",title)
        excerpt = re.sub(self.__pattern, " ",excerpt)

        temp = [" ".join([t.get_text() for t in rs]) for rs in content_sets]
        content = " ".join(temp)
        content = re.sub(self.__pattern," ",content)

        content = self.__normalize_text(content)

        return {"title":title, "excerpt":excerpt, "content":content}


  
    def download_all_articles(self):
        """Saves all articles as txt files under data/

        :urls: filename of a txt file containing article urls located in project root
        """

        # Create corpus directory
        corpusdir = 'data/'
        if not os.path.isdir(corpusdir):
            os.mkdir(corpusdir)       

        zeitdir = 'data/zeit/'
        if not os.path.isdir(zeitdir):
            os.mkdir(zeitdir)       

        kronedir = 'data/krone/'
        if not os.path.isdir(kronedir):
            os.mkdir(kronedir)       

        # Save articles
        # Zeit
        with open("zeit.txt", "r") as url_list:
            for line in url_list.readlines():
                article = self.__get_zeit_article(line)

                # Format title
                title = re.sub("...ZEIT ONLINE ","",article["title"].strip())
                title = re.sub("\\W","_",title)
                title = re.sub("_+","_",title)

                with open(zeitdir+title+".txt", "w") as text_file:
                    text_file.write(article["content"])

        # Krone
        with open("krone.txt", "r") as url_list:
            for line in url_list.readlines():
                article = self.__get_krone_article(line)

                # Format title
                title = re.sub("-.*-.*- krone.at","",article["title"].strip())
                title = re.sub("\\W","_",title)
                title = re.sub("_+","_",title)

                with open(kronedir+title+".txt", "w") as text_file:
                    text_file.write(article["content"])






