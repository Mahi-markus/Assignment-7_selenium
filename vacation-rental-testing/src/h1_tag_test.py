from selenium.webdriver.common.by import By


def test_h1_tag(driver, test_results):
    try:
        h1_tag = driver.find_element(By.TAG_NAME, "h1")
        assert h1_tag.is_displayed()
        test_results.append(["https://www.alojamiento.io/", "H1 Tag Existence", "Pass", "H1 tag found"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "H1 Tag Existence", "Fail", str(e)])
