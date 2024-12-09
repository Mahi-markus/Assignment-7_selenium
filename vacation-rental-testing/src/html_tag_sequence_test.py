from selenium.webdriver.common.by import By

def test_html_tag_sequence(driver, test_results):
    try:
        html_tags = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //h6")
        for i in range(1, len(html_tags)):
            assert html_tags[i].tag_name >= html_tags[i - 1].tag_name, "HTML tags are not in proper sequence"
        test_results.append(["https://www.alojamiento.io/", "HTML Tag Sequence", "Pass", "All tags are in sequence"])
    except Exception as e:
        test_results.append(["https://www.alojamiento.io/", "HTML Tag Sequence", "Fail", str(e)])
