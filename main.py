from bs4 import BeautifulSoup as bs
from urllib import request
import lxml
import re
import numpy as np
import nltk as nlp

# Define get article functions

# Remove newline and hyperlinks and join text objects and non breaking spaces
pattern = "\\n|<.*>|\\xa0|\\r"

# Krone Zeitung
def get_krone_article(url):
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
def get_zeit_article(url, pages = 1):

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


def normalize_article(article):
    """Normlizes the the article

    :article: Article dict
    :returns: The normalized text and the frequency distribution object

    """
    # Normalize text
    # Convert normal text to nltk.Text
    tokens = nlp.word_tokenize(article["content"])
    text = nlp.Text(tokens)

    # Frequency distribution
    return text, nlp.FreqDist(text)


def basic_statistics(text, fd):
    """Computes basic metrics and statistics for a article frequency distribution

    :fd: Frequency distribution af an article
    :returns: Word/vocab size, lexical diversity and words which have more than 5 characters and occurre more than 2 times

    """
    # Simple statistics
    # Basic measures
    total_words = fd.N()
    vocab_size = fd.B()

    lexical_diversity = total_words/vocab_size

    # Words longer than 7 characters and occurring more than 5 times
    important_words = [w for w in fd.keys() if len(w) > 5 and fd[w] > 2]

    return {"words":total_words, "vocab":vocab_size, "lexical_diversity":lexical_diversity, "important":important_words}


# NLP

# Get article
url_zeit = "http://www.zeit.de/gesellschaft/zeitgeschehen/2015-07/malaysia-airlines-mh370-wrackteil-frankreich-toulous"
url_krone = "http://www.krone.at/Welt/Grosse_Zuversicht._dass_Wrackteil_von_MH370_stammt-Verschollene_Boeing-Story-465019"

zeit = get_zeit_article(url_zeit)
krone = get_krone_article(url_krone)

zt, zfd = normalize_article(zeit)
kt, kfd = normalize_article(krone)

zstat = basic_statistics(zt,zfd)
kstat = basic_statistics(kt,kfd)

zvocab = set(zt.tokens)
kvocab = set(kt.tokens)
common_vocab = zvocab.intersection(kvocab)

tokens = {"Zeit":zt.tokens, "Krone":kt.tokens}

cfd = nlp.ConditionalFreqDist(
        (news, word)
        for news in ["Zeit","Krone"]
        for word in tokens[news]
        )






# Distribution of word length
# fd_wl = nlp.FreqDist([len(w) for w in zfd])

# Plotting

# Plot a CDF
# fd.plot(20, cumulative=True)

# fd_wl.plot()

# Plot CDF
# cdf.plot(samples=common_vocab)


