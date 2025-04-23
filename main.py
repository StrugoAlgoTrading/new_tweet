import json
import time
import requests
from playwright.sync_api import sync_playwright
from new_cookies import save_cookies_auto
import asyncio

COOKIES_FILE = "cookies.json"
LAST_ID_FILE = "last_post_id.txt"
API_URL_TO_SEND = "https://truthsocial.com/api/v1/accounts/107780257626128497/statuses?exclude_replies=true&only_replies=false&with_muted=true"


def load_cookies():
    with open(COOKIES_FILE, "r") as f:
        return json.load(f)

def save_last_post_id(post_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(post_id)

def load_last_post_id():
    try:
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def fetch_post_id():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=COOKIES_FILE)
        page = context.new_page()

        page.goto("https://truthsocial.com/@realDonaldTrump", wait_until="domcontentloaded")

        posts = page.evaluate(
            f"""
            async () => {{
                const res = await fetch("{API_URL_TO_SEND}", {{
                    method: "GET",
                    headers: {{
                        "accept": "application/json, text/plain, */*"
                    }}
                }});
                return await res.json();
            }}
            """
        )
        return posts[0]["id"]

def notify_new_post(post_id):
    try:
        response = requests.post(API_URL_TO_SEND, json={"post_id": post_id})
        print(f"📤 נשלח ל-API, קוד תגובה: {response.status_code}")
    except Exception as e:
        print("❌ שגיאה בשליחה ל-API:", e)

def run_monitor():
    print("🚀 מתחיל מעקב אחרי פוסטים חדשים...")
    last_id = load_last_post_id()

    while True:
        try:
            current_id = fetch_post_id()
            if current_id != last_id:
                print("🔥 פוסט חדש! ID:", current_id)
                # notify_new_post(current_id)
                save_last_post_id(current_id)
                last_id = current_id
            else:
                print("✅ אין פוסט חדש")
        except Exception as e:
            print("❌ שגיאה:", e)
            asyncio.run(save_cookies_auto())

        time.sleep(1)

if __name__ == "__main__":
    run_monitor()
