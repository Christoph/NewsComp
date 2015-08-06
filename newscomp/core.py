# -*- coding: utf-8 -*-

# NLP stuff
from nltk.corpus import stopwords
import re
import nltk as nlp
from nltk.corpus import CategorizedPlaintextCorpusReader

# Data analysis
import numpy as np
import pandas as pd

# For the concordance output
import io
from contextlib import redirect_stdout


class NewsComparator():

    """Gives statistical information for a given article"""

    __metrics = ["TotalWordCount","TotalVocabCount","NormalizedWordCount","NormalizedVocabCount","LexicalDiversity"]

    def initialize(self, language, chars):
        """Initializes the news comparator class

        :language: Language of the articles
        :chars: Chars which will be removed before any statistical analysis

        """
        self.corp, self.words = self.__create_corpus(language,chars)
        self.metrics = self.__basic_statistics(chars)

    def __basic_statistics(self, chars):
        """Computes basic metrics and statistics for a given text

        """

        # Get all newspapers
        cat = self.corp.categories()

        # Creating dataframe and adding new columns
        metrics = pd.DataFrame(index=cat)

        # Compute basic statistics foreach paper separatly
        for news in cat:
            # Simple statistics
            fd = nlp.FreqDist(self.words[news])

            # Basic measures
            # On the normalized text
            metrics.loc[news,"NormalizedWordCount"] = fd.N()
            metrics.loc[news,"NormalizedVocabCount"] = fd.B()

            # On the original text
            words = self.corp.words(categories=news)
            words = [w.encode("utf-8").lower() for w in words if w not in chars]

            vocab = set(words)

            metrics.loc[news,"TotalWordCount"] = len(words)
            metrics.loc[news,"TotalVocabCount"] = len(vocab)
            metrics.loc[news,"LexicalDiversity"] = len(words)/len(vocab)

        return metrics

        # Word length
        #wl = nlp.FreqDist([len(w) for w in tw])

        # Access words of the second corpus
        # corpus.words(corpus.fileids()[1])

    def compare_word_freq(self):
        """Computes and plots the cond freq dist for all categories
        :returns: TODO

        """

        common_vocab = set.intersection(set(self.norm_vocab["zeit"]),set(self.norm_vocab["krone"]))

        cfd = nlp.ConditionalFreqDist(
                (news, word)
                for news in self.corp.categories()
                for word in self.words[news]
                )
        #Plot CDF
        cfd.plot(samples=common_vocab)

    def important_words(self, length, frequency, perArticle=False):
        """Returns a list with words longer than length chars and occure more than frequency times

        :length: longer than length
        :frequency: occuring more than frequency times
        :categorized: Over all words or per category

        :returns: list/dict of words

        """

        result = {}

        if not(perArticle):
            cat = self.corp.categories()

            for news in cat:
                fd = nlp.FreqDist(self.words[news])

                words = [w for w in self.norm_vocab[news] if len(w) > length and fd[w] > frequency]
                result.update({news: words})

        return result

    def __create_corpus(self, language, chars):
        """Create a categorized nltk.corpus from data/* where the subfolders are the different categories.

        :chars: List of chars which will be additionally to stopwords  removed before the statistical analysis
        :language: The newspaper language as string
        :returns: nltk.corpus, list(all normalized words)

        """

        # Create corpus from data directory
        news_corpus = CategorizedPlaintextCorpusReader('data/', r'.*\.txt', cat_pattern=r'(\w+)/*')

        # Get all german stopwords and addition chars for removal
        g_stop = stopwords.words(language)
        g_stop.extend(chars)

        # Stemmer
        snow = nlp.stem.SnowballStemmer(language, ignore_stopwords=True)

        # Dict of all words/category
        cat = news_corpus.categories()
        total_words = {}

        for news in cat:
            #Get the words
            words = news_corpus.words(categories=news)

            # Remove stopwords and tokenize
            words = [w.lower() for w in words if w not in g_stop]

            # Stem all tokens
            words = [snow.stem(w) for w in words]

            total_words.update({news: words})

        return news_corpus, total_words

    def text_concordance(self, word, text):
        """Returns all concordandes for the nltk.text

        :word: word/wordstem/substring 
        :text: nltk text
        :returns: concordance string

        """

        # Initialize variable
        concordance = io.StringIO()

        # Get all string with word as substring 
        # The word may be somewhere in the middle
        #words = set([w for w in text.tokens if re.findall("\\b\\w*"+word+"\\w*\\b",w)])
        # The word has to be at the start of a given word
        words = set([w for w in text.tokens if re.findall("\\b"+word+"\\w*\\b",w)])

        # Get all concordances
        with redirect_stdout(concordance):
            for w in words:
                text.concordance(w)

        # Save and close the IO object
        result = concordance.getvalue()
        concordance.close()

        # Remove headers and double newlines from nltk concordance output
        result = re.sub("Displaying.*matches:","",result)
        result = re.sub("\\n\\n","\\n",result)

        return result

    def corpus_concordance(self, word, corpus):
        """Returns all concodrdances in the corpus

        :word: word/wordstem/substring
        :corpus: nltk corpus
        :returns: concordance string

        """
        concordance = ""

        # Initialize variable
        for file in corpus.fileids():
            text = nlp.Text([w.lower() for w in corpus.words(file)])

            concordance += self.text_concordance(word,text)
        return concordance

    # Plotting

    # Plot a CDF
    # fd.plot(20, cumulative=True)

    # fd_wl.plot()




