import requests
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ---------------------------
# Start AdsPower Browser Session
# ---------------------------
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
options.add_experimental_option("debuggerAddress", debugger_address)

driver = webdriver.Chrome(service=service, options=options)

# ---------------------------
# Navigate to TradingView Chart
# ---------------------------
driver.get("https://www.tradingview.com/chart/WQ0zUSgM/")
print("Page title:", driver.title)
time.sleep(5)  # Allow page to load

wait = WebDriverWait(driver, 30)

# Wait for the watchlist container to appear
watchlist_container = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".watchlist-__KRxuOy"))
)

# ---------------------------
# Function to Export Data for a Coin using Shift+Tab navigation
# ---------------------------
def export_data_for_coin(coin_element):
    try:
        # Scroll coin into view and click it to update the chart.
        driver.execute_script("arguments[0].scrollIntoView(true);", coin_element)
        coin_element.click()
        
        symbol = coin_element.get_attribute("data-symbol-full")
        print(f"Processing {symbol}...")
        time.sleep(2)  # Wait for chart update
        
        # Click the "Generate report" button.
        gen_report_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Generate report')]]"))
        )
        gen_report_btn.click()
        print("Clicked 'Generate report'.")
        
        # Wait for the report generation process to start.
        time.sleep(10)
        
        # Now simulate Shift+Tab 5 times to focus the export data button,
        # then press Enter.
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

# ---------------------------
# Loop Through the Watchlist Coins and Export Data
# ---------------------------
coins = driver.find_elements(By.CSS_SELECTOR, "[data-symbol-full^='BINANCE:']")

# Loop over each coin (re-fetching the list each iteration to avoid stale element issues).
for i in range(len(coins)):
    coins = driver.find_elements(By.CSS_SELECTOR, "[data-symbol-full^='BINANCE:']")
    if i >= len(coins):
        break
    coin = coins[i]
    export_data_for_coin(coin)

# ---------------------------
# Cleanup
# ---------------------------
driver.quit()
requests.get(close_url)
