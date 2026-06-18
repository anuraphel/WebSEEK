-- Schema for Distributed Search Engine

CREATE TABLE IF NOT EXISTS web_pages (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    content TEXT,
    raw_html TEXT,
    hash VARCHAR(64), -- To detect content changes
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP
);

CREATE INDEX idx_url ON web_pages(url);
CREATE INDEX idx_crawled_at ON web_pages(crawled_at);

-- For Inverted Index (simplified logic, Member 2 might extend this)
CREATE TABLE IF NOT EXISTS inverted_index (
    word VARCHAR(255) PRIMARY KEY,
    document_ids INTEGER[] -- Array of web_page IDs
);
