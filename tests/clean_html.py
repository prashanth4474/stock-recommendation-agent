import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_html(url, output_file):
    logging.info(f"Fetching HTML content from {url}")
    
    # Fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    logging.info("Fetched HTML content successfully")

    # Parse the HTML content using a faster parser
    soup = BeautifulSoup(response.content, 'lxml')
    logging.info("Parsed HTML content with BeautifulSoup")

    # Perform any cleaning operations here
    # For example, removing script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    logging.info("Removed script and style elements")

    # Prettify the cleaned HTML
    cleaned_html = soup.prettify()
    logging.info("Prettified the cleaned HTML")

    # Save the cleaned HTML to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)
    logging.info(f"Cleaned HTML saved to {output_file}")

# Example usage
url = "https://www.nseindia.com/get-quotes/equity?symbol=HDFCBANK"  # Replace with your target URL
output_file = "cleaned_page.html"  # The file where the cleaned HTML will be saved
clean_html(url, output_file)