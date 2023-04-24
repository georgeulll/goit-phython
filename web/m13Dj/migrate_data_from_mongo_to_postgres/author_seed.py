from quotes.quotes.settings import DATABASES

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, Boolean, func, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
import json
from pathlib import Path

username = DATABASES['default']['USER']
password = DATABASES['default']['PASSWORD']
db_name = DATABASES['default']['NAME']
host = DATABASES['default']['HOST']
port = DATABASES['default']['PORT']

url_to_db = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'

engine = create_engine(url_to_db, echo=True, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Author(Base):
    __tablename__ = "app_quotes_author"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    born_date = Column(Date)
    born_location = Column(String(100), nullable=False)
    description = Column(String)
    user_id = Column(Integer)


class Tag(Base):
    __tablename__ = "app_quotes_tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer)

    quote_rel = relationship("Quote", secondary='app_quotes_quotes_tag',
                             back_populates='tag_rel', passive_deletes=True)


class Quote(Base):
    __tablename__ = "app_quotes_quotes"
    id = Column(Integer, primary_key=True)
    quote_text = Column(String)
    author_id = Column('author_id', ForeignKey('app_quotes_author.id', ondelete='CASCADE'))
    user_id = Column(Integer)

    tag_rel = relationship("Tag", secondary="app_quotes_quotes_tag",
                           back_populates='quote_rel', passive_deletes=True)


class QuotesToTag(Base):
    __tablename__ = "app_quotes_quotes_tag"
    id = Column(Integer, primary_key=True)
    quotes_id = Column('quotes_id', ForeignKey('app_quotes_quotes.id', ondelete='CASCADE'))
    tag_id = Column('tag_id', ForeignKey('app_quotes_tag.id', ondelete='CASCADE'))


def read_json_file(file_name: str, encoding: str = 'utf-8'):
    file_path = Path('.', file_name)
    with open(file_path, 'r', encoding=encoding) as file:
        data = json.load(file)
    return data


def seed_author():
    authors = read_json_file('authors.json')
    for author in authors:
        a = Author(fullname=author['fullname'],
                   born_date=author['born_date'],
                   born_location=author['born_location'],
                   description=author['description'],
                   user_id=1
                   )

        session.add(a)
    session.commit()


def seed_quotes():
    quotes = read_json_file('quotes.json')
    for quote in quotes:
        if quote['author'] == 'Alexandre Dumas fils':
            a_id = session.query(Author.id).select_from(Author).filter(Author.fullname == 'Alexandre Dumas-fils')
        else:
            a_id = session.query(Author.id).select_from(Author).filter(Author.fullname == quote['author'])
        q = Quote(quote_text=quote['quote'],
                  author_id=a_id,
                  user_id=1
                  )

        session.add(q)
    session.commit()


def seed_tag():
    quotes = read_json_file('quotes.json')
    tags_basket = []
    for quote in quotes:
        for element in quote['tags']:
            if element in tags_basket:
                continue
            else:
                tags_basket.append(element)

    for tag in tags_basket:
        t = Tag(name=tag,
                user_id=1)

        session.add(t)
    session.commit()


def seed_quotes_to_tag():
    quotes = read_json_file('quotes.json')

    # tags=session.query(Tag).all
    # quotes_=session.query(Quote).all
    for quote in quotes:
        q_id = session.query(Quote.id).select_from(Quote).filter(Quote.quote_text == quote['quote'])
        t_id = session.query(Tag.id).select_from(Tag).filter(Tag.name in quote['tags'])
        qt = QuotesToTag(quotes_id=q_id,
                         tag_id=t_id,
        )
        session.add(qt)
    session.commit()


if __name__ == '__main__':
    # seed_author()
    # seed_quotes()
    # seed_tag()
    seed_quotes_to_tag()