# -*- coding: utf-8 -*-

# Python imports
import importlib

# NLP stuff
from nltk.corpus import stopwords
import re
import nltk as nlp
from nltk.corpus import CategorizedPlaintextCorpusReader

# My own classes
import web
import core

# Reload custom modules
def reloadall():
    global web
    global core
    web = importlib.reload(web)
    core = importlib.reload(core)

# Call to reload always
reloadall()

# Initialize variables and classes
# Variables
chars_to_remove = [",",".","-","\"",":",";","_","(",")","!","#","'"]

# My classes
webservice = web.FetchArticles()

news = core.NewsComparator()
