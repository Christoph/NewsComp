# Web stuff
from bs4 import BeautifulSoup as bs
from urllib import request
import lxml

# NLP stuff
from nltk.corpus import stopwords
import re
import nltk as nlp

# My own classes
import web

# For the concordance output
import io
from contextlib import redirect_stdout


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

url_zeit = "http://www.zeit.de/gesellschaft/zeitgeschehen/2015-07/malaysia-airlines-mh370-wrackteil-frankreich-toulous"
url_krone = "http://www.krone.at/Welt/Grosse_Zuversicht._dass_Wrackteil_von_MH370_stammt-Verschollene_Boeing-Story-465019"

# Initialize variables and classes
# My classes
web = web.FetchArticle()

# Get all german stopwords and , and . 
g_stop = stopwords.words("german")
g_stop.append(",")
g_stop.append(".")

# German stemmer
snow = nlp.stem.snowball.GermanStemmer(ignore_stopwords=True)

# Get the article text
zeit_text = web.get_article(url_zeit, "zeit")
krone_text = web.get_article(url_krone, "krone")

# Remove stopwords and tokenize
zt = [w.lower() for w in zeit_text.tokens if w not in g_stop]
kt = [w.lower() for w in krone_text.tokens if w not in g_stop]

# Tokenize words
zt = [snow.stem(w) for w in zt]
kt = [snow.stem(w) for w in kt]

zfd = nlp.FreqDist(zt)
kfd = nlp.FreqDist(kt)

# Basic statistics
zstat = basic_statistics(zt,zfd)
kstat = basic_statistics(kt,kfd)

# Vocabulary
zvocab = set(zt)
kvocab = set(kt)
common_vocab = zvocab.intersection(kvocab)

tokens = {"Zeit":zt, "Krone":kt}

cfd = nlp.ConditionalFreqDist(
        (news, word)
        for news in ["Zeit","Krone"]
        for word in tokens[news]
        )

# Word length comparrison
zwl = nlp.FreqDist([len(w) for w in zt])
kwl = nlp.FreqDist([len(w) for w in kt])

wordlength = {"Zeit": zwl, "Krone": kwl}

cwl = nlp.ConditionalFreqDist(
        (news, length)
        for news in ["Zeit","Krone"]
        for length in wordlength[news]
        )

# Generates list for concordance function
def word_concordance(word, text):
    """Prints concordance for the word

    :word: word/wordstem 
    :text: nltk text
    :returns: concordance string

    """

    # Initialize variable
    concordance = io.StringIO()

    # Get all string with word as substring 
    words = set([w for w in zeit_text.tokens if re.findall("\\b\\w*"+word+"\\w*\\b",w)])

    # Get all concordances
    with redirect_stdout(concordance):
        for w in words:
            text.concordance(w)

    # Save and close the IO object
    result = concordance.getvalue()
    concordance.close()

    # Remove headers from nltk concordance output
    result = re.sub("Displaying.*matches:","",result)
    result = re.sub("\\n\\n","\\n",result)

    return result

# Plotting

# Plot a CDF
# fd.plot(20, cumulative=True)

# fd_wl.plot()

# Plot CDF
# cdf.plot(samples=common_vocab)


