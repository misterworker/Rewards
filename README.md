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

# Ubuntu Setup and Rewards Bot Installation Guide

```bash
# Update and upgrade system packages
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y wget curl unzip git software-properties-common

# Install Python3, pip, and venv
sudo apt install -y python3 python3-pip python3-venv

# Add Microsoft Edge repository and key
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main"
sudo apt update

# Install Microsoft Edge
sudo apt install -y microsoft-edge-stable

# Get installed Edge version
EDGE_VERSION=$(microsoft-edge-stable --version | grep -oP '[0-9.]+')

# Download matching Edge WebDriver
wget "https://msedgedriver.azureedge.net/${EDGE_VERSION}/edgedriver_linux64.zip" -O msedgedriver.zip

# Unzip and move WebDriver
unzip msedgedriver.zip
chmod +x msedgedriver
sudo mv msedgedriver /usr/local/bin/

# Clone your Rewards repository
git clone https://github.com/misterworker/Rewards.git
cd Rewards

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Setup cron jobs
```bash
sudo apt update
sudo apt install cron

sudo service cron start

crontab -e
0 1 * * * /home/username/Rewards/venv/bin/python /home/username/Rewards/rewards.py # Paste at bottom of file
```
