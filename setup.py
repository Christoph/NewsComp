try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'News comparator',
    'author': 'Christoph Kralj',
    'url': 'Christoph.github.io',
    'download_url': 'Github',
    'author_email': 'christoph.kralj@gmail.com',
    'license': 'MIT',
    'version': '0.1',
    'install_requires': ['nose', 'bs4','urllib','lxml','re','numpy','nltk','socketio'],
    'packages': ['newscomp'],
    'scripts': [],
    'name': 'NewsComparer'
}

setup(**config)
