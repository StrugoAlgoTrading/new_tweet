import requests
from playwright.sync_api import sync_playwright
from src.config.setting import SECRETS


class TruthHandler:
    def __init__(self, cookies_file: str):
        self.cookies_file = cookies_file

    def fetch_post_id(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=self.cookies_file)
            page = context.new_page()
            page.goto("https://truthsocial.com/@realDonaldTrump", wait_until="domcontentloaded")
            posts = page.evaluate(
                f"""
                async () => {{
                    const res = await fetch("{SECRETS.TRUMP_URL}", {{
                        method: "GET",
                        headers: {{
                            "accept": "application/json, text/plain, */*"
                        }}
                    }});
                    return await res.json();
                }}
                """
            )
            return posts[0]["id"], posts[0]['created_at']

    def notify_new_post(self, tweet_time):
        try:
            response = requests.post(SECRETS.PUSH_URL, json={"event_type": "Trump Tweet", "ticker": "tqqq", "time": tweet_time})
            print(response.status_code)
        except Exception as e:
            print("❌ שגיאה בשליחה ל-API:", e)