# Microsoft Rewards Automation Script

This Python script automates the process of clicking Microsoft Rewards cards using the Edge browser and Selenium.

## 🎯 What It Does

- Launches Microsoft Edge with your user profile
- Navigates to [https://rewards.bing.com/](https://rewards.bing.com/)
- Identifies clickable reward cards
- Clicks through eligible cards, opens them in a new tab if needed, waits briefly, and then returns

## 🧠 Logic & Rules

1. **Always Click First 3 Cards**
   - Cards 1, 2, and 3 are always clicked regardless of the day.

2. **Skip Inactive Cards**
   - Cards 4, 5, and 6 (indices 3, 4, 5) are skipped entirely — they're known to be inactive.

3. **Day-Based Logic for Remaining Cards**
   - Cards beyond the first 3 are only clicked on:
     - **Wednesday**
     - **Friday**
     - **Sunday**

4. **Tab Handling**
   - If a card opens in a new tab, the script switches to it, waits a few seconds, then closes the tab and returns.
   - If no new tab opens, it uses the browser’s back button.

5. **Natural Behavior**
   - Wait times are randomized to simulate human interaction.

## ⚙️ Requirements

- Python 3
- Microsoft Edge installed
- Microsoft Edge WebDriver downloaded
- Selenium installed (`pip install selenium`)

## 📁 Paths to Update

Update the following variables in the script with the correct paths on your system:

```python
EDGE_DRIVER_PATH = r"C:\path\to\msedgedriver.exe"
EDGE_AUTOMATION_PROFILE_PATH = r"C:\path\to\EdgeProfile"
```

## Deploy
Use Google Cloud Compute Engine, e2 micro 30GB standard disk for free usage. This is a headless VM, so you'll have to uncomment the headless option if needed. Install all dependencies, run automate_login with your email and one time passcode, then set up a cron job for rewards.py to be executed daily.

```bash
curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip
unzip ngrok.zip
sudo mv ngrok /usr/local/bin/

ngrok config add-authtoken <YOUR_AUTH_TOKEN>

nohup ngrok http 8000 > ngrok.log 2>&1 & # Get the link from the log file
```
