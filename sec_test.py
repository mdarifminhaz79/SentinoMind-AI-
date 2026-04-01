import os
import sys
import time
import requests
import urllib.parse
import random
import re
import base64
from io import BytesIO
from groq import Groq
from huggingface_hub import InferenceClient
from loguru import logger
from dotenv import load_dotenv

# adding root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from db_management.supabase_handler import DBHandler

load_dotenv()

class PromptGenerator:
    def __init__(self):
        logger.info("Initializing PromptGenerator with Llama-3.3-70b...")
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = "llama-3.3-70b-versatile"

    def _call_groq(self, system_prompt, user_prompt, temperature=0.7):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ Groq API Error: {e}")
            return None

    def generate_safe_prompt(self, category, context):
        logger.info(f"🔍 Generating prompt for: {category}")

        # Step 1: CONCEPT + VISUAL_PROMPT দুটো আলাদা করে তৈরি
        sys_p = """You are a Visual Prompt Engineer for a news magazine.
Convert news into a safe, metaphorical image prompt.
NO violence, blood, weapons, or real people's names.
Use symbolic objects, environments, color, lighting, and mood instead."""

        usr_p = f"""Category: {category}
News: {context}

Create TWO things:
1. CONCEPT: A 2-sentence description of the mood and symbolism
2. VISUAL_PROMPT: A single cinematic sentence starting with 'A professional photo of...'
   describing ONLY what the camera sees — objects, lighting, colors, composition.
   Do NOT include metaphor explanations or news references in VISUAL_PROMPT.

Format your response exactly like:
CONCEPT: ...
VISUAL_PROMPT: ..."""

        raw = self._call_groq(sys_p, usr_p, temperature=0.8)
        if not raw:
            return None

        # VISUAL_PROMPT লাইনটি বের করা
        visual_match = re.search(r'VISUAL_PROMPT:\s*(.+)', raw, re.IGNORECASE | re.DOTALL)
        prompt = visual_match.group(1).strip().split('\n')[0] if visual_match else raw.strip()
        logger.info(f"📝 Raw visual prompt: {prompt[:100]}...")

        # Step 2: Safety Audit + Refine Loop
        for attempt in range(3):
            logger.info(f"🛡️ Auditing (attempt {attempt + 1}/3)...")
            audit_sys = """You are an AI Safety Auditor for image generation.
Check ONLY for: real person names, gore, weapons, sexual content.
Metaphors and symbols are ALWAYS safe.
Respond ONLY with: 'STATUS: OK' or 'STATUS: REJECTED | FEEDBACK: reason'"""

            audit_res = self._call_groq(audit_sys, f"Audit this image prompt: {prompt}", temperature=0.1)

            if audit_res and "STATUS: OK" in audit_res:
                logger.success(f"✅ Prompt approved: {prompt[:80]}...")
                return prompt

            feedback = audit_res or "Simplify and remove any sensitive elements."
            refine_sys = "Rewrite this image prompt to fix the safety issue. Keep it purely visual and cinematic. Start with 'A professional photo of...'"
            prompt = self._call_groq(refine_sys, f"Prompt: {prompt}\nIssue: {feedback}", temperature=0.6)
            if not prompt:
                return None

        logger.error("❌ Prompt failed safety audit after 3 attempts.")
        return None


