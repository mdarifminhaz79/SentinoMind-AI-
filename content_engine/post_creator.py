import os
import sys
from loguru import logger
from groq import Groq
from dotenv import load_dotenv

# adding root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from db_management.supabase_handler import DBHandler

load_dotenv()

class PostCreator:
    def __init__(self):
        self.db = DBHandler()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"

    def analyze_and_generate(self, page_id):
        """Analyzing and creating posts from news from the database"""
        #1. 
        pending_news = self.db.fetch_raw_for_processing(page_id)

        if not pending_news:
            logger.info('😴 No raw news to process.')
            return
        
        for news in pending_news:
            unique_id = news['unique_id']
            title = news['title_name']
            context = news['main_context']
            category = news['news_category']

            logger.info(f"🧐 Analyzing: {title[:50]}...")

            # Using GROQ Ai to check the news

            prompt = f"""
            Analyze this news and decide if it's interesting for a viral social media page.
            News Title: {title}
            Context: {context[:2000]}

            If it's boring, political propaganda, or just plain old news, reply ONLY with 'DELETE'.
            If it's interesting/viral, reply in this format:
            SUMMARY: [2 line summary]
            POST: [Witty viral Facebook post with emojis]
            """
            # POST: [Witty viral Facebook post with emojis]
            # PROMPT: [High quality image generation prompt for this news]

            try:
                response = self.client.chat.completions.create(
                    messages = [
                        {
                            'role': "user",
                            'content': prompt
                        }
                    ],
                    model=self.model
                )
                ai_output = response.choices[0].message.content

                if "DELETE" in ai_output:
                    # removing the boring context from db
                    self.db.delete_boring_news(unique_id)
                else:
                    # separating summary,post,prompt
                    lines = ai_output.split('\n')

                    summary = ""
                    post_content = ""
                    # image_prompt = ""

                    for line in lines:
                        if line.startswith("SUMMARY:"): summary = line.replace("SUMMARY:", "").strip()
                        if line.startswith("POST:"): post_content = line.replace("POST:", "").strip()
                        # if line.startswith("PROMPT:"): image_prompt = line.replace("PROMPT:", "").strip()

                    #5. Updating database (status: ready)
                    self.db.update_enriched_content(
                        unique_id=unique_id,
                        summary=summary,
                        # image_url=image_prompt,
                        post_content=post_content
                    )
            
            except Exception as e:
                logger.error(f"❌ AI Analysis failed for {unique_id}: {e}")


# --- Test Script ---
if __name__ == "__main__":
    creator = PostCreator()
    creator.analyze_and_generate()