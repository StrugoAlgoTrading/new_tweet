# Dockerfile להרצת Truth Social Monitor עם Playwright ו-Xvfb (GUI וירטואלי)
FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

# התקנת תלות להרצת דפדפן במצב headless=False
RUN apt-get update && apt-get install -y xvfb

# הגדרת סביבת עבודה
WORKDIR /app

# העתקת קבצים
COPY requirements.txt requirements.txt
COPY monitor.py monitor.py
COPY refresh_cookies.py refresh_cookies.py

# התקנת תלויות
RUN pip install --no-cache-dir -r requirements.txt

# התקנת דפדפנים של Playwright
RUN playwright install --with-deps

# הפקודה שתופעל כשמריצים את הקונטיינר (כולל הרצת monitor עם קוקיז מתוקנים)
CMD xvfb-run --auto-servernum --server-args='-screen 0 1280x720x24' python3 monitor.py
