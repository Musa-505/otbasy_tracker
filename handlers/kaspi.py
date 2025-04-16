from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from services.kaspi_api import get_kaspi_offers

router = Router()

@router.message(Command("kaspi"))
async def kaspi_handler(message: Message):
    text = get_kaspi_offers()  # Бұл енді str

    if not text:
        await message.answer("❌ Қателік! Мәліметтерді алу мүмкін болмады.")
        return

    # Telegram лимиті — 4096 символ
    max_length = 4096
    while len(text) > max_length:
        part = text[:max_length]
        await message.answer(part, parse_mode=ParseMode.HTML)
        text = text[max_length:]

    if text:
        await message.answer(text, parse_mode=ParseMode.HTML)