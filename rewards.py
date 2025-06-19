import os
import time
import random
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDGE_DRIVER_PATH = os.path.join(BASE_DIR, "msedgedriver")  # Linux WebDriver
EDGE_AUTOMATION_PROFILE_PATH = os.path.join(BASE_DIR, "EdgeProfile")

BOT_TOKEN = ""  # Fill this in
USER_ID = ""    # Fill this in

MESSAGE_OK = "✅ Microsoft Rewards completed successfully."
MESSAGE_ERR = "❌ Microsoft Rewards script ran with some issues:\n{}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": USER_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"[!] Failed to send Telegram message: {e}")

def wait_random(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def main():
    errors = []

    # Optional: Lower CPU priority (Linux only)
    try:
        os.nice(10)
    except Exception as e:
        print(f"[!] Could not lower process priority: {e}")

    # Edge options
    options = Options()
    options.add_argument(f"user-data-dir={EDGE_AUTOMATION_PROFILE_PATH}")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless=new")
    options.page_load_strategy = "eager"  # Faster, but might need occasional .wait

    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    driver.set_page_load_timeout(180)  # Set 3-minute timeout for slow machines

    print("[*] Launching Microsoft Rewards...")
    driver.get("https://rewards.bing.com/")

    WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ds-card-sec.ng-scope"))
    )
    wait_random(6.5, 12.5)

    original_window = driver.current_window_handle
    today = datetime.datetime.today().strftime('%A')
    allowed_days = ['Friday', 'Sunday', 'Wednesday']
    skip_indices = [3, 4, 5]

    cards = driver.find_elements(By.CSS_SELECTOR, "a.ds-card-sec.ng-scope")
    if not cards:
        error_msg = "No reward cards found on initial load."
        print(f"[!] {error_msg}")
        errors.append(error_msg)
        driver.quit()
        return errors

    print(f"[+] Found {len(cards)} reward cards")

    for i, card in enumerate(cards):
        if i in skip_indices:
            print(f"[-] Skipping card {i+1} (inactive)")
            continue
        if i > 2 and today not in allowed_days:
            print(f"[-] Skipping card {i+1} (not allowed on {today})")
            continue

        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            wait_random(0.3, 0.8)

            windows_before = driver.window_handles
            driver.execute_script("arguments[0].click();", card)
            print(f"[+] Clicked card {i+1}/{len(cards)}")
            wait_random(2.0, 4.0)

            windows_after = driver.window_handles
            if len(windows_after) > len(windows_before):
                new_window = [w for w in windows_after if w not in windows_before][0]
                driver.switch_to.window(new_window)
                print("[*] Switched to new tab")
                wait_random(4.0, 7.0)
                driver.close()
                driver.switch_to.window(original_window)
                print("[*] Closed new tab and returned")
            else:
                driver.back()
                print("[*] Used back button to return to main page")

            wait_random(1.5, 3.2)

        except Exception as e:
            error_msg = f"Card {i+1}: {e}"
            print(f"[!] {error_msg}")
            errors.append(error_msg)

    print("[✓] Finished clicking all reward cards.")
    driver.quit()
    return errors

if __name__ == "__main__":
    try:
        errors = main()
        if not errors:
            send_telegram_message(MESSAGE_OK)
        else:
            error_text = "\n".join(errors)
            send_telegram_message(MESSAGE_ERR.format(error_text))
    except Exception as e:
        send_telegram_message(MESSAGE_ERR.format(f"Fatal error: {e}"))
