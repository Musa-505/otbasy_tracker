import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from utils.config import TOKEN
from handlers.start import router as start_router
from handlers.kaspi import router as kaspi_router
from services.scheduler import send_kaspi_updates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(kaspi_router)

async def on_startup():
    logger.info("🚀 Kaspi Bot іске қосылды!")

async def main():
    dp.startup.register(on_startup)
    
    # Kaspi жаңартуды бөлек Task ретінде іске қосамыз
    asyncio.create_task(send_kaspi_updates(bot))
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("⚠️ Бот тоқтатылды!")