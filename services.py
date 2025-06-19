from datetime import datetime
from typing import Dict, Any


class CatalogService:
    def __init__(self):
        self.products: Dict[str, Dict[str, Any]] = {
            "1": {
                "name": "Анна",
                "age": 23,
                "height": 168,
                "weight": 55,
                "chest": 3,
                "price": 5000,
                "description": "Привет, я Анна! Люблю активный отдых и длительные прогулки. Открыта к новым знакомствам и общению.",
                "photos": [
                    "https://i.pinimg.com/736x/40/eb/e0/40ebe0b9e8d1046f173eb26a61009d81.jpg",
                    "https://i.pinimg.com/736x/d5/46/5f/d5465facf810f00a584037d6d951121d.jpg",
                    "https://i.pinimg.com/564x/ac/0d/10/ac0d1064bcc926541bf8941c7a069c6b.jpg"
                ],
                "hours_available": [1, 2, 4, 6, 12],
                "seller_id": "@ya_jaspers"  # ID продавца в Telegram
            },
            "2": {
                "name": "Мария",
                "age": 25,
                "height": 172,
                "weight": 58,
                "chest": 2,
                "price": 6000,
                "description": "Меня зовут Мария. Я творческая личность, люблю искусство и музыку. Всегда рада новым впечатлениям.",
                "photos": [
                    "https://i.pinimg.com/474x/1e/00/97/1e0097a81c088c49c32d6fa3c4018b32.jpg",
                    "https://i.pinimg.com/736x/77/d3/38/77d33805d0708b4de31bc80ec7da9a49.jpg"
                ],
                "hours_available": [1, 2, 4, 8],
                "seller_id": "@ya_jaspers"  # ID продавца в Telegram
            }
        }


    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Получение товара по ID"""
        return self.products.get(str(product_id))  # Явное преобразование


class OrderService:
    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}


    @staticmethod  # Добавлен декоратор staticmethod
    def _validate_order_data(hours: int, product: Dict[str, Any]) -> None:
        """Валидация данных заказа"""
        if not isinstance(hours, int) or hours <= 0:
            raise ValueError("Hours must be positive integer")
        if not product:
            raise ValueError("Product not found")


    async def create_order(self, user_id: str, product_id: str, hours: int) -> Dict[str, Any]:
        """Создание заказа"""
        product = CatalogService().get_product(str(product_id))
        self._validate_order_data(hours, product)  # Вынесена валидация

        order = {
            "order_id": f"order_{datetime.now().timestamp()}",
            "product_name": product['name'],
            "hours": hours,
            "total": product['price'] * hours,
            "date": datetime.now().strftime("%Y.%m.%d"),
            "seller_id": str(product['seller_id']),
            "user_id": str(user_id)
        }

        self.orders[order['order_id']] = order  # Сохраняем заказ
        return order