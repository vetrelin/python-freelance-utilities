import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def get_data(url):
    print(f"Парсим: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # логика сбора данных (например, заголовки и цены)
        items = []
        # допустим, мы ищем блоки с цитатами или товарами
        quotes = soup.find_all('div', class_='quote')
        
        for q in quotes:
            text = q.find('span', class_='text').text
            author = q.find('small', class_='author').text
            items.append({'Текст': text, 'Автор': author})
        return items
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return []

def run_parser():
    # список страниц
    base_url = "http://quotes.toscrape.com/page/"
    urls = [f"{base_url}{i}/" for i in range(1, 6)] # Первые 5 страниц

    # многопоточность
    all_results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_data, urls))
        for res in results:
            all_results.extend(res)

    # сохранение
    df = pd.DataFrame(all_results)
    df.to_excel("parsed_data.xlsx", index=False)
    print("\nГотово! Данные сохранены в parsed_data.xlsx")

if __name__ == "__main__":
    run_parser()