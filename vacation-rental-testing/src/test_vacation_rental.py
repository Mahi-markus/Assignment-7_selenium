import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from report_generator import generate_report  # Import from the separate report generation module

# Choose browser (Chrome by default)
BROWSER = "chrome"  # Change to "firefox" for Firefox browser

# Initialize WebDriver
def setup_driver():
    if BROWSER.lower() == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif BROWSER.lower() == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise ValueError("Unsupported browser! Choose 'chrome' or 'firefox'.")
    return driver

# WebDriver setup
driver = setup_driver()
driver.maximize_window()
driver.get("https://www.alojamiento.io/")

# Results storage
test_results = []
url_links = []

# Test 1: H1 Tag Existence
def test_h1_tag():
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        assert h1_tag.is_displayed()
        test_results.append(["https://www.alojamiento.io/", "H1 Tag Existence", "Pass", "H1 tag found"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "H1 Tag Existence", "Fail", str(e)])

# Test 2: HTML Tag Sequence
def test_html_tag_sequence():
    try:
        html_tags = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6")
        for i in range(1, len(html_tags)):
            assert html_tags[i].tag_name >= html_tags[i - 1].tag_name, "HTML tags are not in proper sequence"
        test_results.append(["https://www.alojamiento.io/", "HTML Tag Sequence", "Pass", "All tags are in sequence"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "HTML Tag Sequence", "Fail", str(e)])

# Test 3: Image Alt Attributes
def test_image_alt_attributes():
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img for img in images if not img.get_attribute("alt")]
        if missing_alt:
            raise ValueError(f"{len(missing_alt)} images missing alt attributes")
        test_results.append(["https://www.alojamiento.io/", "Image Alt Attribute", "Pass", "All images have alt attributes"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "Image Alt Attribute", "Fail", str(e)])

# Test 4: URL Status Code
def test_url_status():
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            url = link.get_attribute("href")
            if url:
                try:
                    response = requests.get(url)
                    status = "Pass" if response.status_code != 404 else "Fail"
                    message = "Valid URL" if status == "Pass" else f"Status Code: {response.status_code}"
                    
                    # Store the result in both url_links and test_results
                    url_links.append([url, "URL Validity", status, message])
                    if status == "Fail":  # Only add 404 links to test_results
                        test_results.append([url, "URL Status", "Fail", message])
                except requests.exceptions.RequestException as e:
                    url_links.append([url, "URL Validity", "Fail", f"Error: {e}"])
                    test_results.append([url, "URL Status", "Fail", f"Error: {e}"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "URL Status", "Fail", str(e)])

# Execute Tests
test_h1_tag()
test_html_tag_sequence()
test_image_alt_attributes()
test_url_status()

# Generate Excel Report
generate_report(test_results, url_links, [])

driver.quit()
