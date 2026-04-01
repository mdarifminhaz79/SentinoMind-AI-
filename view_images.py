import webbrowser
import os
import sys
from loguru import logger

# প্রোজেক্ট পাথ সেটআপ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from db_management.supabase_handler import DBHandler

db = DBHandler()

def view_sentino_images(limit=5):
    table_name = "sentino_pipeline"  # আপনার আসল টেবিল নাম
    column_name = "image_url"        # আপনার আসল কলাম নাম
    
    try:
        logger.info(f"🚀 Fetching images from '{table_name}' table...")
        
        # ডাটাবেস থেকে ইমেজ আছে এমন রো গুলো সিলেক্ট করা হচ্ছে
        response = db.supabase.table(table_name) \
            .select(f"title_name, {column_name}") \
            .not_.is_(column_name, "null") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()

        if not response.data:
            logger.warning("No images found in the 'image_url' column yet.")
            return

        logger.success(f"✅ Found {len(response.data)} images! Opening in browser...")
        
        for record in response.data:
            title = record.get('title_name', 'Untitled')
            url = record.get(column_name)
            
            if url and "http" in str(url):
                print(f"\n📰 Title: {title}")
                print(f"🖼️ Image: {url}")
                # ব্রাউজারে ছবি ওপেন করা
                webbrowser.open(url)
            
    except Exception as e:
        logger.error(f"Something went wrong: {e}")

if __name__ == "__main__":
    view_sentino_images(limit=5) # শেষ ৫টি ছবি দেখাবে