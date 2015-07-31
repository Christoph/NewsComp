try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'NLP news comparer',
    'author': 'Christoph Kral',
    'url': 'Christoph.github.io',
    'download_url': 'Github',
    'author_email': 'christoph.kralj@gmail.com',
    'license': 'MIT',
    'version': '0.1',
    'install_requires': ['nose', 'bs4','urllib','lxml','re','numpy','nltk'],
    'packages': ['newscomp'],
    'scripts': [],
    'name': 'NewsComparer'
}

setup(**config)
