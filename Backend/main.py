import time
import sys
import os
from loguru import logger
from dotenv import load_dotenv

# এনভায়রনমেন্ট লোড করা (এটি সবার আগে থাকা জরুরি)
load_dotenv()

# পাথ সেটআপ নিশ্চিত করা
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

try:
    from content_engine.news_fetcher import NewsFetcher
    from content_engine.post_creator import PostCreator
    from content_engine.image_gen import ImageGenerator
    from db_management.supabase_handler import DBHandler
    logger.success("✅ All modules imported successfully!")
except ImportError as e:
    logger.error(f"❌ Import Error: {e}")
    sys.exit(1)

def run_pipeline(page_id):
    logger.info(f"🚀 Starting Pipeline for Page: {page_id}")
    db = DBHandler()
    
    try:
        # ১. নিউজ ফেচিং
        fetcher = NewsFetcher()
        fetcher.fetch_and_store(page_id=page_id)
        logger.info("✅ Step 1: News fetching done.")

        # ২. পোস্ট ক্রিয়েশন
        creator = PostCreator()
        creator.analyze_and_generate(page_id=page_id)
        logger.info("✅ Step 2: Content generation done.")

        # ৩. ইমেজ জেনারেশন (এখানেই সমস্যা হতে পারে)
        image_gen = ImageGenerator()
        pending_posts = db.fetch_ready_for_images(page_id=page_id) 
        
        # ডিব্যাগ মেসেজ
        logger.info(f"🔍 Debug: Found {len(pending_posts) if pending_posts else 0} posts with 'ready' status.")

        if not pending_posts:
            logger.warning("☕ No 'ready' posts found. Check if PostCreator updated the status correctly.")
        else:
            for post in pending_posts:
                logger.info(f"🎨 Generating image for ID: {post.get('unique_id')}")
                image_gen.generate_and_update(post['unique_id'], post['news_category'], post['title_name'])
        
        logger.success("🏁 Pipeline Finished!")
    except Exception as e:
        logger.error(f"💥 Error: {str(e)}")

if __name__ == "__main__":
    # কমান্ড লাইন থেকে page_id রিসিভ করা
    if len(sys.argv) > 1:
        target_page_id = sys.argv[1]
    else:
        target_page_id = "test_page_id"
        logger.warning(f"⚠️ No Page ID provided. Using default: {target_page_id}")
        
    run_pipeline(target_page_id)