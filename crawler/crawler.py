import requests
from bs4 import BeautifulSoup
import logging
import re
from products.models import Product

logger = logging.getLogger(__name__)


class EsmerdisScraper:
    BASE_URL = "https://www.esmerdis.com/shop/page/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def scrape_page(self, page_number):
        url = f"{self.BASE_URL}{page_number}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page {page_number}: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='wd-product')
        product_data = []

        for product in products:
            try:
                product_url = product.find('a', class_='product-image-link')['href']
                
                product_details = self.scrape_product_page(product_url)
                
                if product_details:
                    product_data.append(Product(**product_details))
            except Exception as e:
                logger.error(f"Failed to parse product on page {page_number}: {e}")

        return product_data

    def scrape_product_page(self, product_url):
        try:
            response = requests.get(product_url, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch product page {product_url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            title = soup.find('h1', class_='product_title entry-title wd-entities-title').text.strip()
            price = [price.get_text(strip=True) for price in soup.find_all('span', class_='woocommerce-Price-amount amount')]
            description = soup.find('p', class_='c-product__title').text.strip()
            category = soup.find('span', class_='wd-last-link').text.strip()
            image_urls = []
            for a_tag in soup.find_all('a', href=True):
                if a_tag['href'].endswith('.jpg'):
                    image_urls.append(a_tag['href'])
            return {
                'title': title,
                'price': self.clean_price(price[-1]),
                'description': description,
                'category': category,
                'stock_status': "In Stock",
                'image_urls': image_urls
            }
        except Exception as e:
            logger.error(f"Failed to parse product details from {product_url}: {e}")
            return None

    def scrape_all_pages(self):
        page_number = 1
        all_products = []

        # while True:
        for i in range(1):
            logger.info(f"Scraping page {page_number}...")
            products = self.scrape_page(page_number)
            if not products:
                break  # No more products found

            all_products.extend(products)
            page_number += 1

        if all_products:
            for product_data in all_products:
                Product.objects.update_or_create(
                    title=product_data.title,
                    defaults={
                        'price': product_data.price,
                        'description': product_data.description,
                        'category': product_data.category,
                        'stock_status': product_data.stock_status,
                        'image_urls': product_data.image_urls,
                    }
                )
            logger.info(f"Successfully saved {len(all_products)} products.")
        else:
            logger.warning("No products found to save.")

    def clean_price(self, price_str):
        cleaned_price = re.sub(r'[^\d.]', '', price_str)
        
        if cleaned_price:
            return float(cleaned_price)
        return None