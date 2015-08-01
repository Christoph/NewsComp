
from bs4 import BeautifulSoup as bs
from urllib import request
import lxml
import re
import numpy as np
import nltk as nlp

class FetchArticle():

    """Fetches and normalizes an url or a list of urls"""

    # Different Wrappers
    # Krone Zeitung
    def get_krone_article(self, url, pattern):
        html = request.urlopen(url).read()

        # Get html as object
        soup = bs(html, "lxml", from_encoding="ISO-8859-1")

        # Article title
        title = re.sub(pattern,"",soup.title.get_text())

        # Article excerpt
        excerpt = re.sub(pattern, "", soup.find("div","content_lead").get_text())

        # Article text
        content = re.sub(pattern, "", soup.find("div","content_text").get_text())
        
        return {"title":title, "excerpt":excerpt, "content":content}



    # Zeit Online 
    def get_zeit_article(self, url, pattern,  pages = 1):

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
        title = re.sub(pattern, " ",title)
        excerpt = re.sub(pattern, " ",excerpt)

        temp = [" ".join([t.get_text() for t in rs]) for rs in content_sets]
        content = " ".join(temp)
        content = re.sub(pattern," ",content)

        return {"title":title, "excerpt":excerpt, "content":content}


    def normalize_article(self, article):
        """Normlizes the the article

        :article: Article dict
        :returns: The normalized text and the frequency distribution object

        """
        # Normalize text
        # Convert normal text to nltk.Text
        tokens = nlp.word_tokenize(article["content"])
        text = nlp.Text(tokens)

        # Frequency distribution
        return text

    def get_article(self, url, news):
        """Returns normalized article text

        :url: Article url or list of article urls
        :news: Which newspaper as string
        :returns: raw text 

        """

        # Initialize variables
        # Remove newline and hyperlinks and join text objects and non breaking spaces
        pattern = "\\n|<.*>|\\xa0|\\r"

        # Get articles
        if news == "zeit":
            article = self.get_zeit_article(url, pattern)
        elif news == "krone":
            article = self.get_krone_article(url, pattern)

        return self.normalize_article(article)














