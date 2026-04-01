import time
import streamlit as st
import requests
import pandas as pd
import os
import sys
from groq import Groq
from huggingface_hub import HfApi
from google import genai
from dotenv import load_dotenv, set_key

# --- PATH & DB SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
    
try:
    from db_management.supabase_handler import DBHandler
    db_ready = True
except Exception as e:
    st.error(f'Database handler not found: {str(e)}')
    db_ready = False

# --- UTILS ---
def valid_groq(api_key):
    try:
        client = Groq(api_key=api_key)
        client.models.list()
        return True
    except: return False

def valid_hf(api_key):
    try:
        api = HfApi(token=api_key)
        api.whoami()
        return True
    except: return False

def validate_google(api_key):
    try:
        client = genai.Client(api_key=api_key)
        client.models.list()
        return True
    except: return False

def load_data(page_id):
    db = DBHandler()
    try:
        res = db.supabase.table("sentino_pipeline")\
            .select("*")\
            .eq("page_id", page_id)\
            .in_("status", ["final", "ready"])\
            .order("created_at", desc=True)\
            .execute()
        
        df = pd.DataFrame(res.data)
        
        if not df.empty:
            # final first, then ready
            df['status_order'] = df['status'].map({"final": 0, "ready": 1})
            df = df.sort_values("status_order").drop(columns=["status_order"])
        
        return df
    except Exception as e:
        return pd.DataFrame()
        

# --- MAIN APP CONFIG ---
st.set_page_config(page_title="SentinoMind Dashboard", layout="wide", page_icon="🤖")

def main():
    if not db_ready: return

    st.title("🤖 SentinoMind AI Content Center")

    # 1. Sidebar: AI Configuration
    with st.sidebar:
        st.header("🔑 AI Authentication")
        groq_api = st.text_input("Groq API Key", type="password")
        hf_key = st.text_input("HuggingFace Key", type="password")
        google_ai_key = st.text_input("Google AI Key", type="password")

        if st.button("Save & Validate AI Keys"):
            if not all([groq_api, hf_key, google_ai_key]):
                st.error('Please fill all keys!')
            else:
                with st.spinner('Validating...'):
                    if valid_groq(groq_api) and valid_hf(hf_key) and validate_google(google_ai_key):
                        set_key(".env", 'GROQ_API_KEY', groq_api)
                        set_key(".env", 'HUGGINGFACE_API_KEY', hf_key)
                        set_key(".env", 'GOOGLE_API_KEY', google_ai_key)
                        st.success("✅ Keys validated and saved!")
                    else:
                        st.error("❌ One or more keys are invalid.")

    # 2. Main Area: Facebook Connection
    st.subheader("📲 Facebook Connection")
    col_a, col_b = st.columns(2)
    with col_a:
        input_page_id = st.text_input("Facebook Page ID", type="default", help="Enter your FB Page ID")
    with col_b:
        input_page_key = st.text_input("Page Access Token", type="password")

    if st.button('🚀 Process & Load News'):
        if not input_page_id or not input_page_key:
            st.warning("Please enter both Page ID and Access Token.")
        else:
            with st.spinner('Validating Facebook Access...'):
                # Facebook API Check (GET Request)
                fb_url = f"https://graph.facebook.com/v22.0/{input_page_id}"
                fb_params = {'access_token': input_page_key, 'fields': 'name'}
                fb_res = requests.get(fb_url, params=fb_params)
                
                if fb_res.status_code == 200:
                    page_name = fb_res.json().get('name', 'Unknown Page')
                    
                    # Update Session State
                    st.session_state['page_id'] = input_page_id
                    st.session_state['page_key'] = input_page_key
                    st.session_state['page_name'] = page_name

                    # Run AI Pipeline
                    with st.spinner("⚙️ AI Pipeline is running... this may take a few minutes..."):
                        try:
                            pipeline_res = requests.post(
                                "http://127.0.0.1:8000/run-pipeline",
                                json={"page_id": input_page_id},
                                timeout=600 
                            )
                            
                            if pipeline_res.status_code == 200:
                                # Pipeline সাকসেস হলে ডাটা লোড
                                df = load_data(input_page_id)
                                st.session_state['df'] = df
                                st.success(f"✅ Connected to: **{page_name}**")
                                st.rerun()
                            else:
                                st.error("❌ Pipeline failed. Please check backend logs.")
                        except Exception as e:
                            st.error(f"❌ Backend Offline: {str(e)}")
                else:
                    st.error(f"❌ FB Validation Failed: {fb_res.json().get('error', {}).get('message')}")

    # 3. Render News Items
    if 'df' in st.session_state and st.session_state['df'] is not None:
        st.divider()
        st.header(f"📰 News Feed: {st.session_state.get('page_name', '')}")
        
        for _, row in st.session_state['df'].iterrows():
            render_news_item(
                row, 
                st.session_state['page_id'], 
                st.session_state['page_key'],
                st.session_state['page_name']
            )

def render_news_item(row, page_id, page_key, page_name):
    u_id = row.get('unique_id')
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(row.get('title_name', 'Untitled'))
            st.write(row.get('post_content', ''))
            if row.get('image_url'):
                st.image(row.get('image_url'), width=500)
        
        with col2:
            st.write("### ⚙️ Action")
            status = row.get('status', 'Pending')
            if status == "Published": 
                st.success(f"Status: {status}")
            else: 
                st.info(f"Status: {status}")

            if st.button("🚀 Post to FB", key=f"btn_{u_id}"):
                post_logic(u_id, page_id, page_key, page_name)

def post_logic(u_id, page_id, page_key, page_name):
    with st.spinner("Posting..."):
        try:
            payload = {
                "page_id": page_id,
                "page_key": page_key,
                "db_row_id": str(u_id),
                "page_name": page_name
            }
            r = requests.post("http://127.0.0.1:8000/post-to-page", json=payload)
            if r.status_code == 200:
                st.success("✅ Posted successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"❌ Error: {r.json().get('detail')}")
        except:
            st.error("Backend is offline. Run backend.py first.")

if __name__ == "__main__":
    main()