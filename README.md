# Vacation Rental Home Page Automation Testing

This project automates the testing of a vacation rental details page to validate essential elements and functionalities. It checks SEO-impacting test cases such as the presence of `h1` tags, HTML tag sequence, image `alt` attributes, broken URLs, currency filter functionality, and script data scraping. Test results are recorded in an Excel file.

## Features

- Validate the existence of `h1` tags.
- Ensure proper HTML tag sequence ([H1-H6]).
- Check for missing `alt` attributes in images.
- Verify that no URLs return a `404` status.
- Test currency filter functionality and property tile updates.
- Scrape and save site-related data to an Excel file.

## Requirements
- **Operating System**    :Linux
- **Programming Language**: Python
- **Libraries/Tools**: Selenium, Pandas
- **Browser**: Google Chrome
- **Tested on**: [https://www.alojamiento.io/](https://www.alojamiento.io/)

## Installation and Setup

Follow these steps to clone the repository, set up the environment, and run the project:

### 1. Clone the repository:

```bash
git clone https://github.com/Mahi-markus/Assignment-7_selenium.git

```

### 2. Create a virtual environment and activate it:

```bash
python -m venv venv          #On Windows:
venv\Scripts\activate
```

```bash
python3 -m venv venv        #On macOS/Linux:
source venv/bin/activate

```

### 3. Navigate to directory:

```bash
cd vacation-rental-testing
```

### 4. Install the required dependencies:

```bash
pip install -r requirements.txt

```

### 5. Navigate to src folder

```bash
cd src

```

### 6. Run the Automation:

```bash
python main.py
    or
python3 main.py

```

### 7. Run scappper to get the scraped data:

```bash
python scrapper.py
    or
python3 scrapper.py

```

### 8. Output

- Test results and scrapte data will be saved in an Excel file located in the **Output**(src/Output) folder.
- Each test case result includes:
  page_url
  testname
  passed/fail
  comments
- main.py: The main script to run the tests.
- Output/: Folder where the generated Excel reports are saved.
- requirements.txt: List of required necessary libraries.
