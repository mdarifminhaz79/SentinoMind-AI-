import requests

# আপনার URL এবং টোকেন
url = "https://graph.facebook.com/v22.0/936731689303838"
params = {
    "access_token": "EAANT89eXPx4BRF1wOiS9Lyugqdd0YYa99l6QXY9GNtEqGb8EYZAFjYZBjnOg2QSbx0U6bIHWlXc6gTyCrdVdLTIVSgb34dPY4DooZBBsYAd04S7FkUo6vpKhRcaOEObLATGImI5p8k72gsZBRAFhDISK6MZBZCqfZAOZC1bbELDH9fQZCBdlKCA8CfVXX2V3BZBxdGP8hDd6mSFr3AnQgxtCSGKyTwarj8xa57Sc7ekZBtMaeThippvw8ZCxCPEHUDVrOPfQfBZAbNG01tv04yYBTZABZCPQ2YcLQZDZD", # এখানে আপনার টোকেনটি দিন
    "fields": "name" # শুধুমাত্র নাম চাইলে এটি স্পেসিফাই করা ভালো
}

response = requests.get(url, params=params)
fb_data = response.json() # রেসপন্সটিকে JSON ডিকশনারিতে কনভার্ট করা

# চেক করা যে এরর আছে কি না
if "name" in fb_data:
    page_name = fb_data['name']
    print(f"Page Name: {page_name}")
else:
    print("Error:", fb_data.get("error", {}).get("message", "Unknown error"))
# import os
# import time
# import requests
# import urllib.parse
# import random
# import re
# from io import BytesIO
# from google import genai
# from google.genai import types
# from groq import Groq
# from loguru import logger
# from dotenv import load_dotenv

# load_dotenv()

# # ============================================================
# # CLASS 1: PromptGenerator — শুধু Groq দিয়ে প্রম্পট বানায়
# # ============================================================
# class PromptGenerator:
#     def __init__(self):
#         logger.info("Initializing PromptGenerator with Llama-3.3-70b...")
#         self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#         self.model_name = "llama-3.3-70b-versatile"

#     def _call_groq(self, system_prompt, user_prompt, temperature=0.7):
#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model_name,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 temperature=temperature,
#                 max_tokens=300
#             )
#             return response.choices[0].message.content
#         except Exception as e:
#             logger.error(f"❌ Groq API Error: {e}")
#             return None

#     def generate_safe_prompt(self, category, context):
#         logger.info(f"🔍 Starting prompt generation for category: {category}")

#         # Step 1: Architect — প্রম্পট তৈরি
#         sys_p = "You are an expert Visual Prompt Engineer. Convert news into a safe metaphorical image prompt. Avoid violence, blood, or graphic content. Use symbolism."
#         usr_p = f"Category: {category}\nContext: {context}\nCreate a cinematic AI image prompt starting with 'A professional...'"
#         prompt = self._call_groq(sys_p, usr_p, temperature=0.8)
#         if not prompt:
#             return None

#         # Step 2 & 3: Audit & Refine Loop
#         for attempt in range(3):
#             logger.info(f"🛡️ Auditing prompt (Attempt {attempt + 1}/3)...")
#             audit_sys = "You are an AI Safety Auditor. Check for violence, blood, or graphic content. If safe, respond 'STATUS: OK'. If unsafe, respond 'STATUS: REJECTED | FEEDBACK: reason'."
#             audit_res = self._call_groq(audit_sys, f"Audit this: {prompt}", temperature=0.1)

#             if audit_res and "STATUS: OK" in audit_res:
#                 logger.success(f"✅ Prompt approved on attempt {attempt + 1}.")
#                 return prompt

#             feedback = audit_res.replace("STATUS: REJECTED", "") if audit_res else "Avoid literal violence."
#             refine_sys = "You are a prompt refinement expert. Rewrite the prompt to replace violent elements with neutral metaphors while keeping the news mood."
#             prompt = self._call_groq(refine_sys, f"Original: {prompt}\nFeedback: {feedback}", temperature=0.6)

#         logger.error("❌ Prompt failed safety audit after 3 attempts.")
#         return None


# # ============================================================
# # CLASS 2: ImageGenerator — প্রম্পট নিয়ে ছবি বানায়
# # ============================================================
# class ImageGenerator:
#     def __init__(self):
#         self.prompt_engine = PromptGenerator()
#         self.gemini = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
#         self.hf_key = os.getenv("HUGGINGFACE_API_KEY")

#     def final_sanitize(self, text):
#         """রাজনৈতিক ও সংবেদনশীল শব্দ সরিয়ে ফেলা"""
#         replacements = {
#             "Trump": "world leader", "Biden": "politician", "Elon": "tech CEO",
#             "war": "conflict", "blood": "red ink", "kill": "neutralize",
#             "murder": "tragedy", "Claude": "AI system", "Pentagon": "government agency",
#             "Iran": "foreign nation", "Tehran": "capital city",
#         }
#         for word, rep in replacements.items():
#             text = re.sub(f"\\b{word}\\b", rep, text, flags=re.IGNORECASE)
#         return re.sub(r'\s+', ' ', text).strip()[:500]

