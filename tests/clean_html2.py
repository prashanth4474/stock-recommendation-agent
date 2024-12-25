import httpx
from bs4 import BeautifulSoup, Comment
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_html(url, retries=3, backoff_factor=0.3, timeout=10.0):
    for i in range(retries):
        try:
            logging.info(f"Fetching HTML content from {url}, attempt {i+1}")
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                logging.info("Fetched HTML content successfully")
                return response.content
        except (httpx.RequestError, httpx.HTTPStatusError, httpx.ReadTimeout) as e:
            logging.error(f"Error fetching HTML content: {e}")
            if i < retries - 1:
                sleep_time = backoff_factor * (2 ** i)
                logging.info(f"Retrying in {sleep_time:.2f} seconds...")
                await asyncio.sleep(sleep_time)
            else:
                logging.error("Max retries reached. Failed to fetch HTML content.")
                raise

async def clean_html(url, output_file):
    html_content = await fetch_html(url)
    
    # Parse the HTML content using a faster parser
    soup = BeautifulSoup(html_content, 'lxml')
    logging.info("Parsed HTML content with BeautifulSoup")

    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    logging.info("Removed script and style elements")

    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    logging.info("Removed comments")

    # Remove empty elements
    for element in soup.find_all():
        if not element.get_text(strip=True):
            element.decompose()
    logging.info("Removed empty elements")

    # Remove non-content elements (example: navigation, footer, ads)
    for selector in ['nav', 'footer', '.ad', '.advertisement']:
        for element in soup.select(selector):
            element.decompose()
    logging.info("Removed non-content elements")

    # Remove inline styles
    for element in soup.find_all(style=True):
        del element['style']
    logging.info("Removed inline styles")

    # Prettify the cleaned HTML
    cleaned_html = soup.prettify()
    logging.info("Prettified the cleaned HTML")

    # Save the cleaned HTML to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)
    logging.info(f"Cleaned HTML saved to {output_file}")

# Example usage
url = "https://www.screener.in/company/HDFCBANK/"  # Replace with your target URL
output_file = "cleaned_page.html"  # The file where the cleaned HTML will be saved

# Run the async function
asyncio.run(clean_html(url, output_file))