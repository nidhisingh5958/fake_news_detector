import requests
import feedparser
from datetime import datetime, timedelta
import re
from urllib.parse import urlparse
import time

class NewsFetcher:
    def __init__(self):
        self.news_sources = {
            'reuters': 'http://feeds.reuters.com/reuters/topNews',
            'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'ap': 'https://feeds.apnews.com/rss/apf-topnews',
            'npr': 'https://feeds.npr.org/1001/rss.xml',
            'cnn': 'http://rss.cnn.com/rss/edition.rss'
        }
        self.cached_news = []
        self.last_fetch = None
        self.cache_duration = timedelta(hours=1)
    
    def fetch_current_news(self):
        """Fetch current news from multiple sources"""
        if self.last_fetch and datetime.now() - self.last_fetch < self.cache_duration:
            return self.cached_news
        
        all_articles = []
        
        for source, url in self.news_sources.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:  # Get top 10 from each source
                    article = {
                        'title': entry.title,
                        'summary': getattr(entry, 'summary', ''),
                        'source': source,
                        'published': getattr(entry, 'published', ''),
                        'link': getattr(entry, 'link', '')
                    }
                    all_articles.append(article)
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"Error fetching from {source}: {e}")
                continue
        
        self.cached_news = all_articles
        self.last_fetch = datetime.now()
        return all_articles
    
    def get_news_keywords(self):
        """Extract keywords from current news"""
        articles = self.fetch_current_news()
        keywords = set()
        
        for article in articles:
            text = f"{article['title']} {article['summary']}".lower()
            # Extract meaningful words (3+ chars, not common words)
            words = re.findall(r'\b[a-z]{3,}\b', text)
            keywords.update(words)
        
        # Remove common words
        common_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        return keywords - common_words
    
    def check_news_relevance(self, text):
        """Check if text relates to current news topics"""
        current_keywords = self.get_news_keywords()
        text_words = set(re.findall(r'\b[a-z]{3,}\b', text.lower()))
        
        overlap = len(text_words.intersection(current_keywords))
        relevance_score = overlap / max(len(text_words), 1) * 100
        
        return {
            'relevance_score': relevance_score,
            'matching_keywords': list(text_words.intersection(current_keywords)),
            'is_news_related': relevance_score > 10
        }