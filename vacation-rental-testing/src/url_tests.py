import requests
from selenium.webdriver.common.by import By

def test_url_status(driver, test_results, url_links):
    try:
        # Find all <a> tags (links)
        links = driver.find_elements(By.TAG_NAME, "a")
        if not links:
            raise ValueError("No links found on the page!")

        for link in links:
            url = link.get_attribute("href")
            if url:
                # Ensure the URL is valid and skip if it's not an HTTP/HTTPS link
                if not (url.startswith("http://") or url.startswith("https://")):
                    print(f"Skipping invalid URL: {url}")
                    continue

                print(f"Found URL: {url}")  # Debugging: Print URLs to check they are being extracted
                try:
                    # Make a HEAD request to check the status code without downloading the full content
                    response = requests.head(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    status = "Pass" if response.status_code != 404 else "Fail"
                    message = "Valid URL" if status == "Pass" else f"Status Code: {response.status_code}"

                    # Store the result in both url_links and test_results
                    url_links.append([url, "URL Validity", status, message])
                    if status == "Fail":  # Only add 404 links to test_results
                        test_results.append([url, "URL Status", "Fail", message])
                except requests.exceptions.RequestException as e:
                    # Handle any request errors (e.g., timeouts, connection errors, etc.)
                    error_message = f"Error: {str(e)}"
                    url_links.append([url, "URL Validity", "Fail", error_message])
                    test_results.append([url, "URL Status", "Fail", error_message])
            else:
                print("Skipping empty href attribute.")
    except Exception as e:
        # If something goes wrong, log the exception in the test results
        error_message = f"Exception occurred: {str(e)}"
        test_results.append([None, "URL Status", "Fail", error_message])
        print(error_message)






