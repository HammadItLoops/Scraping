import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Base URL of the website
base_url = "https://www.hebrew4christians.com/Articles/articles.html"

#r = requests.get(url)
#print(r)

# Headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

# A set to store visited URLs and prevent duplicate scraping
visited_urls = set()

def scrape_page(url):
    """Scrapes a page and extracts its text content."""
    if url in visited_urls:
        return  # Skip if already visited

    print(f"Scraping: {url}")
    visited_urls.add(url)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = "\n".join([line.strip() for line in soup.get_text().splitlines() if line.strip()])

            # Save the text to a file
            with open("extracted2_text.txt", "a", encoding="utf-8") as file:
                file.write(f"\n\n=== {url} ===\n\n")
                file.write(page_text)

            # Find and process internal links
            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(url, href)  # Convert relative URL to absolute
                if is_valid_url(full_url):
                    scrape_page(full_url)
        else:
            print(f"Failed to fetch {url}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

def is_valid_url(url):
    """Checks if the URL belongs to the same domain and has not been visited."""
    parsed_url = urlparse(url)
    return parsed_url.netloc == urlparse(base_url).netloc and url not in visited_urls

# Start scraping
scrape_page(base_url)

print("Scraping completed!")
