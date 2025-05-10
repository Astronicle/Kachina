import requests
from bs4 import BeautifulSoup

def guide(url):
    try:
        # Fetch the page
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        img = soup.find('img', class_=lambda c: c and c.startswith('wp-image-'))

        if img and img.get('src'):
            return img['src']
        
        return "No matching image found."

    except Exception as e:
        return f"Error: {e}"