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

try:
    os.remove("data.json")
except:
    pass

if __name__ == "__main__":
    TOKYOURL = "https://www.japan-property.jp/property-for-sale/Tokyo"
    tokyo = Parser(TOKYOURL)
    data = tokyo.get_urls_of_pages()
    for i in data:
        tokyo.get_data_of_properties("https://www.japan-property.jp" + i)

if __name__ == "__main__":
    KANAGAWAURL = "https://www.japan-property.jp/property-for-sale/Kanagawa"
    kanagawa = Parser(KANAGAWAURL)
    data = kanagawa.get_urls_of_pages()
    for i in data:
        kanagawa.get_data_of_properties("https://www.japan-property.jp" + i)

if __name__ == "__main__":
    HOKKAIDOURL = "https://www.japan-property.jp/property-for-sale/Hokkaido"
    hokkaido = Parser(HOKKAIDOURL)
    data = hokkaido.get_urls_of_pages()
    for i in data:
        kanagawa.get_data_of_properties("https://www.japan-property.jp" + i)

if __name__ == "__main__":
    OKINAWAURL = "https://www.japan-property.jp/property-for-sale/Okinawa"
    okinawa = Parser(OKINAWAURL)
    data = okinawa.get_urls_of_pages()
    for i in data:
        okinawa.get_data_of_properties("https://www.japan-property.jp" + i)

if __name__ == "__main__":
    FUKUOKAURL = "https://www.japan-property.jp/property-for-sale/Fukuoka"
    fukuoka = Parser(FUKUOKAURL)
    data = fukuoka.get_urls_of_pages()
    for i in data:
        fukuoka.get_data_of_properties("https://www.japan-property.jp" + i)

if __name__ == "__main__":
    OSAKAURL = "https://www.japan-property.jp/property-for-sale/Osaka"
    osaka = Parser(OSAKAURL)
    data = osaka.get_urls_of_pages()
    for i in data:
        osaka.get_data_of_properties("https://www.japan-property.jp" + i)  

if __name__ == "__main__":
    KYOTOURL = "https://www.japan-property.jp/property-for-sale/Kyoto"
    kyoto = Parser(KYOTOURL)
    data = kyoto.get_urls_of_pages()
    for i in data:
        kyoto.get_data_of_properties("https://www.japan-property.jp" + i)

import json
from pymongo import MongoClient, errors

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