from selenium.webdriver.common.by import By

def test_image_alt_attributes(driver, test_results):
    try:
        images = driver.find_elements(By.TAG_NAME, "img")
        missing_alt = [img for img in images if not img.get_attribute("alt")]
        if missing_alt:
            raise ValueError(f"{len(missing_alt)} images missing alt attributes")
        test_results.append(["https://www.alojamiento.io/", "Image Alt Attribute", "Pass", "All images have alt attributes"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "Image Alt Attribute", "Fail", str(e)])
