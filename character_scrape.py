def guide(name):
    def fetch_image_from_url(url):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://google.com",
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            print("Fetched HTML snippet:", response.text[:500])  # 🔹 print first 500 chars
        except Exception as e:
            print("Request failed:", e)
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all('meta'):
            if tag.get('property') == 'og:image':
                return tag.get('content')
        return None

    name = name.lower().replace(" ", "-")
    main_url = f"https://kqm.gg/i/{name}/"
    return fetch_image_from_url(main_url)