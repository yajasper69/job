import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from datetime import datetime
from services import CatalogService, OrderService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, token: str):
        if not isinstance(token, str):
            raise TypeError("Bot token must be string")
        self.bot = Bot(token=token, parse_mode=ParseMode.HTML)
        self.dp = Dispatcher()
        self.catalog = CatalogService()
        self.orders = OrderService()

        # Регистрация обработчиков
        self.dp.message(CommandStart())(self._cmd_start)
        self.dp.message()(self._handle_web_app_data)

    @staticmethod
    async def _cmd_start(message: types.Message) -> None:
        """Обработка команды /start"""
        welcome_text = """
<b>Что умеет этот бот?</b>
Я помогу тебе попасть в мир райского наслаждения...
        """

        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Выбрать модель 🛍️",
            web_app=WebAppInfo(url="http://localhost:63342/PythonProject/bot/html.html?_ijt=9emn3fui1udf22pha55unh0887&_ij_reload=RELOAD_ON_SAVE")
        ))
        builder.row(types.InlineKeyboardButton(
            text="Start",
            callback_data="start_registered"
        ))

        await message.answer(welcome_text)
        await message.answer(
            "Нажмите кнопку ниже:",
            reply_markup=builder.as_markup()
        )

    async def _handle_web_app_data(self, message: types.Message) -> None:
        """Обработка данных из Mini App"""
        try:
            data = json.loads(message.web_app_data.data)

            if data['action'] == 'place_order':
                order = await self.orders.create_order(
                    user_id=str(message.from_user.id),  # Явное преобразование в string
                    product_id=str(data['product_id']),  # Явное преобразование
                    hours=int(data['hours'])  # Явное преобразование
                )

                # Теперь заказ автоматически сохраняется в OrderService
                logger.info(f"New order created: {order['order_id']}")

                await message.answer(f"Заказ #{order['order_id']} создан!")

                # Уведомление покупателю
                await message.answer(
                    f"<b>Заявка создана!</b>\n"
                    f"Модель: {order['product_name']}\n"
                    f"Часы: {order['hours']}\n"
                    f"Стоимость: {order['total']} руб\n"
                    f"Дата: {order['date']}"
                )

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            await message.answer("Ошибка в данных заказа")
        except Exception as e:
            logger.error(f"WebApp error: {e}")
            await message.answer("Ошибка обработки запроса")

    async def run(self) -> None:
        """Запуск бота"""
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    bot = TelegramBot("8023704901:AAH_NYoPrWjdl512dlerr69LSFh15iZlvGw")
    asyncio.run(bot.run())