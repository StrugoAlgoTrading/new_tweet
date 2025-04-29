import time
import asyncio
from src.files_manager import FileManager
from src.config.setting import CONFIG
from src.truth_social import TruthHandler

def main():
    file_manager = FileManager(CONFIG.LAST_ID_FILE)
    last_id = file_manager.load_last_post_id()
    while True:
        try:
            truth_social = TruthHandler(CONFIG.COOKIES_FILE)
            current_id, tweet_time = truth_social.fetch_post_id()
            if current_id != last_id:
                print("🔥 פוסט חדש! ID:", current_id)
                truth_social.notify_new_post(tweet_time)
                file_manager.save_last_post_id(current_id)
                last_id = current_id
            else:
                print("🔥 פוסט ישן! ID:", current_id)
                truth_social.notify_new_post(tweet_time)
        except:
            asyncio.run(file_manager.save_cookies_auto())
        time.sleep(1)


if __name__ == "__main__":
    main()
