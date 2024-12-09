import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from h1_tag_test import test_h1_tag
from html_tag_sequence_test import test_html_tag_sequence
from image_alt_test import test_image_alt_attributes
from currency_test import test_currency_change_for_all
from report_generator import generate_report
from url_tests import test_url_status  # Import the new test


BROWSER = "chrome"
TIMEOUT = 30  # Timeout duration in seconds


# Initialize WebDriver
def initialize_driver():
    options = Options()
    options.add_argument("--headless")  # Optional: Use headless mode
    options.add_argument("--no-sandbox")  # Recommended for CI environments
    options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--log-level=3")  # Reduce log verbosity

    if BROWSER.lower() == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        raise ValueError("Unsupported browser! Choose 'chrome' or 'firefox'.")
    return driver


# Main function to run all tests
def main():
    url = "https://www.alojamiento.io/"
    test_results = []
    currency_results = []
    url_links = []

    # Initialize WebDriver
    driver = initialize_driver()

    try:
        # Open the target URL
        driver.get(url)

        # Set the timeout using WebDriverWait
        wait = WebDriverWait(driver, TIMEOUT)

        # Wait until the page is loaded (for example, checking the presence of <body> element)
        #wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Run the tests
        print("Running H1 Tag Existence Test...")
        test_h1_tag(driver, test_results)

        print("Running HTML Tag Sequence Test...")
        test_html_tag_sequence(driver, test_results)

        print("Running Image Alt Attribute Test...")
        test_image_alt_attributes(driver, test_results)

        print("Running URL Status Test...")
        test_url_status(driver, test_results, url_links)

        # Debugging: Check the url_links before generating the report
        print(f"URL Links: {url_links}")

        print("Running Currency Change Test...")
        #currency_results = test_currency_change_for_all(driver, url)

        # Generate the report
        print("Generating the report...")
        generate_report(test_results=test_results, url_links=url_links, currency_results=currency_results)

    except Exception as e:
        print(f"An error occurred while running the tests: {str(e)}")
    finally:
        driver.quit()

    print("All tests completed successfully.")



if __name__ == "__main__":
    main()

