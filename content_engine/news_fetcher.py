import os
import requests
from loguru import logger
from newspaper import Article
from dotenv import load_dotenv
import sys

# রুট পাথ অ্যাড করা যাতে db_management পায়
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_management.supabase_handler import DBHandler

load_dotenv()

class NewsFetcher:
    def __init__(self):
        self.serper_key = os.getenv("SERPER_API_KEY")
        self.search_url = "https://google.serper.dev/news"
        self.db = DBHandler()
        
        self.categories = [
            "world news",
            "sports",
            "technology",
            "entertainment"
        ]

    def extract_article_context(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text if len(article.text) > 150 else None
        except:
            return None

    def fetch_and_store(self,page_id):
        total_count = 0
        if not self.serper_key:
            logger.error("❌ SERPER_API_KEY missing in .env file!")
            return 0

        for category in self.categories:
            logger.info(f"🌐 Searching for: {category}")
            
            headers = {
                'X-API-KEY': self.serper_key,
                'Content-Type': 'application/json'
            }
            payload = {"q": category, "gl": "us"}

            try:
                response = requests.post(self.search_url, headers=headers, json=payload)
                res_data = response.json()

                # ডিবাগিং: যদি ডাটা না আসে তবে পুরো রেসপন্স প্রিন্ট হবে
                if "news" not in res_data:
                    logger.error(f"API Error for {category}: {res_data}")
                    continue

                news_items = res_data.get('news', [])
                
                for item in news_items[:3]:
                    title = item.get('title')
                    link = item.get('link')
                    
                    context = self.extract_article_context(link)
                    if context:
                        success_id = self.db.insert_raw_news(page_id=page_id, title=title, context=context, category=category)
                        if success_id:
                            logger.success(f"📌 Stored: {success_id}")
                            total_count += 1
                
            except Exception as e:
                logger.error(f"❌ System Error: {e}")

        return total_count

if __name__ == "__main__":
    fetcher = NewsFetcher()
    added = fetcher.fetch_and_store(page_id="test_page_id")
    print(f"\n🔥 Total added: {added}")