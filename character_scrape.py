import requests
from bs4 import BeautifulSoup

def guide(name):
    def fetch_image_from_url(url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('meta'):
            if tag.get('property') == 'og:image':
                return tag.get('content')
        return None

    main_url = f"https://kqm.gg/i/{name}/"
    # fallback_url = f"https://keqingmains.com/q/{name}-quickguide/"

    return fetch_image_from_url(main_url)
# print(guide("nahida"))