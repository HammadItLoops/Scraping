import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

# Base URL of the website
base_url = "https://www.hebrew4christians.com/index.html#loaded"
stop_url = "https://www.hebrew4christians.com/Online_Store/Books/MyBook/mybook.html"

#r = requests.get(url)
#print(r)

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

# A set to store visited URLs and prevent duplicate scraping
visited_urls = set()

url_queue = deque([base_url])


def scrape_page(url):
    """Scrapes a page and extracts its text content."""
    print(f"Scraping: {url}")
    visited_urls.add(url)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = "\n".join([line.strip() for line in soup.get_text().splitlines() if line.strip()])

            # Save the text
            with open("scraped.docs", "a", encoding="utf-8") as file:
                file.write(f"\n\n=== {url} ===\n\n")
                file.write(page_text)

            # Stop scraping if the target URL is reached
            if url == stop_url:
                print("Target page reached. Stopping scraping.")
                return False

            # Find and process
            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(url, href)  # Convert relative URL to absolute
                if is_valid_url(full_url):
                    url_queue.append(full_url)
        else:
            print(f"Failed to fetch {url}, Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return True


def is_valid_url(url):
    """Checks if the URL belongs to the same domain and has not been visited."""
    parsed_url = urlparse(url)
    return parsed_url.netloc == urlparse(base_url).netloc and url not in visited_urls


# Start scraping
while url_queue:
    current_url = url_queue.popleft()
    if not scrape_page(current_url):
        break

print("Scraping completed!")
