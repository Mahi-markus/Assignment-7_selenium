from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from report_generator import generate_report

def test_currency_change_for_all(driver, url):
    # Open the webpage
    driver.get(url)
    

    try:
        # Wait for the availability price element to load and be visible
        print("Waiting for availability price element to load...")
        availability_price_element = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, 'js-default-price'))
        )
        initial_availability_price = availability_price_element.text.strip()
        print(f"Initial Availability Price: {initial_availability_price}")

        # Wait for the price elements to load in cards
        print("Waiting for price elements...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
        )
        price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')

        # Select only the first card for testing
        first_card_price = price_elements[0].text
        print(f"First Card Initial Price: {first_card_price}")

        # Scroll to the footer section to locate the currency dropdown
        print("Waiting for currency dropdown to become present...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'js-currency-sort-footer'))
        )
        footer_currency_element = driver.find_element(By.ID, 'js-currency-sort-footer')
        driver.execute_script("arguments[0].scrollIntoView(true);", footer_currency_element)
        time.sleep(1)  # Wait for the scroll to complete

        # Click on the currency dropdown
        currency_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
        )
        currency_dropdown.click()
        print("Currency dropdown clicked.")

        # Fetch all available currency options
        currency_options = driver.find_elements(By.XPATH, "//div[@class='footer-section']//div[@class='footer-currency-dd']//ul[@class='select-ul']//li")
        print(f"Found {len(currency_options)} currency options.")

        results = []  # To store results for all currencies

        for currency_option in currency_options:
            currency_text = currency_option.text.strip()

            # Skip empty or invalid options
            if not currency_text:
                print("Skipping an empty currency option.")
                continue

            print(f"\nTesting currency: {currency_text}")

            # Scroll to and click on the currency option
            driver.execute_script("arguments[0].scrollIntoView(true);", currency_option)
            time.sleep(1)
            try:
                currency_option.click()
            except Exception as e:
                print(f"Error clicking on the currency option {currency_text}: {e}")
                driver.execute_script("arguments[0].click();", currency_option)

            # Wait for the availability price to update
            WebDriverWait(driver, 60).until(
                EC.text_to_be_present_in_element((By.ID, 'js-default-price'), currency_text.split()[0])
            )
            updated_availability_price = availability_price_element.text.strip()
            print(f"Updated Availability Price: {updated_availability_price}")

            # Wait for the prices to update in the cards
            WebDriverWait(driver, 60).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'js-price-value'), currency_text.split()[0])
            )
            updated_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')

            # Select the first card's updated price
            first_card_updated_price = updated_price_elements[0].text
            print(f"First Card Updated Price: {first_card_updated_price}")

            # Compare initial and updated prices
            if first_card_price != first_card_updated_price:
                test_result = "PASS (Currency changed successfully)"
            else:
                test_result = "FAIL (Currency did not change)"

            # Verify if availability price has changed
            if currency_text.split()[0] in updated_availability_price:
                availability_result = "PASS (Currency changed successfully)"
            else:
                availability_result = "FAIL (Currency did not change)"

            print(f"First Card Price Test Result: {test_result}")
            print(f"Availability Price Test Result: {availability_result}")

            # Add results for this currency
            results.append([
                currency_text,
                "Card 1",
                first_card_price,
                first_card_updated_price,
                test_result,
                initial_availability_price,
                updated_availability_price,
                availability_result
            ])

            # Reopen the dropdown for the next currency
            currency_dropdown = driver.find_element(By.ID, 'js-currency-sort-footer')
            driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
            currency_dropdown.click()
            currency_options = driver.find_elements(By.XPATH, "//div[@class='footer-section']//div[@class='footer-currency-dd']//ul[@class='select-ul']//li")

        return results
    except Exception as e:
        print(f"Error occurred during currency change testing: {e}")
        return []



# Main execution
if __name__ == "__main__":
    # Set Chrome options
    options = Options()
    # options.add_argument('--headless')  # Uncomment to run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-analytics")
 

    # Initialize the WebDriver for Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = "https://www.alojamiento.io/property/apartamentos-centro-coló3n/BC-189483"
        currency_results = test_currency_change_for_all(driver, url)

        # Prepare dummy test_results and url_links (Replace with actual results)
        test_results = [
            [url, "Sample Test 1", "PASS", "Test passed successfully"],
            [url, "Sample Test 2", "FAIL", "Test failed"]
        ]
        url_links = [
            [url, "URL Link 1", "PASS", "Valid link"],
            [url, "URL Link 2", "FAIL", "Broken link"]
        ]

        # Generate the report
        #generate_report(test_results, url_links, currency_results)
    finally:
        driver.quit()
