import streamlit as st
import pandas as pd
import os
import sys
import requests
import urllib.parse
from io import BytesIO

# --- 1. FACEBOOK POSTING FUNCTION ---
def post_to_fb(message, image_url=None):
    """ফেসবুক পেজে টেক্সট (এবং সম্ভব হলে ছবি) পোস্ট করার ফাংশন"""
    PAGE_ID = "968206979717398" 
    ACCESS_TOKEN = "EAANT89eXPx4BQ6TrctZANoIHlabrJheGqZCGvnBPWs7e9y8vOCCIC1L5gjgrIZA0pJFYI1jSHI13eeYRb8zKXR19ybethio82gnmwWuLICuCzXIBqhoKrvBCRZBfRrc68ZA0EjTkYh9kkPZBMIYIm86FPZBBCzlokTsF2WL43d1IXA2QqBwUJZBs5txdXbQka7bO4bXzYZBqlvcZBdNhGmecBuNYhxYJk84oB3IQL8y1EZD" 
    
    # যদি ইমেজ থাকে তবে আলাদা এন্ডপয়েন্ট ব্যবহার করা যায়, আপাতত ফিড এন্ডপয়েন্ট ব্যবহার করছি
    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"
    
    payload = {
        'message': message,
        'access_token': ACCESS_TOKEN
    }
    
    if image_url:
        payload['link'] = image_url  # ছবিকে লিঙ্ক হিসেবে শেয়ার করবে

    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"error": {"message": str(e)}}

# --- 2. PATH & DB SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from db_management.supabase_handler import DBHandler
    db_ready = True
except ImportError:
    st.error("❌ Could not find 'db_management' folder. Check your folder structure.")
    db_ready = False

# --- 3. UTILITY FUNCTIONS ---
def get_safe_url(url):
    """ইউআরএল-এর স্পেস বা স্পেশাল ক্যারেক্টার এনকোড করার জন্য"""
    if not url or not isinstance(url, str):
        return None
    return urllib.parse.quote(url, safe=':/?=&')

def load_data():
    """Supabase থেকে লেটেস্ট ডাটা রিড করা"""
    db = DBHandler()
    try:
        response = db.supabase.table("sentino_pipeline").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- 4. PAGE CONFIG ---
st.set_page_config(page_title="SentinoMind AI Dashboard", layout="wide", page_icon="🤖")

def main():
    if not db_ready: return
    
    st.title("🤖 SentinoMind AI - Content Command Center")
    st.markdown("---")

    df = load_data()
    if df.empty:
        st.warning("📭 No data found in 'sentino_pipeline' table.")
        if st.button("🔄 Refresh"): st.rerun()
        return

    # --- SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Controls")
        if st.button("🔄 Refresh Dashboard"): st.rerun()
        st.markdown("---")
        
        if 'status' in df.columns:
            all_statuses = df['status'].unique().tolist()
            status_filter = st.multiselect("Filter by Status", options=all_statuses, default=all_statuses)
            filtered_df = df[df['status'].isin(status_filter)]
        else:
            filtered_df = df

    # --- MAIN FEED LOOP ---
    for _, row in filtered_df.iterrows():
        unique_id = row.get('unique_id')
        status = row.get('status', 'N/A')
        image_url = row.get('image_url')
        title = row.get('title_name', 'Untitled News')
        
        # কন্টেন্ট লজিক
        post_body = str(row.get('post_content') or '').strip()
        summary = str(row.get('summary') or '').strip()
        final_display = post_body if post_body else (summary if summary else "")

        with st.container():
            # ৩ কলামের লেআউট: [Image, Text Content, Actions]
            col_img, col_txt, col_meta = st.columns([1.5, 2.5, 1], gap="medium")

            # কলাম ১: ইমেজ ডিসপ্লে
            with col_img:
                if image_url:
                    safe_img_url = get_safe_url(image_url)
                    st.image(safe_img_url, use_container_width=True, caption=f"ID: {unique_id}")
                else:
                    st.info("🖼️ No image generated yet.")

            # কলাম ২: টেক্সট কন্টেন্ট ও ডিটেইলস
            with col_txt:
                st.subheader(title)
                tabs = st.tabs(["📝 Final Post", "🎭 Visual Prompt", "📋 Raw Data"])
                
                with tabs[0]:
                    if not final_display:
                        st.warning("AI hasn't written the post content yet.")
                    st.text_area("Edit Content:", value=final_display, height=200, key=f"area_{unique_id}")
                
                with tabs[1]:
                    v_prompt = row.get('visual_prompt', 'N/A')
                    st.code(v_prompt, language=None)
                
                with tabs[2]:
                    st.json(row.to_dict())

            # কলাম ৩: অ্যাকশন এবং স্ট্যাটাস
            with col_meta:
                st.write("### ⚙️ Action")
                st.info(f"**Current Status:** {status}")
                
                if st.button("🚀 Post to Facebook", key=f"btn_{unique_id}"):
                    if final_display:
                        with st.spinner("Uploading to Meta..."):
                            res = post_to_fb(final_display, image_url)
                            if "id" in res:
                                st.success(f"✅ Posted! ID: {res['id']}")
                            else:
                                st.error(f"❌ Error: {res.get('error', {}).get('message', 'Unknown error')}")
                    else:
                        st.error("No text content available to post!")

        st.markdown("---")

if __name__ == "__main__":
    main()