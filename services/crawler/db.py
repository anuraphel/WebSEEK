import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class WebPage(Base):
    __tablename__ = 'web_pages'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String)
    content = Column(Text)
    raw_html = Column(Text)
    hash = Column(String(64))
    crawled_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_modified = Column(DateTime)

class DBManager:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/search_engine")
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def save_page(self, url, title, content, raw_html):
        session = self.Session()
        try:
            page = WebPage(
                url=url,
                title=title,
                content=content,
                raw_html=raw_html
            )
            session.merge(page) # merge handles updates if URL already exists
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error saving page {url}: {e}")
        finally:
            session.close()
