import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

BROWSER = "chrome"  # Change to "firefox" for Firefox browser

# Setup WebDriver
def setup_driver():
    if BROWSER.lower() == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif BROWSER.lower() == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise ValueError("Unsupported browser! Choose 'chrome' or 'firefox'.")
    return driver

# Test Results
currency_results = []

# Test: Currency Filter
def test_currency_filter(driver):
    try:
        # Navigate to the website
        driver.get("https://www.alojamiento.io/")
        time.sleep(3)  # Allow the page to load
        
        # Find the currency dropdown
        currency_dropdown = driver.find_element(By.CLASS_NAME, "nav-link.cursor-pointer.custom-currency")  # Update as needed
        currency_dropdown.click()

        # Retrieve options within the dropdown
        options = driver.find_elements(By.TAG_NAME, "option")
        for option in options:
            currency_symbol = option.text.strip()
            option.click()
            time.sleep(2)  # Wait for prices to update

            # Verify prices contain the currency symbol
            prices = driver.find_elements(By.CLASS_NAME, "listing-price.absolute.text-center.color-dark")  # Update as needed
            if not prices:
                raise ValueError("No prices found on the page.")

            if not all(currency_symbol in price.text for price in prices):
                raise ValueError(f"Prices did not update correctly for currency: {currency_symbol}")

        currency_results.append(["https://www.alojamiento.io/", "Currency Filter", "Pass", "Currency filter works correctly"])
    except Exception as e:
        currency_results.append(["https://www.alojamiento.io/", "Currency Filter", "Fail", str(e)])

# Generate CSV Report
def generate_csv_report(filename, results):
    df = pd.DataFrame(results, columns=["URL", "Test Case", "Status", "Details"])
    df.to_csv(filename, index=False)
    print(f"Report generated: {filename}")

# Main Execution
if __name__ == "__main__":
    driver = setup_driver()
    driver.maximize_window()

    try:
        test_currency_filter(driver)
    finally:
        driver.quit()

    # Generate the report
    generate_csv_report("currency_filter_test_results.csv", currency_results)
