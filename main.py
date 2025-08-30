"""Тут простенький бекенд на fastapi который берет все данные из базы данных и выдает их в xml
    Используется база данных mongodb
"""

from fastapi import FastAPI, Response
from pymongo import MongoClient
from xml.etree.ElementTree import Element, SubElement, tostring

app = FastAPI()

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["jp-property"]  # твоя база
collection = db["properties"]  # коллекция объявлений


@app.get("/feed", response_class=Response)
def get_feed():
    root = Element("real_estate_feed")

    # Достаём все объявления
    listings = list(collection.find({}))
    for item in listings:
        offer = SubElement(root, "offer")

        SubElement(offer, "title").text = str(item.get("title", ""))
        SubElement(offer, "url").text = str(item.get("url", ""))
        SubElement(offer, "price").text = str(item.get("price", ""))
        SubElement(offer, "description").text = str(item.get("description", ""))

        # Геолокация
        location = SubElement(offer, "location")
        SubElement(location, "lat").text = str(item.get("lat", ""))
        SubElement(location, "lon").text = str(item.get("lon", ""))

        # Картинки
        images_el = SubElement(offer, "images")
        for img in item.get("images", []):
            SubElement(images_el, "image").text = img

    # Генерим XML
    xml_data = tostring(root, encoding="utf-8")

    return Response(content=xml_data, media_type="application/xml")