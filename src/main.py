import requests
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
time.sleep(5)  # Allow the page to load

# Create a wait instance
wait = WebDriverWait(driver, 20)

# Wait for the watchlist container to be present (adjust the selector if necessary)
watchlist_container = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".watchlist-__KRxuOy"))
)

# ---------------------------
# Define a Function to Export Data for Each Coin
# ---------------------------
def export_data_for_coin(coin_element):
    try:
        # Scroll coin into view and click it
        driver.execute_script("arguments[0].scrollIntoView(true);", coin_element)
        coin_element.click()
        
        # Get the coin's symbol (e.g. "BINANCE:BTCUSDT.P")
        symbol = coin_element.get_attribute("data-symbol-full")
        print(f"Processing {symbol}...")
        time.sleep(2)  # Wait for the chart to update
        
        # Wait for the "Generate report" button to become clickable and click it.
        gen_report_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(),'Generate report')]]")
            )
        )
        gen_report_btn.click()
        print("Clicked 'Generate report'.")
        
        # Option 2: Wait dynamically until the export button becomes active.
        # We assume that the export button has a class that includes "ghost-PVWoXu5j"
        # and while disabled it includes "gray". Wait until "gray" is no longer in the class.
        export_btn = wait.until(lambda d:
            d.find_element(By.XPATH, "//button[contains(@class, 'ghost-PVWoXu5j')]")
            if "gray" not in d.find_element(By.XPATH, "//button[contains(@class, 'ghost-PVWoXu5j')]").get_attribute("class")
            else None
        )
        export_btn.click()
        print("Clicked 'Export Data'.")
        
        # Wait a bit for the export process to complete (if necessary)
        time.sleep(3)
    
    except Exception as e:
        print(f"Error processing coin {symbol if 'symbol' in locals() else ''}: {e}")

# ---------------------------
# Loop Through the Watchlist Coins and Export Data
# ---------------------------
# Get the list of coin elements. These should have a "data-symbol-full" attribute starting with "BINANCE:"
coins = driver.find_elements(By.CSS_SELECTOR, "[data-symbol-full^='BINANCE:']")

# Loop over each coin. (Re-fetch the list each iteration to avoid stale element issues.)
for i in range(len(coins)):
    coins = driver.find_elements(By.CSS_SELECTOR, "[data-symbol-full^='BINANCE:']")
    if i >= len(coins):
        break
    coin = coins[i]
    export_data_for_coin(coin)

# ---------------------------
# Cleanup: Close Browser and Stop AdsPower Session
# ---------------------------
driver.quit()
requests.get(close_url)
