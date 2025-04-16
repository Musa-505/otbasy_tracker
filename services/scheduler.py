import asyncio
from aiogram import Bot
from services.kaspi_api import get_kaspi_offers
from services.storage import get_all_users

def format_offers(offers):
    text = "📄 Kaspi ұсыныстары:\n\n"
    for offer in offers:
        merchant = offer.get("merchantName", "Белгісіз сатушы")
        title = offer.get("title", "Атауы жоқ")
        price = offer.get("price", "Бағасы жоқ")
        text += f"💡 <b>{merchant}</b>\n📝 {title}\n💲 {price}₸\n\n"
    return text

async def send_kaspi_updates(bot: Bot):
    while True:
        offers = get_kaspi_offers()
        if not offers:
            await asyncio.sleep(3600)
            continue

        text = format_offers(offers)
        for chat_id in get_all_users():
            try:
                await bot.send_message(chat_id, text, parse_mode="HTML")
            except Exception as e:
                print(f"❌ Қате {chat_id}: {e}")

        await asyncio.sleep(3600)  # 1 сағат сайын