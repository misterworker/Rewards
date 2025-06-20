import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Configuration ===
EDGE_DRIVER_PATH = "/home/username/selenium_bot/msedgedriver"
EDGE_PROFILE_PATH = "/home/username/selenium_bot/EdgeProfile"
# EDGE_DRIVER_PATH = r"C:\Users\ethan\Downloads\edgedriver_win64\msedgedriver.exe"
# EDGE_PROFILE_PATH = r"C:\Users\ethan\Documents\General\Automation\Rewards\EdgeProfile"
EMAIL = "" # Fill this in

# === Set up Edge Options ===
options = Options()
options.add_argument(f"user-data-dir={EDGE_PROFILE_PATH}")
# options.add_argument("--headless=new")  # Headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# === Start Driver ===
service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    print("[*] Opening login page...")
    driver.get("https://login.live.com/")
    time.sleep(2)

    # === Step 1: Enter Email ===
    email_input = wait.until(EC.presence_of_element_located((By.ID, "usernameEntry")))
    email_input.clear()
    email_input.send_keys(EMAIL)
    print("[+] Email entered")

    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']")))
    next_btn.click()
    print("[+] Next button clicked")

    # === Step 2: Wait for Send Code button ===
    wait.until(EC.staleness_of(next_btn))  # Wait until the previous button is stale
    send_code_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']")))
    send_code_btn.click()
    print("[+] Send code clicked")

    # === Step 3: Enter 6-digit Code ===
    wait.until(EC.presence_of_element_located((By.ID, "codeEntry-0")))
    code = input("[?] Enter the 6-digit code: ").strip()

    if len(code) != 6 or not code.isdigit():
        raise ValueError("Invalid code. Must be 6 digits.")

    for i, digit in enumerate(code):
        field = wait.until(EC.presence_of_element_located((By.ID, f"codeEntry-{i}")))
        field.clear()
        field.send_keys(digit)
    print("[✓] Code entered")

    # === Step 4: Final Code Submit Button ===
    code_submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']")))
    code_submit_btn.click()
    print("[+] Code confirmation submitted")

    # === Step 5: Final "Yes" Button ===
    wait.until(EC.staleness_of(code_submit_btn))
    yes_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton']")))
    yes_btn.click()
    print("[+] 'Yes' button clicked — Login should be complete.")

except Exception as e:
    print(f"[!] Error: {e}")

finally:
    driver.quit()
