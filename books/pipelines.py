import csv

from datetime import datetime as dt
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from books.settings import NEW_BOOKS, REMOVED_BOOKS, RESULTS_DIR

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    title = Column(String)
    rating = Column(Float)
    ratings = Column(Integer)
    genres = Column(String)
    link = Column(String)


class HitBookParserPipeline:
    def __init__(self):
        RESULTS_DIR.mkdir(exist_ok=True)
        engine = create_engine('sqlite:///sqlite.db')
        self.session = Session(engine)
        Base.metadata.create_all(engine)
        self.books_from_old_db = [
            (author, title) for author, title
            in self.session.query(Book.author, Book.title).all()
        ]
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.new_books = []

    def process_item(self, item, spider):
        book = Book(
            author=item['author'],
            title=item['title'],
            rating=item['rating'],
            ratings=item['ratings'],
            genres=item['genres'],
            link=item['link']
        )
        self.session.add(book)
        self.session.commit()
        if (book.author, book.title) not in self.books_from_old_db:
            self.new_books.append((book.author, book.title))
        return item

    def close_spider(self, spider):
        current_time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_books_path = RESULTS_DIR / f'{NEW_BOOKS}_{current_time}.csv'
        removed_books_path = (
            RESULTS_DIR / f'{REMOVED_BOOKS}_{current_time}.csv'
        )
        books_from_new_db = [
            (author, title) for author, title
            in self.session.query(Book.author, Book.title).all()
        ]
        retired_books = [
            (author, title) for author, title in self.books_from_old_db
            if (author, title) not in books_from_new_db
        ]
        if self.new_books:
            with open(new_books_path, mode='w', encoding='utf-8') as csvfile:
                csv.writer(
                    csvfile,
                    dialect=csv.unix_dialect,
                    quoting=csv.QUOTE_MINIMAL,
                ).writerows([
                    ('Author', 'Title'),
                    *self.new_books,
                ])
        if retired_books:
            with open(
                removed_books_path, mode='w', encoding='utf-8'
            ) as csvfile:
                csv.writer(
                    csvfile,
                    dialect=csv.unix_dialect,
                    quoting=csv.QUOTE_MINIMAL,
                ).writerows([
                    ('Author', 'Title'),
                    *retired_books,
                ])
        self.session.close()
