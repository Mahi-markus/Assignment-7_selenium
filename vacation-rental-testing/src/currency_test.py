from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_currency_change_for_all(driver, url):
    driver.get(url)

    # Capture the initial value of the availability price
    availability_price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'js-default-price'))
    )
    initial_availability_price = availability_price_element.text.strip()
    print(f"Initial Availability Price: {initial_availability_price}")

    # Wait for the price elements to load in cards
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-price-value'))
    )
    price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
    first_card_price = price_elements[0].text
    print(f"First Card Initial Price: {first_card_price}")

    # Scroll to the footer section to locate the currency dropdown
    footer_currency_element = driver.find_element(By.ID, 'js-currency-sort-footer')
    driver.execute_script("arguments[0].scrollIntoView(true);", footer_currency_element)
    time.sleep(1)

    # Click on the currency dropdown
    currency_dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
    )
    currency_dropdown.click()

    # Fetch all available currency options
    currency_options = driver.find_elements(By.XPATH, "//div[@class='footer-section']//div[@class='footer-currency-dd']//ul[@class='select-ul']//li")
    results = []

    for currency_option in currency_options:
        currency_text = currency_option.text.strip()
        if not currency_text:
            continue

        print(f"\nTesting currency: {currency_text}")
        driver.execute_script("arguments[0].scrollIntoView(true);", currency_option)
        time.sleep(1)
        try:
            currency_option.click()
        except Exception:
            driver.execute_script("arguments[0].click();", currency_option)

        WebDriverWait(driver, 50).until(
            EC.text_to_be_present_in_element((By.ID, 'js-default-price'), currency_text.split()[0])
        )
        updated_availability_price = availability_price_element.text.strip()

        WebDriverWait(driver, 50).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'js-price-value'), currency_text.split()[0])
        )
        updated_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
        first_card_updated_price = updated_price_elements[0].text

        test_result = "PASS (Currency changed successfully)" if first_card_price != first_card_updated_price else "FAIL (Currency did not change)"
        availability_result = "PASS (Currency changed successfully)" if currency_text.split()[0] in updated_availability_price else "FAIL (Currency did not change)"

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
