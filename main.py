# design a program to download specific reports from SEC edgar system
# input: Company Name/Ticker, report type (such as 13F, 13G, 10Q, etc. )

"""Checking the description and legal compliances through the official website:
https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
Limitations:
Current max request rate: 10 requests/second

Sample Declared Bot Request Headers:

User-Agent:Sample Company Name AdminContact@<sample company domain>.com

Accept-Encoding:gzip, deflate

Host:www.sec.gov
packages needed:
sec_edgar_downloader
request
"""

#install the requirements by running
"""
pip install -r requirements.txt
"""
# using the sec-api.io Python library which helps in api calls to the website
import requests as requests
from sec_edgar_downloader import Downloader
# taking user input: company name/ ticker and report type
ticker = input("Enter Company Ticker (e.g., AAPL): ").strip().upper()
report_type = input("Enter Report Type (e.g., 10-K): ").strip().upper()


# validating if the entries are correct
correct={"10-K": "10-K", "10Q": "10-Q", "10-Q": "10-Q","8-K": "8-K", "13F": "13F-HR", "13G": "SC 13G","S-1": "S-1", "20-F": "20-F", "6-K": "6-K"}
def is_valid_ticker(ticker: str) -> bool:# Validate report type
   try:
        url = "https://www.sec.gov/files/company_tickers.json"
        headers = {
            "User-Agent": "YESHIVA UNIVERSITY lbhupath@mail.yu.edu",  # Required by SEC
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return any(item["ticker"].upper() == ticker for item in data.values())
   except Exception as e:
        print(f" Error validating ticker: {e}")
        return False

if report_type not in correct:
    print(f" Invalid report type: {report_type}")
    print(f"Allowed types: {', '.join(sorted(correct))}")
elif not is_valid_ticker(ticker):
    print(f"Ticker '{ticker}' not found in SEC database.")
else:
    # Initialize Downloader (required by SEC)
    # The filings are downloaded locally into a folder named SEC-Edgar-filings in txt format
    dl = Downloader("YESHIVA UNIVERSITY", "lbhupath@mail.yu.edu")

    try:
        # Download latest filing for the given stock name,here limit tells the number of reports
        dl.get(report_type, ticker, limit=1)
        print(f"Latest {report_type} filing for {ticker} downloaded successfully!")
        print("Check the 'SEC-Edgar-filings' folder.")
    except Exception as e:
        print(f"Could not download filings for ticker '{ticker}'. Error: {e}")

