from os import curdir
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException



def get_products(category):
    # Set up chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    
    # Add user agent to look more like a real browser
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Add additional headers
    chrome_options.add_argument("--accept-language=en-US,en;q=0.9")
    chrome_options.add_argument("--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        url = f"https://www.lcbo.com/en/products#t=clp-products&sort=relevancy&layout=card&f:@stores_stock=[true]&f:@ec_category=[{category}]"
        # url = f"https://www.lcbo.com/en/products#t=clp-products&sort=relevancy&layout=card&f:@ec_category=[{category}]"
        print(f"Navigating to {url}")
        driver.get(url)

        # Wait for the page to load
        print("Waiting for page to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "coveo-product-info"))
        )

        load_more_attempts = 0
        max_attempts = 100

        # Always get the initial set of products
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        product_divs = soup.find_all("div", class_="coveo-product-info")

        print(f"Initial product divs found: {len(product_divs)}")

        # Click button until exhausted
        while load_more_attempts < max_attempts:
            try:
                load_more_button = driver.find_element(By.ID, "loadMore")
                if load_more_button.is_displayed() and load_more_button.is_enabled():
                    # Scroll to button
                    driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                    time.sleep(1)

                    # Click button
                    load_more_button.click()
                    load_more_attempts += 1
                    print("Clicked Load More Button, waiting for new products....")
                    time.sleep(3)

                    # After clicking, update the soup and product_divs
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    product_divs = soup.find_all("div", class_="coveo-product-info")
                    print(f"Found {category}: {len(product_divs)} elements")
                else:
                    print("All products fully loaded")
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    product_divs = soup.find_all("div", class_="coveo-product-info")
                    print(f"Found {category}: {len(product_divs)} elements")
                    break
            except NoSuchElementException:
                print("Load More button not found - all products may be loaded")
                break
            except ElementNotInteractableException:
                print("Load more button not interactable")
                break

        # Extract product names
        products = []
        for div in product_divs:
            product_info = {}

            if not hasattr(div, 'find'):
                continue

            product_title = div.find('span')
            if product_title and hasattr(product_title, 'text'):
                product_info['name'] = (product_title.text.strip())
            else:
                continue

            product_size = div.select_one("div.coveo-result-row.product-item-volume span")
            if product_size and hasattr(product_size, 'text'):
                product_info["volume"] = product_size.text.strip() 
            else: 
                continue

            product_price = div.select_one("div.coveo-result-row.product-item-price span.sr-only")
            if product_price and hasattr(product_price, 'text'):
                product_info["price"] = float(product_price.text.strip().replace("Sale Price $", "").replace("Price $",""))
            else:
                continue

            products.append(product_info)

        return products

    finally:
        driver.quit()


import json

def category_writer(product_list, get_products):

    for i in range(len(product_list)):
        current_product = product_list[i]
        filename = f"{current_product}.json"
        current_product_complete = get_products(current_product)
        with open(filename, 'w') as f:
            json.dump(current_product_complete, f, indent=2)
            print(f"Contents have been written in {filename}")
       




         



