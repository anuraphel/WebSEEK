import redis
import os

class URLQueue:
    def __init__(self):
        self.redis = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        self.queue_key = "url_queue"
        self.visited_key = "visited_urls"

    def push(self, url):
        """Push a URL to the queue if it hasn't been visited."""
        if not self.redis.sismember(self.visited_key, url):
            self.redis.lpush(self.queue_key, url)

    def pop(self):
        """Pop a URL from the queue."""
        url = self.redis.rpop(self.queue_key)
        if url:
            return url.decode('utf-8')
        return None

    def mark_visited(self, url):
        """Mark a URL as visited."""
        self.redis.sadd(self.visited_key, url)

    def is_visited(self, url):
        """Check if a URL has been visited."""
        return self.redis.sismember(self.visited_key, url)

    def size(self):
        """Return the number of URLs in the queue."""
        return self.redis.llen(self.queue_key)