class ImageGenerator:
    def __init__(self):
        self.prompt_engine = PromptGenerator()
        self.db = DBHandler()
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")

    def final_sanitize(self, text):
        """শুধু আসল মানুষের নাম সরানো — বাকি সব visual শব্দ রাখা"""
        real_names = [
            "Trump", "Biden", "Musk", "Elon", "Obama", "Putin",
            "Xi Jinping", "Modi", "Zelensky", "Netanyahu",
            "Marlon", "Wayans",
        ]
        for name in real_names:
            text = re.sub(f"\\b{name}\\b", "a famous person", text, flags=re.IGNORECASE)
        return re.sub(r'\s+', ' ', text).strip()[:500]

    def generate_image_binary(self, prompt):

        # শুধু NSFW শব্দ ব্লক — visual/mood শব্দ রাখো
        blocked_nsfw = {"nude", "naked", "sexual", "gore", "blood",
                        "decapitat", "pornograph", "explicit"}
        filtered_p = " ".join([w for w in prompt.split()
                                if w.lower() not in blocked_nsfw])

        # Style booster
        style_suffix = ", photorealistic, cinematic lighting, 8k, award-winning photography, highly detailed"
        final_prompt = (filtered_p + style_suffix)[:500]

        logger.info(f"🎨 Image prompt: {final_prompt[:120]}...")

        # ─── Provider 1: HuggingFace InferenceClient ──────────────────────
        try:
            logger.info("🚀 Trying HuggingFace InferenceClient (provider=auto)...")
            hf_client = InferenceClient(
                provider="auto",
                api_key=self.hf_key,
            )
            pil_image = hf_client.text_to_image(
                prompt=final_prompt,
                model="black-forest-labs/FLUX.1-schnell",
            )
            buf = BytesIO()
            pil_image.save(buf, format="JPEG", quality=95)
            logger.success("✅ HuggingFace success!")
            return buf.getvalue()
        except Exception as e:
            logger.warning(f"⚠️ HF failed: {e}")

        # ─── Provider 2: Pollinations ─────────────────────────────────────
        logger.info("🔄 Trying Pollinations...")
        seed = random.randint(1, 999999)
        encoded_p = urllib.parse.quote(final_prompt[:300])
        pol_url = (
            f"https://image.pollinations.ai/prompt/{encoded_p}"
            f"?model=flux-schnell&width=1024&height=1024&seed={seed}&nologo=true"
        )
        pol_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "image/*",
            "Referer": "https://pollinations.ai/"
        }
        for attempt in range(3):
            wait = (attempt + 1) * 8
            logger.info(f"  Pollinations attempt {attempt + 1}/3 (waiting {wait}s)...")
            time.sleep(wait)
            try:
                resp = requests.get(pol_url, headers=pol_headers, timeout=120)
                ct = resp.headers.get("Content-Type", "")
                logger.debug(f"  {resp.status_code} | {ct} | {len(resp.content)} bytes")
                if resp.status_code == 200 and "image" in ct and len(resp.content) > 10000:
                    logger.success("✅ Pollinations success!")
                    return resp.content
                if resp.status_code in (502, 503, 504):
                    logger.warning(f"  Server down ({resp.status_code}), retrying...")
                else:
                    logger.warning(f"  Unexpected: {resp.text[:150]}")
            except Exception as e:
                logger.error(f"  Attempt {attempt + 1} error: {e}")

        # ─── Provider 3: Together AI ──────────────────────────────────────
        together_key = os.getenv("TOGETHER_API_KEY")
        if together_key:
            logger.info("🔄 Trying Together AI (FLUX free)...")
            try:
                resp = requests.post(
                    "https://api.together.xyz/v1/images/generations",
                    headers={
                        "Authorization": f"Bearer {together_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "black-forest-labs/FLUX.1-schnell-Free",
                        "prompt": final_prompt,
                        "width": 1024,
                        "height": 1024,
                        "steps": 4,
                        "n": 1,
                        "response_format": "b64_json"
                    },
                    timeout=60
                )
                if resp.status_code == 200:
                    img_b64 = resp.json()["data"][0]["b64_json"]
                    logger.success("✅ Together AI success!")
                    return base64.b64decode(img_b64)
                logger.warning(f"⚠️ Together: {resp.status_code} - {resp.text[:150]}")
            except Exception as e:
                logger.warning(f"⚠️ Together failed: {e}")
        else:
            logger.warning("⚠️ TOGETHER_API_KEY not set — skipping Together AI")

        # ─── Provider 4: Fal.ai ───────────────────────────────────────────
        fal_key = os.getenv("FAL_API_KEY")
        if fal_key:
            logger.info("🔄 Trying Fal.ai (FLUX)...")
            try:
                resp = requests.post(
                    "https://fal.run/fal-ai/flux/schnell",
                    headers={
                        "Authorization": f"Key {fal_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": final_prompt,
                        "image_size": "square_hd",
                        "num_images": 1
                    },
                    timeout=60
                )
                if resp.status_code == 200:
                    img_url = resp.json()["images"][0]["url"]
                    img_resp = requests.get(img_url, timeout=30)
                    if img_resp.status_code == 200:
                        logger.success("✅ Fal.ai success!")
                        return img_resp.content
                logger.warning(f"⚠️ Fal: {resp.status_code} - {resp.text[:150]}")
            except Exception as e:
                logger.warning(f"⚠️ Fal failed: {e}")
        else:
            logger.warning("⚠️ FAL_API_KEY not set — skipping Fal.ai")

        logger.error("❌ All image providers failed.")
        return None

    def justify_visual(self, title, img_data):
        """Groq vision দিয়ে ছবি যাচাই — সম্পূর্ণ ফ্রি, উচ্চ কোটা"""

        vision_models = [
            "meta-llama/llama-4-scout-17b-16e-instruct",  # সর্বোচ্চ কোটা
            "llama-3.2-90b-vision-preview",               # ব্যাকআপ
            "llama-3.2-11b-vision-preview",               # হালকা ব্যাকআপ
        ]

        img_b64 = base64.standard_b64encode(img_data).decode("utf-8")

        judge_prompt = (
            f"News Title: '{title}'\n\n"
            "Task: You are an image auditor. The image is a symbolic/metaphorical "
            "representation of the news title. If the image is professional, high-quality, "
            "and captures the MOOD or THEME (even symbolically), reply 'PASS'. "
            "Only reply 'FAIL' if the image is broken, blank, or completely unrelated. "
            "Answer ONLY with PASS or FAIL — nothing else."
        )

        for model in vision_models:
            try:
                logger.info(f"⚖️ Justifying with Groq vision ({model})...")
                response = self.prompt_engine.client.chat.completions.create(
                    model=model,
                    messages=[{
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": judge_prompt
                            }
                        ]
                    }],
                    max_tokens=10,
                    temperature=0.1
                )
                result = response.choices[0].message.content.strip().upper()
                verdict = "PASS" if "PASS" in result else "FAIL"
                logger.success(f"✅ Groq vision verdict: {verdict} (raw: {result[:40]})")
                return verdict

            except Exception as e:
                err = str(e)
                if "429" in err:
                    logger.warning(f"⏳ {model} rate limited — trying next...")
                elif "404" in err or "not found" in err.lower():
                    logger.warning(f"⚠️ {model} unavailable — trying next...")
                else:
                    logger.warning(f"⚠️ {model} error: {err[:120]}")

        logger.warning("⚠️ All vision models failed — defaulting to PASS")
        return "PASS"

    def generate_and_update(self):
        # ধাপ ১: ডাটাবেস থেকে 'ready' নিউজগুলো আনুন
        # নোট: fetch_ready_for_images ব্যবহার করা উচিত যদি আপনি content তৈরি হওয়ার পরের নিউজ চান
        news_list = self.db.fetch_ready_for_images() 

        if not news_list:
            logger.info("ℹ️ No 'ready' news found for image generation.")
            return

        for news in news_list:
            unique_id = news['unique_id']
            category = news['news_category']
            context = news['main_context']

            logger.info(f"🚀 Processing ID: {unique_id} | Category: {category}")

            # ধাপ ২: ইমেজ প্রম্পট তৈরি
            safe_prompt = self.prompt_engine.generate_safe_prompt(category, context)
            
            if safe_prompt:
                # ✅ সংশোধন: self.final_sanitize ব্যবহার করুন (self.prompt_engine নয়)
                sanitized_prompt = self.final_sanitize(safe_prompt)
                
                # ধাপ ৩: ইমেজ জেনারেট করা
                image_bytes = self.generate_image_binary(sanitized_prompt)

                if image_bytes:
                    # ধাপ ৪: স্টোরেজে আপলোড
                    file_name = f"final_images/{unique_id}.jpg"
                    public_url = self.db.upload_to_storage(file_name, image_bytes)

                    if public_url:
                        # ধাপ ৫: ডাটাবেসে URL এবং Prompt আপডেট করা
                        # নিশ্চিত করুন আপনার DBHandler এ এই ফাংশনটি আছে
                        self.db.update_final_image(unique_id, public_url) 
                        logger.success(f"🎉 Fully Processed: {unique_id}")
                    else:
                        logger.error(f"❌ Storage upload failed for {unique_id}")
                else:
                    logger.error(f"❌ Image binary generation failed for {unique_id}")