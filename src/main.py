import os
import shutil
from pathlib import Path
import requests
import time
import sys
import winsound  # For Windows beep; fallback provided below if needed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --------------------------------------------------
# Clear the 'data' folder in the project root
# --------------------------------------------------
def clear_data_folder():
    # Assuming this file is in project_root/src, the project root is one level up.
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    data_folder = project_root / "data"
    print(f"Clearing data folder: {data_folder}")

    if data_folder.exists() and data_folder.is_dir():
        shutil.rmtree(data_folder)  # Remove the folder and its contents.
    # Recreate the folder
    data_folder.mkdir(exist_ok=True)
    print("Data folder cleared.")

clear_data_folder()

# --------------------------------------------------
# Start AdsPower Browser Session
# --------------------------------------------------
ads_id = "ktunx7f"  # Your AdsPower profile ID

open_url = f"http://local.adspower.com:50325/api/v1/browser/start?user_id={ads_id}"
close_url = f"http://local.adspower.com:50325/api/v1/browser/stop?user_id={ads_id}"

resp = requests.get(open_url).json()
if resp["code"] != 0:
    print("Failed to start AdsPower browser:", resp["msg"])
    sys.exit()

chrome_driver_path = resp["data"]["webdriver"]
debugger_address   = resp["data"]["ws"]["selenium"]

service = Service(executable_path=chrome_driver_path)
options = Options()
options.add_argument("--start-maximized")  # Ensure window is maximized
options.add_experimental_option("debuggerAddress", debugger_address)

driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# --------------------------------------------------
# Navigate to TradingView Chart
# --------------------------------------------------
driver.get("https://www.tradingview.com/chart/WQ0zUSgM/")
print("Page title:", driver.title)
time.sleep(5)  # Allow page to load

wait = WebDriverWait(driver, 30)

# Wait for the watchlist container to appear
watchlist_container = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".watchlist-__KRxuOy"))
)

# --------------------------------------------------
# Function to Export Data for a Coin using Shift+Tab navigation
# --------------------------------------------------
def export_data_for_coin(coin_element):
    try:
        # Scroll coin into view and click it to update the chart.
        driver.execute_script("arguments[0].scrollIntoView(true);", coin_element)
        coin_element.click()
        
        symbol = coin_element.get_attribute("data-symbol-full")
        print(f"Processing {symbol}...")
        time.sleep(2)  # Allow chart update
        
        # Click the "Generate report" button.
        gen_report_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Generate report')]]"))
        )
        gen_report_btn.click()
        print("Clicked 'Generate report'.")
        
        # Wait for the spinner to appear and then disappear.
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.spinner-TPU6ljEC")))
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.spinner-TPU6ljEC")))
            print("Loading spinner disappeared.")
        except Exception as e:
            print("Spinner wait issue (fallback to fixed wait):", e)
            time.sleep(10)
        
        # Optionally, wait for the report container to be visible.
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.reportContainer-NyzFj5yn")))
        print("Report container is visible. Proceeding with export data step.")
        
        # Simulate Shift+Tab 5 times then press Enter to activate "Export Data".
        actions = ActionChains(driver)
        for _ in range(5):
            actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        print("Sent Shift+Tab (x5) then Enter to activate 'Export Data'.")
        
        # Wait a bit for any processing/download to complete.
        time.sleep(3)
    
    except Exception as e:
        print(f"Error processing coin {symbol if 'symbol' in locals() else ''}: {e}")

# --------------------------------------------------
# Loop Through the Watchlist Coins and Export Data
# --------------------------------------------------
coins = driver.find_elements(By.CSS_SELECTOR, "[data-symbol-full^='BINANCE:']")

# Loop over each coin (re-fetching the list each iteration to avoid stale element issues).
for i in range(len(coins)):
    coins = driver.find_elements(By.CSS_SELECTOR, "[data-symbol-full^='BINANCE:']")
    if i >= len(coins):
        break
    coin = coins[i]
    export_data_for_coin(coin)

# --------------------------------------------------
# Cleanup
# --------------------------------------------------
driver.quit()
requests.get(close_url)

# --------------------------------------------------
# Beep twice after process finishes
# --------------------------------------------------
def beep_twice():
    try:
        # For Windows systems
        for _ in range(2):
            winsound.Beep(1000, 300)  # 1000Hz for 300ms
            time.sleep(0.5)
    except Exception:
        # Fallback for non-Windows systems: print the bell character
        print('\a')
        time.sleep(0.5)
        print('\a')

beep_twice()
