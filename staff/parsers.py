import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import time

from staff.translator import Translator
from staff.convert import Convertor

class Parser():
    def __init__(self, URL):
        self.URL = URL    

    def __str__(self):
        return self.URL

    def clean_images_html(self, array):
        """Clean html with image link and return clean links on images in .webp

        Args:
            array (arr): input array with html code of images in .webp

        Returns:
            arr: return clean links on images in .webp
        """
        clean_links = []
        is_image = False
        for link in array:
            string = str()
            for i in link:
                if is_image:
                    if i == '"':
                        is_image = False
                        clean_links.append(string)
                        break
                    else:
                        string += i
                else:
                    if i == '"':
                        is_image = True
                    continue
        return clean_links

    def get_data_of_properties(self, url):
        """Parse Html page (url) and append data to data.json

        Args:
            url (string): url of property`s page

        Returns:
            None, it appends data in data.json directly
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
        }
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        # grep data from html
        tr = Translator()
        en_title = soup.find("title").get_text(strip=True)
        title = tr.translate(text=en_title, tgt="ru", src="en")

        raw_jpy_price = soup.find_all('p', {'class': 'price'})#.replace('¥', '').replace(',', '').get_text(strip=True)
        jpy_price = float(raw_jpy_price[0].text.replace('¥', '').replace(',', ''))
        convertor = Convertor()
        price = convertor.convert_jpy(jpy_price)
        
        # Fix: Check if description exists
        description = ""
        desc_elem = soup.select_one("div.description01")
        if desc_elem:
            ja_description = desc_elem.get_text(" ", strip=True)
            description = tr.translate(text=ja_description, tgt="ru", src="en")
        else:
            print(f"DEBUG: No description found for {url}")
            description = None
            
        # grep coordinates
        iframe = soup.select_one("div.gmap iframe")
        lat, lon = None, None
        if iframe and "maps?q=" in iframe["src"]:
            coords = iframe["src"].split("maps?q=")[1].split("&")[0]
            lat, lon = coords.split(",")

        # grep images
        images = []
        is_image = False
        string = str()
        img_div = soup.select("div.detail_photo_nav img")
        tmp = 0
        for i in img_div:
            img_div[tmp] = str(img_div[tmp])
            tmp += 1
        images = self.clean_images_html(img_div)

        data = {
            "title": title,
            "url": url,
            "price": price,
            "description": description,
            "images": images,
            "lat": lat,
            "lon": lon,
        }

        # --- Append to data.json ---
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
                if not isinstance(existing, list):
                    existing = [existing]
        except (FileNotFoundError, json.JSONDecodeError):
            existing = []

        existing.append(data)

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
            print("Data was appended to data.json")
        return data

    def get_urls_of_pages(self):
        data = []
        options = Options()
        options.add_argument("--headless")  # Run Chrome in headless mode

        service = Service()  # Specify path to chromedriver if needed
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(self.URL)
        time.sleep(5)

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")

        pattern = r'/apartment-property-for-sale-in-[a-zA-Z0-9-]+-S\d+'

        print("Matching links:")
        for tag in soup.find_all('a', href=True):
            link = tag['href']
            if re.match(pattern, link):
                data.append(link)
        print(f"DEBUG: {data}")
        return data

        with open("data.json", "w", encoding="utf-8") as f:
            f.write(json.dump(data, f, ensure_ascii=False, indent=2))
