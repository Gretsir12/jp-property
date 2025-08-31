"""
!!!не забудьте установить все нужные бибилиоткеки "pip install -r req.txt"!!!
Скрипт для обновления/создания базы данных (нужно при первом запуске чтобы наполнить базц данных свежими объявлениями с https://www.japan-property.jp/)
Если объявление в базе данных уже существует то оно не будет создаваться повторно
Сначала скрипт записывает все в data.json, а потом кладет в базу
Для перевода используется установленная локально LLM модель (при первом запуске она сама установится)
Цены переводятся по реальному курсу с https://www.google.com/finance/quote/JPY-RUB
"""
from staff.parsers import Parser
import os

import json
from pymongo import MongoClient, errors

try:
    os.remove("data.json")
except:
    pass

urls = (
    "https://www.japan-property.jp/property-for-sale/Tokyo",
    "https://www.japan-property.jp/property-for-sale/Kanagawa",
    "https://www.japan-property.jp/property-for-sale/Hokkaido",
    "https://www.japan-property.jp/property-for-sale/Okinawa",
    "https://www.japan-property.jp/property-for-sale/Fukuoka",
    "https://www.japan-property.jp/property-for-sale/Osaka",
    "https://www.japan-property.jp/property-for-sale/Kyoto"
)


for URL in urls:
    if __name__ == "__main__":
        city = Parser(URL)
        data = city.get_urls_of_pages()
        for i in data:
            city.get_data_of_properties("https://www.japan-property.jp" + i)

client = MongoClient("mongodb://localhost:27017/")
db = client["jp-property"]
collection = db["properties"]

collection.create_index("url", unique=True)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

try:
    if isinstance(data, list):
        collection.insert_many(data, ordered=False)
    else:
        collection.insert_one(data)
    print("Sucsessfull")
except errors.DuplicateKeyError:
    print("Document exists, skip")