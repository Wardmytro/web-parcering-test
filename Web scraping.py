try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None
    print("Модуль requests або bs4 не встановлено. Використовується urllib для веб-запитів.")

if requests:
    response = requests.get("https://example.com")
    print(response.status_code)
else:
    import urllib.request
    with urllib.request.urlopen("https://example.com") as response:
        print(response.status)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
price_element = soup.find("span", class_="product-price")
print(f"Ціна товару: {price_element.text}")