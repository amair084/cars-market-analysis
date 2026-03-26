# Car Listing Scraper using Cars.com - Amair084 on GitHub

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import pandas as pd
import time
import random
import re

# DRIVER SETUP  ----------------


name = input("Please enter your car trim: ")
lname = name.lower()

current_dir = Path(__file__).parent
driver_path = current_dir.parent / "chromedriver" / "chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = Service(str(driver_path))
driver = webdriver.Chrome(service=service, options=options)

driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

# SCRAPER SETTINGS  -------

base_url = f"https://www.cars.com/shopping/toyota-{lname}/?page="
pages_to_scrape = 1

all_cars = []

# PAGE LOOP  ---------------

def safe_find(element, by, value):
    try:
        return element.find_element(by, value).text
    except:
        return None

for page in range(1, pages_to_scrape + 1):

    url = base_url + str(page)
    print(f"\nScraping page {page}")

    driver.get(url)

    # refresh logic if page fails
    for attempt in range(3):
        try:

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-listing-id]"))
            )

            listings = driver.find_elements(By.CSS_SELECTOR, "[data-listing-id]")

            if len(listings) > 0:
                break

        except:
            print("Page failed — refreshing...")
            driver.refresh()
            time.sleep(5)

    listings = driver.find_elements(By.CSS_SELECTOR, "[data-listing-id]")
    print("Listings found:", len(listings))

# LISTING LOOP  ----------------

    for car in listings:

        def safe(by, value):
            try:
                return car.find_element(by, value).text
            except:
                return None


        def safevar(by, value, attribute=None):
            try:
                element = car.find_element(by, value)
                if attribute:
                    return element.get_attribute(attribute)
                return element.text
            except:
                return None

        def safe_attr(by, value, attr):
            try:
                return car.find_element(by, value).get_attribute(attr)
            except:
                return None

        title = safe(By.TAG_NAME, "a")

        price = None
        text_block = car.text

        match = re.search(r"\$\d{1,3}(,\d{3})*", text_block)

        if match:
            price = match.group()
        mileage = (
            safe(By.CLASS_NAME, "mileage")
            or safe(By.CSS_SELECTOR, ".mileage")
        )

        dealer = safe(By.CLASS_NAME, "spark-body-small")

        deal = safevar("tag name", "fuse-badge", attribute="variant")

        link = safe_attr(By.TAG_NAME, "a", "href")

        # make title into structured fields
        year = None
        model = None
        trim = None

        if title:
            parts = title.split(" ")
            if len(parts) >= 3:
                year = parts[0]
                model = parts[1]
                trim = " ".join(parts[2:])

        all_cars.append(
            {
                "year": year,
                "model": model,
                "trim": trim,
                "title": title,
                "price": price,
                "mileage": mileage,
                "dealer": dealer,
                "deal": deal,
                "link": link,
            }
        )

    time.sleep(random.uniform(4, 7))

# CLEANUP -----------------

driver.quit()

# SAVE DATA ----------------

df = pd.DataFrame(all_cars)

output_path = current_dir.parent / "data" / f"{lname}_market_data.csv"
output_path.parent.mkdir(exist_ok=True)

df.to_csv(output_path, index=False)

print("\nScraping finished")
print("Total cars collected:", len(df))
print("Saved to:", output_path)
print(df.head())