#     def generate_image_binary(self, prompt):
#         from huggingface_hub import InferenceClient

#         # প্রম্পট ক্লিন + ব্লকড শব্দ ফিল্টার
#         short_p = " ".join(prompt.split()[:20])
#         clean_p = re.sub(r'[^\w\s,]', '', short_p).strip()
#         blocked = {"claude", "military", "iran", "pentagon", "banned",
#                    "tehran", "weapon", "war", "attack", "bomb", "government"}
#         filtered_p = " ".join([w for w in clean_p.split() if w.lower() not in blocked])
#         logger.info(f"🎨 Filtered prompt: {filtered_p}")

#         # ─── Provider 1: HuggingFace InferenceClient (SDK) ───────────────
#         try:
#             logger.info("🚀 Trying HuggingFace InferenceClient...")
#             hf_client = InferenceClient(
#                 provider="auto",          # fal-ai / replicate / nebius — HF বেছে নেবে
#                 api_key=self.hf_key,
#             )
#             pil_image = hf_client.text_to_image(
#                 prompt=filtered_p,
#                 model="black-forest-labs/FLUX.1-schnell",
#             )
#             buf = BytesIO()
#             pil_image.save(buf, format="JPEG")
#             logger.success("✅ HuggingFace success!")
#             return buf.getvalue()
#         except Exception as e:
#             logger.warning(f"⚠️ HF failed: {e}")

#         # ─── Provider 2: Pollinations ─────────────────────────────────────
#         logger.info("🔄 Trying Pollinations...")
#         seed = random.randint(1, 999999)
#         encoded_p = urllib.parse.quote(filtered_p[:250])
#         pol_url = (f"https://image.pollinations.ai/prompt/{encoded_p}"
#                    f"?model=flux-schnell&width=1024&height=1024&seed={seed}&nologo=true")
#         pol_headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
#             "Accept": "image/*",
#             "Referer": "https://pollinations.ai/"
#         }
#         for attempt in range(3):
#             wait = (attempt + 1) * 8   # 8s → 16s → 24s backoff
#             logger.info(f"  Pollinations attempt {attempt+1}/3 (waiting {wait}s)...")
#             time.sleep(wait)
#             try:
#                 resp = requests.get(pol_url, headers=pol_headers, timeout=120)
#                 ct = resp.headers.get("Content-Type", "")
#                 logger.debug(f"  {resp.status_code} | {ct} | {len(resp.content)} bytes")
#                 if resp.status_code == 200 and "image" in ct and len(resp.content) > 10000:
#                     logger.success("✅ Pollinations success!")
#                     return resp.content
#                 if resp.status_code in (502, 503, 504):
#                     logger.warning(f"  Server down ({resp.status_code}), retrying...")
#                 else:
#                     logger.warning(f"  Unexpected: {resp.text[:150]}")
#             except Exception as e:
#                 logger.error(f"  Attempt {attempt+1} error: {e}")

#         # ─── Provider 3: Together AI — FLUX.1-schnell Free ───────────────
#         together_key = os.getenv("TOGETHER_API_KEY")
#         if together_key:
#             logger.info("🔄 Trying Together AI (FLUX free)...")
#             try:
#                 import base64
#                 resp = requests.post(
#                     "https://api.together.xyz/v1/images/generations",
#                     headers={"Authorization": f"Bearer {together_key}",
#                              "Content-Type": "application/json"},
#                     json={
#                         "model": "black-forest-labs/FLUX.1-schnell-Free",
#                         "prompt": filtered_p,
#                         "width": 1024, "height": 1024,
#                         "steps": 4, "n": 1,
#                         "response_format": "b64_json"
#                     },
#                     timeout=60
#                 )
#                 if resp.status_code == 200:
#                     img_b64 = resp.json()["data"][0]["b64_json"]
#                     logger.success("✅ Together AI success!")
#                     return base64.b64decode(img_b64)
#                 logger.warning(f"⚠️ Together: {resp.status_code} - {resp.text[:150]}")
#             except Exception as e:
#                 logger.warning(f"⚠️ Together failed: {e}")
#         else:
#             logger.warning("⚠️ TOGETHER_API_KEY not set — skipping Together AI")

