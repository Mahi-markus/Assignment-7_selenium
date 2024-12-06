import pandas as pd

def generate_report(test_results, url_links, currency_results):
    # Create DataFrames
    test_results_df = pd.DataFrame(test_results, columns=["URL", "Test", "Result", "Message"])
    url_links_df = pd.DataFrame(url_links, columns=["URL"])
    currency_df = pd.DataFrame(currency_results, columns=["URL", "Test", "Result", "Message"])

    # Save to Excel
    with pd.ExcelWriter("test_report.xlsx") as writer:
        test_results_df.to_excel(writer, sheet_name="Test Results", index=False)
        url_links_df.to_excel(writer, sheet_name="URL Links", index=False)
        currency_df.to_excel(writer, sheet_name="Currency Filter", index=False)

    print("Report generated successfully: test_report.xlsx")
