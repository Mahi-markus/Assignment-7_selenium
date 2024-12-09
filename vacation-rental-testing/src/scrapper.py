from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import requests  # For fetching IP and CountryCode dynamically

# Function to get IP and CountryCode (this uses an external API)
def get_ip_and_country():
    try:
        response = requests.get("https://ipinfo.io/")
        data = response.json()
        ip = data.get("ip", "Unknown")
        country = data.get("country", "Unknown")
        return ip, country
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP and country: {e}")
        return "Unknown", "Unknown"

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
    print("Checking script content:")
    print(script_content[:200])  # Print the first 200 characters of the script

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
                
                # Get IP and Country dynamically
                ip, country_code = get_ip_and_country()

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
