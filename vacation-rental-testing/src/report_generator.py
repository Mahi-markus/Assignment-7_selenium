import pandas as pd

def generate_report(test_results=None, url_links=None, currency_results=None):
    try:
        with pd.ExcelWriter("vacation_rental_test_report.xlsx", engine="openpyxl") as writer:
            if test_results:
                test_results_df = pd.DataFrame(test_results, columns=["URL", "Test Name", "Status", "Message"])
                test_results_df.to_excel(writer, sheet_name="Test Results", index=False)

            if url_links:
                url_links_df = pd.DataFrame(url_links, columns=["URL", "Test Name", "Status", "Message"])
                url_links_df.to_excel(writer, sheet_name="URL Links", index=False)

            if currency_results:
                currency_results_df = pd.DataFrame(
                    currency_results, 
                    columns=[
                        "Currency", "Card Number", "Initial Price", "Updated Price", "Test Result", 
                        "Initial Availability Price", "Updated Availability Price", "Availability Test Result"
                    ]
                )
                currency_results_df.to_excel(writer, sheet_name="Currency", index=False)

        print("Report generated successfully in 'vacation_rental_test_report.xlsx'.")
    except Exception as e:
        print(f"Error generating the report: {e}")



