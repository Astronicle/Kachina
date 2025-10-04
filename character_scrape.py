import cloudscraper
from bs4 import BeautifulSoup

def guide(name):
    scraper = cloudscraper.create_scraper()
    name = name.lower().replace(" ", "-")
    url = f"https://kqm.gg/i/{name}/"
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all('meta'):
        if tag.get('property') == 'og:image':
            return tag.get('content')
    return None
print(guide("nahida"))