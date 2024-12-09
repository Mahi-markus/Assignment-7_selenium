from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

# Configure WebDriver with the Service class
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the target website
driver.get("https://www.alojamiento.io/")

# Extract all script tags
scripts = driver.find_elements(By.TAG_NAME, 'script')
data_to_extract = []

# Debug: Print the number of script tags found
print(f"Found {len(scripts)} script tags.")

for script in scripts:
    script_content = script.get_attribute('innerHTML')
    
    # Debug: Print part of the script content to check
    print("scraping............")
  

    # Check if the script contains the "ScriptData"
    if "ScriptData" in script_content:
        # Use regex to extract the content of ScriptData
        match = re.search(r'var ScriptData = ({.*?});', script_content, re.DOTALL)
        if match:
            # Extract the JSON-like content
            script_data = match.group(1)
            
            # Extract relevant fields using regex
            try:
                site_url = re.search(r'"SiteUrl":\s*"([^"]+)"', script_data).group(1)
                site_name = re.search(r'"SiteName":\s*"([^"]+)"', script_data).group(1)
                ip = re.search(r'"IP":\s*"([^"]+)"', script_data).group(1)
                country_code = re.search(r'"CountryCode":\s*"([^"]+)"', script_data).group(1)

                # Get browser name dynamically
                browser = driver.capabilities['browserName']

                data = {
                    "SiteURL": site_url,
                    "CampaignID": site_name,  # CampaignID is taken as SiteName here (adjust if needed)
                    "SiteName": site_name,
                    "Browser": browser,
                    "CountryCode": country_code,
                    "IP": ip
                }
                data_to_extract.append(data)
            except AttributeError:
                print("Error extracting values from the script data.")
                
# Debug: Print the extracted data before saving to Excel
print(f"Extracted data: {data_to_extract}")

# Convert to DataFrame
df = pd.DataFrame(data_to_extract)

# Check if DataFrame is populated
if df.empty:
    print("No data was extracted!")
else:
    # Save to Excel
    df.to_excel("output.xlsx", index=False)

# Close the driver
driver.quit()
