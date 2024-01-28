from pathlib import Path


RESULTS = 'results'
NEW_BOOKS = 'new_books'
REMOVED_BOOKS = 'removed_books'

BASE_DIR = Path(__file__).parent
RESULTS_DIR = BASE_DIR / RESULTS

SCROLLS = 0

BOT_NAME = "books"

SPIDER_MODULES = ["books.spiders"]
NEWSPIDER_MODULE = "books.spiders"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    f'{RESULTS_DIR}/books_%(time)s.csv': {
        'format': 'csv',
        'fields': ['author', 'title', 'rating', 'ratings', 'genres', 'link'],
        'overwrite': True,
    },
}

ITEM_PIPELINES = {
    'books.pipelines.HitBookParserPipeline': 300,
}
