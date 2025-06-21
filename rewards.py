import os
import time
import random
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDGE_DRIVER_PATH = os.path.join(BASE_DIR, "msedgedriver")  # Ensure this is executable
EDGE_AUTOMATION_PROFILE_PATH = os.path.join(BASE_DIR, "EdgeProfile")


BOT_TOKEN = ""  # Fill in your bot token
USER_ID = ""    # Fill in your user ID

MESSAGE_OK = "✅ Microsoft Rewards completed successfully."
MESSAGE_ERR = "❌ Microsoft Rewards script ran with some issues:\n{}"

def send_telegram_message(text, user_id=USER_ID, bot_token=BOT_TOKEN):
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": user_id, "text": text}
        )
    except Exception as e:
        print(f"[!] Failed to send Telegram message: {e}")

def wait_random(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def main():
    errors = []

    # Lower process priority to reduce CPU pressure
    try:
        os.nice(10)
    except Exception as e:
        print(f"[!] Failed to set lower priority: {e}")

    # Edge options
    options = Options()
    options.add_argument(f"user-data-dir={EDGE_AUTOMATION_PROFILE_PATH}")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--headless=new")
    options.add_argument("--single-process")
    options.page_load_strategy = "eager"

    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    driver.set_page_load_timeout(180)

    try:
        print("[*] Opening rewards page...")
        driver.get("https://rewards.bing.com/")
        wait_random(8, 12)

        cards = driver.find_elements(By.CSS_SELECTOR, "a.ds-card-sec.ng-scope")
        if not cards:
            error = "No reward cards found on load."
            print(f"[!] {error}")
            errors.append(error)
            driver.quit()
            return errors

        print(f"[+] Found {len(cards)} reward cards.")
        original_window = driver.current_window_handle
        today = datetime.datetime.today().strftime('%A')
        allowed_days = ['Friday', 'Sunday', 'Wednesday']
        skip_indices = [3, 4, 5]

        for i, card in enumerate(cards):
            if i in skip_indices:
                print(f"[-] Skipping card {i+1} (inactive)")
                continue
            if i > 2 and today not in allowed_days:
                print(f"[-] Skipping card {i+1} (not allowed on {today})")
                continue

            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", card)
                wait_random(0.5, 1.2)
                driver.execute_script("arguments[0].click();", card)
                print(f"[+] Clicked card {i+1}/{len(cards)}")

                wait_random(4, 6)

                # Check if new tab opened
                windows = driver.window_handles
                if len(windows) > 1:
                    driver.switch_to.window(windows[-1])
                    print("[*] Switched to new tab")
                    wait_random(5, 8)
                    driver.close()
                    driver.switch_to.window(original_window)
                    print("[*] Closed tab and returned")
                else:
                    driver.back()
                    print("[*] Navigated back to rewards page")

                wait_random(2.5, 4.0)

            except Exception as e:
                err = f"Card {i+1} failed: {str(e)}"
                print(f"[!] {err}")
                errors.append(err)

    finally:
        driver.quit()
        print("[✓] Session ended.")

    return errors

if __name__ == "__main__":
    try:
        result = main()
        if result:
            send_telegram_message(MESSAGE_ERR.format("\n".join(result)))
        else:
            send_telegram_message(MESSAGE_OK)
    except Exception as fatal:
        send_telegram_message(MESSAGE_ERR.format(f"Fatal error: {fatal}"))
