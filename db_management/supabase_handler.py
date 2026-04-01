import os
import uuid
from supabase import create_client
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

class DBHandler:
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        if not url or not key:
            logger.critical("❌ SUPABASE_URL or SUPABASE_KEY not found in environment variables!")
            
        self.supabase = create_client(url, key)
        self.table_name = "sentino_pipeline"
        self.bucket_name = "my_bucket"

    def generate_unique_id(self):
        """Generating a six-digit unique ID"""
        return f"SN-{uuid.uuid4().hex[:6].upper()}"
    
    # --- ইনজেশন পার্ট ---
    def insert_raw_news(self,page_id, title, context, category):
        """প্রাথমিক নিউজ ডেটাবেসে সেভ করা"""
        unique_id = self.generate_unique_id()
        try:
            data = {
                "unique_id": unique_id,
                "page_id": page_id,
                "title_name": title,
                "main_context": context,
                "news_category": category,
                "status": "raw"
            }
            self.supabase.table(self.table_name).insert(data).execute()
            logger.success(f"💾 Ingested: {unique_id} | {title[:40]}...")
            return unique_id
        except Exception as e:
            logger.error(f"❌ Database Insertion Error: {e}")
            return None

    # --- ফেচিং পার্ট ---
    def fetch_raw_for_processing(self,page_id):
        """প্রসেসিং এর জন্য 'raw' স্ট্যাটাসের নিউজ আনা"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("page_id", page_id)
                .eq('status', 'raw')
                .limit(5)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"❌ Failed to fetch raw news: {e}")
            return []

    def fetch_ready_for_images(self,page_id):
        """ইমেজ তৈরির জন্য 'ready' স্ট্যাটাসের নিউজ আনা"""
        try:
            response = (
                self.supabase.table(self.table_name)
                .select("*")
                .eq("page_id", page_id)
                .eq('status', 'ready')
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"❌ Error fetching for images: {e}")
            return []

    # --- আপডেট পার্ট ---
    def update_enriched_content(self, unique_id, summary, post_content):
        """AI দিয়ে তৈরি করা কন্টেন্ট আপডেট করা"""
        try:
            data = {
                "summary": summary,
                "post_content": post_content,
                "status": "ready"
            }
            self.supabase.table(self.table_name).update(data).eq("unique_id", unique_id).execute()
            logger.success(f"🚀 Content Enriched & Ready: {unique_id}")
        except Exception as e:
            logger.error(f"❌ Failed to update enriched content: {e}")

    def update_processed_image(self, unique_id, image_url, visual_prompt):
        """ইমেজ ইউআরএল এবং প্রম্পট সেভ করে স্ট্যাটাস 'final' করা"""
        try:
            data = {
                "image_url": image_url,
                "visual_prompt": visual_prompt,
                "status": "final"
            }
            self.supabase.table(self.table_name).update(data).eq("unique_id", unique_id).execute()
            logger.success(f"✅ Final data updated for ID: {unique_id}")
            return True
        except Exception as e:
            logger.error(f"❌ DB Update Error: {e}")
            return False

    # --- স্টোরেজ পার্ট ---
    def upload_to_storage(self, file_name, file_content):
        """ইমেজ আপলোড করে পাবলিক ইউআরএল রিটার্ন করা"""
        try:
            # Bucket এ আপলোড
            self.supabase.storage.from_(self.bucket_name).upload(
                path=file_name,
                file=file_content,
                file_options={"content-type": "image/jpeg", "upsert": "true"}
            )
            
            # পাবলিক ইউআরএল সংগ্রহ
            res = self.supabase.storage.from_(self.bucket_name).get_public_url(file_name)
            
            # রেজাল্ট থেকে সঠিক ইউআরএল স্ট্রিং বের করা
            if hasattr(res, 'public_url'):
                return res.public_url
            if isinstance(res, dict):
                return res.get('publicURL') or res.get('public_url')
            return res
            
        except Exception as e:
            logger.error(f"❌ Storage Upload Error: {e}")
            return None

    def delete_boring_news(self, unique_id):
        """ডেটাবেস থেকে অপ্রয়োজনীয় নিউজ মুছে ফেলা"""
        try:
            self.supabase.table(self.table_name).delete().eq("unique_id", unique_id).execute()
            logger.warning(f"🗑️ Deleted boring news: {unique_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete record: {e}")
            return False
    
    def get_pending_posts(self,page_id, limit=5):
        try:
            # এখানে 'enriched' এর বদলে 'ready' দিন, কারণ PostCreator 'ready' সেট করে
            response = self.supabase.table(self.table_name)\
                .select("*")\
                .eq("page_id", page_id)\
                .limit(limit)\
                .execute()
                
            posts = response.data
            return posts
        except Exception as e:
            logger.error(f"❌ Error fetching pending posts: {e}")
            return []
        
    def update_user_page_id_and_name(self, page_id, page_name, unique_id):
        try:
            data = {
                'page_id': page_id,
                'page_name': page_name
            }
            self.supabase.table(self.table_name).update(data).eq('unique_id', unique_id).execute()
            
            logger.success(f'Page ID {page_id} saved successfully for row {unique_id}')
        except Exception as e:
            logger.error(f'Failed to save Page ID: {e}')