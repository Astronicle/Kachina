import requests
from bs4 import BeautifulSoup

def guide(name):
    try:
        # Define the URL
        url = f"https://keqingmains.com/{name}/"
        
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()
        
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all h1 tags and print their text content for debugging
        h1_tags = soup.find_all('h1')
        
        # Find the 'Infographic' header by checking for the exact text
        infographic_header = None
        for h1 in h1_tags:
            if h1.get_text(strip=True) == "Infographic" or h1.get_text(strip=True) == "TL;DR":
                infographic_header = h1
                break
        
        if infographic_header:
            # Find the next figure tag immediately following the 'Infographic' header
            figure = infographic_header.find_next('figure')
            
            # Check if the figure tag contains an img tag
            img = figure.find('img') if figure else None
            if img:
                return img['src']
        
        return "No image found after 'Infographic' text."
    
    except Exception as e:
        return f"Error: {e}"