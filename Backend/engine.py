import os
import sys
import requests
import subprocess
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from loguru import logger
from db_management.supabase_handler import DBHandler

app = FastAPI(title="SentinoMind AI Backend")

# --- Models ---
class PipelineRequest(BaseModel):
    page_id: str

class PostRequest(BaseModel):
    page_id: str
    page_key: str
    db_row_id: str
    page_name: str

# --- Path Setup ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Adjust this to point exactly to your main.py (AI logic script)
SCRIPT_PATH = os.path.join(CURRENT_DIR, "main.py")

# --- Helper Functions ---
def run_main_script(page_id: str):
    try:
        logger.info(f"📡 Pipeline started for: {page_id}")
        
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, page_id],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(SCRIPT_PATH),  # ← project root as working dir
            check=True
        )
        
        logger.info("--- MAIN.PY LOGS START ---")
        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.info(result.stderr)  # loguru writes here
        logger.info("--- MAIN.PY LOGS END ---")
        logger.success(f"✅ Pipeline Finished for {page_id}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Main.py crashed!")
        logger.error(f"STDERR: {e.stderr}")
        logger.error(f"STDOUT: {e.stdout}")

# --- Endpoints ---
@app.get("/")
def home():
    return {"status": "online", "message": "SentinoMind Backend is running"}

@app.post("/run-pipeline")
async def run_pipeline_endpoint(request: PipelineRequest, background_tasks: BackgroundTasks):
    # Running the AI script in the background so the UI doesn't freeze
    background_tasks.add_task(run_main_script, request.page_id)
    return {"status": "started", "message": "AI Pipeline is running in background."}

@app.post("/post-to-page")
async def process_and_post(request: PostRequest):
    db = DBHandler()
    try:
        # 1. Fetch content from Supabase
        response = db.supabase.table("sentino_pipeline")\
            .select("post_content, image_url, title_name, unique_id")\
            .eq("unique_id", request.db_row_id)\
            .single().execute()
        
        row_data = response.data
        if not row_data:
            raise HTTPException(status_code=404, detail="Data not found in DB.")

        message = row_data.get("post_content") or row_data.get("title_name")
        img_url = row_data.get("image_url")
        
        # 2. Facebook Graph API Logic
        target = "photos" if img_url else "feed"
        fb_url = f"https://graph.facebook.com/v22.0/{request.page_id}/{target}"
        
        payload = {
            "access_token": request.page_key,
            ("caption" if target == "photos" else "message"): message
        }
        if img_url:
            payload["url"] = img_url

        fb_res = requests.post(fb_url, data=payload)
        result = fb_res.json()

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"]["message"])

        # 3. Update DB Status
        db.update_user_page_id_and_name(
            page_id=request.page_id, 
            unique_id=request.db_row_id,
            page_name=request.page_name
        )
        db.supabase.table("sentino_pipeline").update({"status": "Published"}).eq("unique_id", request.db_row_id).execute()

        return {"status": "success", "fb_id": result.get("id")}

    except Exception as e:
        logger.error(f"Post Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)