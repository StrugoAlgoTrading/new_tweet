from playwright.async_api import async_playwright
import json
from .config.setting import SECRETS


class FileManager:
    def __init__(self, last_id_file: str):
        self.last_id_file = last_id_file

    def save_last_post_id(self, post_id):
        with open(self.last_id_file, "w") as f:
            f.write(post_id)

    def load_last_post_id(self):
        try:
            with open(self.last_id_file, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    async def save_cookies_auto(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            print("🚀 טוען את דף ההתחברות...")
            await page.goto(SECRETS.LOGIN_URL)
            await page.click("text=Sign In")
            await page.fill('input[name="username"]', SECRETS.USERNAME)
            await page.fill('input[name="password"]', SECRETS.PASSWORD)
            await page.click('button[type="submit"]')
            cookies = await context.cookies()
            with open("../cookies.json", "w") as f:
                json.dump(cookies, f, indent=2)
            await browser.close()
            print("🍪 קוקיז נשמרו ל־cookies.json")
            await browser.close()