import pandas as pd

def generate_report(test_results, url_links, currency_results):
    # Convert test_results to a DataFrame
    test_results_df = pd.DataFrame(test_results, columns=["URL", "Test Name", "Status", "Message"])
    
    # Convert url_links to a DataFrame with proper column names
    url_links_df = pd.DataFrame(
        url_links, 
        columns=["URL", "Test Name", "Status", "Message"]
    )
    
    # Save the DataFrames to an Excel file
    with pd.ExcelWriter("vacation_rental_test_report.xlsx") as writer:
        test_results_df.to_excel(writer, sheet_name="Test Results", index=False)
        url_links_df.to_excel(writer, sheet_name="URL Links", index=False)
        if currency_results:  # Include currency results if provided
            currency_results_df = pd.DataFrame(currency_results, columns=["URL", "Test Name", "Status", "Message"])
            currency_results_df.to_excel(writer, sheet_name="Currency Results", index=False)

