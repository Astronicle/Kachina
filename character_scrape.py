import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def guide(name):
    def fetch_image_from_url(url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Search all meta tags
        meta_tags = soup.find_all('meta')

        for tag in meta_tags:
            tag_prop = tag.get('property')
            if tag_prop == 'og:image':
                return tag['content']

        return None

    # main and fallback URLs
    main_url = f"https://kqm.gg/i/{name}/"
    fallback_url = f"https://keqingmains.com/q/{name}-quickguide/"

    try:
        img_url = fetch_image_from_url(main_url)
        if img_url:
            return img_url
        else:
            raise ValueError("No image found at main URL.")
    except Exception:
        try:
            img_url = fetch_image_from_url(fallback_url)
            if img_url:
                return img_url
            else:
                return "No image found in fallback URL either."
        except Exception as fe:
            return f"Error in fallback URL: {fe}"