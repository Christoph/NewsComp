from bs4 import BeautifulSoup as bs
from urllib import request
import lxml
import re
import nltk as nlp
import web

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

web = web.FetchArticle()

zt = web.get_article(url_zeit, "zeit")
kt = web.get_article(url_krone, "krone")

ztokens = zt.tokens
ktokens = kt.tokens

zfd = nlp.FreqDist(ztokens)
kfd = nlp.FreqDist(ktokens)

zstat = basic_statistics(zt,zfd)
kstat = basic_statistics(kt,kfd)

zvocab = set(ztokens)
kvocab = set(ktokens)
common_vocab = zvocab.intersection(kvocab)

tokens = {"Zeit":ztokens, "Krone":ktokens}

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


