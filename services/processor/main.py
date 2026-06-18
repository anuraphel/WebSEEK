import os
import time
import re
from collections import Counter
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class InvertedIndex(Base):
    __tablename__ = 'inverted_index'
    word = Column(String, primary_key=True)
    document_ids = Column(JSON) # Storing as JSON for simplicity in this demo

class Processor:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL", "postgresql://admin:password123@db:5432/search_engine")
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def tokenize(self, text):
        """Simple tokenization: lowercase and remove non-alphanumeric."""
        if not text:
            return []
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def update_index(self):
        """Read web_pages, generate inverted index entries."""
        session = self.Session()
        try:
            # For simplicity, we process all pages. In a real system, use a 'processed' flag.
            from sqlalchemy import text as sql_text
            pages = session.execute(sql_text("SELECT id, content FROM web_pages")).fetchall()
            
            global_index = {}
            for page_id, content in pages:
                tokens = set(self.tokenize(content)) # Use set for presence in doc
                for token in tokens:
                    if token not in global_index:
                        global_index[token] = []
                    global_index[token].append(page_id)

            # Update database
            for word, doc_ids in global_index.items():
                # This is a naive update. In production, use upserts.
                session.execute(
                    sql_text("INSERT INTO inverted_index (word, document_ids) VALUES (:word, :doc_ids) "
                             "ON CONFLICT (word) DO UPDATE SET document_ids = EXCLUDED.document_ids"),
                    {"word": word, "doc_ids": doc_ids}
                )
            session.commit()
            print(f"Index updated with {len(global_index)} words.")
        except Exception as e:
            session.rollback()
            print(f"Error updating index: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    processor = Processor()
    while True:
        print("Running index update pipeline...")
        processor.update_index()
        time.sleep(60) # Run every minute
