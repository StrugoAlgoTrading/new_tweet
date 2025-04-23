import asyncio
from playwright.async_api import async_playwright
import json

USERNAME = "benstrugo"
PASSWORD = "Benmaya15"
LOGIN_URL = "https://truthsocial.com/login"

async def save_cookies_auto():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("🚀 טוען את דף ההתחברות...")
        await page.goto(LOGIN_URL)

        # ממלא את הטופס
        await page.click("text=Sign In")
        await page.fill('input[name="username"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[type="submit"]')
        cookies = await context.cookies()
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)
        await browser.close()
        print("🍪 קוקיז נשמרו ל־cookies.json")
        await browser.close()
