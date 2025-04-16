import requests
import re
import json
import os

def extract_product_id(url: str) -> str | None:
    match = re.search(r'-(\d+)/?\?c=', url)
    if match:
        return match.group(1)
    return None

def get_kaspi_offers_for_product(product_id, referer_url):
    url = f"https://kaspi.kz/yml/offer-view/offers/{product_id}"
    headers = {
        "Accept": "application/json, text/*",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://kaspi.kz",
        "Referer": referer_url,
        "User-Agent": "Mozilla/5.0",
        "x-ks-city": "750000000"
    }

    payload = {
        "cityId": "750000000",
        "id": product_id,
        "merchantUID": [],
        "page": 0,
        "product": {
            "brand": "Отбасы хрестоматиясы",
            "categoryCodes": ["Self-help literature", "Books", "Leisure", "Categories"],
            "baseProductCodes": [],
            "groups": None
        },
        "sortOption": "PRICE",
        "highRating": None,
        "searchText": None,
        "zoneId": ["Magnum_ZONE1"],
        "installationId": "-1"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("offers", [])
    return []

def get_kaspi_offers(file_path=None) -> str:
    if file_path is None:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "..", "data", "booksUrl.json")

    with open(file_path, "r", encoding="utf-8") as f:
        urls = json.load(f)

    all_text = ""
    for url in urls:
        product_id = extract_product_id(url)
        if not product_id:
            all_text += f"❌ ID табылмады: {url}\n\n"
            continue

        offers = get_kaspi_offers_for_product(product_id, url)
        otbasy_offer = next((offer for offer in offers if offer.get("merchantName") == "ОТБАСЫ БАСПА ҮЙІ"), None)

        if not otbasy_offer:
            all_text += f"📘 ⚠️ Атауы анықталмады\n🔗 {url}\n⚠️ ОТБАСЫ БАСПА ҮЙІ сатушысы табылмады.\n\n"
            continue

        title = otbasy_offer.get("title", "Атауы жоқ")
        otbasy_price = otbasy_offer.get("price")

        cheaper_offers = [
            offer for offer in offers
            if offer.get("price", float('inf')) < otbasy_price
        ]

        all_text += f"📘 <b>{title}</b>\n🔗 {url}\n"
        all_text += f"🏷️ ОТБАСЫ БАСПА ҮЙІ бағасы: <b>{otbasy_price}₸</b>\n"

        if cheaper_offers:
            all_text += f"🔽 Арзан сатушылар:\n"
            for offer in cheaper_offers:
                all_text += f"💡 {offer.get('merchantName')}\n💲 {offer.get('price')}₸\n"
        else:
            all_text += "✅ Ешкім арзан сатып жатқан жоқ.\n"
        all_text += "\n"

    return all_text if all_text else "❌ Ешқандай нәтиже табылмады."