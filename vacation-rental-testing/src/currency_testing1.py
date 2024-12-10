
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def click_with_retry(driver, element, retries=3):
    """Tries to click an element with retries if interception occurs."""
    for attempt in range(retries):
        try:
            element.click()
            return True
        except Exception as e:
            print(f"Click attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    return False

def test_currency_change(driver, url):
    driver.get(url)
    results = []

    try:
        # Scroll to the footer section and locate the currency dropdown
        print("Waiting for currency dropdown to become present...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'js-currency-sort-footer'))
        )
        footer_currency_element = driver.find_element(By.ID, 'js-currency-sort-footer')
        driver.execute_script("arguments[0].scrollIntoView(true);", footer_currency_element)
        time.sleep(1)

        # Click the currency dropdown
        currency_dropdown = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, 'js-currency-sort-footer'))
        )
        click_with_retry(driver, currency_dropdown)
        print("Currency dropdown clicked.")

        # Fetch currency options
        currency_options = driver.find_elements(By.XPATH, "//div[@class='footer-section']//div[@class='footer-currency-dd']//ul[@class='select-ul']//li")
        print(f"Found {len(currency_options)} currency options.")

        for currency_option in currency_options:
            currency_text = currency_option.text.strip()

            if not currency_text:
                print("Skipping an empty currency option.")
                continue

            print(f"\nTesting currency: {currency_text}")

            # Scroll to and click on the currency option
            driver.execute_script("arguments[0].scrollIntoView(true);", currency_option)
            time.sleep(1)

            if not click_with_retry(driver, currency_option):
                results.append([currency_text, "FAIL (Click failed)", "N/A", "N/A"])
                continue

            # Validate the currency change
            print(f"Currency {currency_text} selected. Validating changes...")
            try:
                # Wait for the updated price to reflect
                updated_price = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'js-default-price'))
                ).text.strip()

                print(f"Updated price: {updated_price}")

                # Check card prices if applicable
                card_price_elements = driver.find_elements(By.CLASS_NAME, 'js-price-value')
                if card_price_elements:
                    card_price_text = card_price_elements[0].text.strip()
                    if currency_text.split()[0] in card_price_text:
                        card_result = "PASS (Currency updated correctly)"
                    else:
                        card_result = "FAIL (Currency not reflected in card price)"
                else:
                    card_result = "N/A (No card prices available)"

                results.append([currency_text, "PASS (Currency updated successfully)", updated_price, card_result])
            except Exception as e:
                print(f"Error validating currency {currency_text}: {e}")
                results.append([currency_text, "FAIL (Validation error)", "N/A", "N/A"])

            # Reopen the dropdown for the next currency
            try:
                currency_dropdown = driver.find_element(By.ID, 'js-currency-sort-footer')
                driver.execute_script("arguments[0].scrollIntoView(true);", currency_dropdown)
                time.sleep(1)
                click_with_retry(driver, currency_dropdown)
                currency_options = driver.find_elements(By.XPATH, "//div[@class='footer-section']//div[@class='footer-currency-dd']//ul[@class='select-ul']//li")
            except Exception as e:
                print(f"Error reopening dropdown: {e}")
                break

    except Exception as e:
        print(f"Error occurred during currency change testing: {e}")
    return results
