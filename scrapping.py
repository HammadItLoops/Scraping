import requests
from bs4 import BeautifulSoup

url = "https://www.hebrew4christians.com/Articles/articles.html"

# r = requests.get(url)
#print(r)


#  headers
headers = {
    "accept-ranges": "bytes",
    "dnt": "1",
    "referer": "https://www.hebrew4christians.com/Articles/articles.html",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

# GET request
response = requests.get(url, headers=headers)

#request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()

    # remove excessive whitespace
    cleaned_text = "\n".join(
        [line.strip() for line in page_text.splitlines() if line.strip()]
    )

    print(cleaned_text)

# Save the text to a file
    with open("extracted_text.txt", "w", encoding="utf-8") as file:
        file.write(cleaned_text)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