#         # ─── Provider 4: Fal.ai ───────────────────────────────────────────
#         fal_key = os.getenv("FAL_API_KEY")
#         if fal_key:
#             logger.info("🔄 Trying Fal.ai (FLUX)...")
#             try:
#                 resp = requests.post(
#                     "https://fal.run/fal-ai/flux/schnell",
#                     headers={"Authorization": f"Key {fal_key}",
#                              "Content-Type": "application/json"},
#                     json={"prompt": filtered_p, "image_size": "square_hd", "num_images": 1},
#                     timeout=60
#                 )
#                 if resp.status_code == 200:
#                     img_url = resp.json()["images"][0]["url"]
#                     img_resp = requests.get(img_url, timeout=30)
#                     if img_resp.status_code == 200:
#                         logger.success("✅ Fal.ai success!")
#                         return img_resp.content
#                 logger.warning(f"⚠️ Fal: {resp.status_code} - {resp.text[:150]}")
#             except Exception as e:
#                 logger.warning(f"⚠️ Fal failed: {e}")
#         else:
#             logger.warning("⚠️ FAL_API_KEY not set — skipping Fal.ai")

#         logger.error("❌ All image providers failed.")
#         return None

#     def justify_visual(self, title, img_data):
#         """Groq vision দিয়ে ছবি যাচাই — Gemini এর বিকল্প, সম্পূর্ণ ফ্রি"""
#         import base64

#         # Groq vision models (ফ্রি টায়ার, উচ্চ কোটা)
#         vision_models = [
#             "meta-llama/llama-4-scout-17b-16e-instruct",  # সর্বোচ্চ কোটা
#             "llama-3.2-90b-vision-preview",               # ব্যাকআপ
#             "llama-3.2-11b-vision-preview",               # হালকা ব্যাকআপ
#         ]

#         img_b64 = base64.standard_b64encode(img_data).decode("utf-8")

#         for model in vision_models:
#             try:
#                 logger.info(f"⚖️ Justifying with Groq vision ({model})...")
#                 judge_prompt = (
#                     f"News Title: '{title}'\n\n"
#                     "Task: You are an image auditor. The provided image is a symbolic/metaphorical "
#                     "representation of the news title above. If the image is professional, high-quality, "
#                     "and captures the MOOD or THEME of the news (even if symbolic), reply with 'PASS'. "
#                     "Only reply 'FAIL' if the image is broken, blank, or completely unrelated. "
#                     "Answer ONLY with 'PASS' or 'FAIL'."
#                 )
#                 response = self.prompt_engine.client.chat.completions.create(
#                     model=model,
#                     messages=[{
#                         "role": "user",
#                         "content": [
#                             {
#                                 "type": "image_url",
#                                 "image_url": {
#                                     "url": f"data:image/jpeg;base64,{img_b64}"
#                                 }
#                             },
#                             {
#                                 "type": "text",
#                                 "text": judge_prompt
#                             }
#                         ]
#                     }],
#                     max_tokens=50,
#                     temperature=0.1
#                 )
#                 result = response.choices[0].message.content.strip().upper()
#                 verdict = "PASS" if "PASS" in result else "FAIL"
#                 logger.success(f"✅ Groq vision verdict: {result[:80]}")
#                 return verdict

#             except Exception as e:
#                 err = str(e)
#                 if "429" in err:
#                     logger.warning(f"⏳ {model} rate limited, trying next...")
#                 elif "404" in err or "not found" in err.lower():
#                     logger.warning(f"⚠️ {model} unavailable, trying next...")
#                 else:
#                     logger.warning(f"⚠️ {model} error: {err[:100]}")

#         logger.warning("⚠️ All vision models failed — defaulting to PASS")
#         return "PASS"


# # ============================================================
# # MAIN TEST
# # ============================================================
# if __name__ == "__main__":
#     test_category = "World News"
#     test_context = (
#         "The cancel culture is about to get CANCELED 😂! Marlon Wayans is back with a new Scary Movie and he's not playing nice! 🎥 Get ready for a horror comedy extravaganza that takes aim at EVERYTHING from Scream to M3GAN 🤣. The first trailer is OUT NOW and it's a REBOOT LIKE NO OTHER "
#     )

#     engine = ImageGenerator()

#     print("\n--- STEP 1: PROMPT GENERATION ---")
#     safe_visual_prompt = engine.prompt_engine.generate_safe_prompt(test_category, test_context)

#     if safe_visual_prompt:
#         print(f"\n✨ Generated Prompt:\n{safe_visual_prompt}")

#         clean_p = engine.final_sanitize(safe_visual_prompt)
#         print(f"\n🧹 Sanitized Prompt:\n{clean_p}")

#         print("\n--- STEP 2: IMAGE GENERATION ---")
#         image_bytes = engine.generate_image_binary(clean_p)

#         if image_bytes:
#             with open("test_output.jpg", "wb") as f:
#                 f.write(image_bytes)
#             print("\n✅ Success! Image saved as 'test_output.jpg'")

#             verdict = engine.justify_visual(test_context, image_bytes)
#             print(f"⚖️ Gemini Justification: {verdict}")
#         else:
#             print("\n❌ Image generation failed.")
#     else:
#         print("\n❌ Safe prompt generation failed after 3 attempts.")