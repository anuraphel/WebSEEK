from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# DB Setup
DB_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@db:5432/search_engine")
engine = sa.create_engine(DB_URL)
Session = sessionmaker(bind=engine)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def search(q: str = Query(...)):
    session = Session()
    try:
        # 1. Lookup word in inverted index
        query = sa.text("SELECT document_ids FROM inverted_index WHERE word = :word")
        result = session.execute(query, {"word": q.lower()}).fetchone()
        
        if not result:
            return []

        doc_ids = result[0]
        if not doc_ids:
            return []

        # 2. Get page details for those IDs
        pages_query = sa.text("SELECT url, title, content FROM web_pages WHERE id = ANY(:ids)")
        pages = session.execute(pages_query, {"ids": doc_ids}).fetchall()

        results = []
        for page in pages:
            results.append({
                "url": page.url,
                "title": page.title or page.url,
                "snippet": page.content[:200] + "..." if page.content else ""
            })
        
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return {"error": str(e)}
    finally:
        session.close()
