import cloudscraper
from bs4 import BeautifulSoup

def guide(name):
    try:
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        })

        name = name.lower().replace(" ", "-")
        url = f"https://kqm.gg/i/{name}/"

        response = scraper.get(url, headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        }, timeout=10)

        # Log or return the status code
        if response.status_code != 200:
            return f"❌ HTTP Error {response.status_code} while fetching {url}"

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('meta'):
            if tag.get('property') == 'og:image':
                return tag.get('content')

        return "⚠️ No og:image meta tag found."

    except Exception as e:
        # Return the error text to Discord
        return f"💥 Exception occurred: {type(e).__name__} - {e}"

# Example test
print(guide("Nahida"))