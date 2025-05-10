import requests
from bs4 import BeautifulSoup

def guide(name):
    def fetch_image_from_url(url):
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Search all headers: h1, h2, h3
        header_tags = soup.find_all(['h1', 'h2', 'h3'])

        for tag in header_tags:
            tag_text = tag.get_text(strip=True)
            if tag_text in ["Infographic", "TL;DR"]:
                figure = tag.find_next('figure')
                if figure:
                    img = figure.find('img')
                    if img and img.get('src'):
                        return img['src']
                break

        return None

    # main and fallback URLs
    main_url = f"https://keqingmains.com/{name}/"
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