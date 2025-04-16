from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.storage import save_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    save_user(message.chat.id)
    await message.answer("Сәлем 👋\nKaspi ұсыныстарын көру үшін /kaspi деп жазыңыз.")