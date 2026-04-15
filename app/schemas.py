from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated
from decimal import Decimal
from datetime import datetime


class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="Название категории (3-50 символов)"
        )
    ]
    parent_id: Annotated[
        int | None,
        Field(
            default=None,
            description="ID родительской категории, если есть"
        )
    ]


class Category(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """
    id: Annotated[
        int,
        Field(
            description="Уникальный идентификатор категории"
        )
    ]
    name: Annotated[
        str,
        Field(
            description="Название категории"
        )
    ]
    parent_id: Annotated[
        int | None,
        Field(
            default=None,
            description="ID родительской категории, если есть"
        )
    ]
    is_active: Annotated[
        bool,
        Field(
            description="Активность категории"
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах.
    """
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100,
            description="Название товара (3-100 символов)"
        )
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            max_length=500,
            description="Описание товара (до 500 символов)"
        )
    ]
    price: Annotated[
        Decimal,
        Field(
            gt=0,
            decimal_places=2,
            description="Цена товара (больше 0)"
        )
    ]
    image_url: Annotated[
        str | None,
        Field(
            default=None,
            max_length=200,
            description="URL изображения товара"
        )
    ]
    stock: Annotated[
        int,
        Field(
            ge=0,
            description="Количество товара на складе (0 или больше)"
        )
    ]
    category_id: Annotated[
        int,
        Field(
            description="ID категории, к которой относится товар"
        )
    ]


class Product(BaseModel):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """
    id: Annotated[
        int,
        Field(
            description="Уникальный идентификатор товара"
        )
    ]
    name: Annotated[
        str,
        Field(
            description="Название товара"
        )
    ]
    description: Annotated[
        str | None,
        Field(
            default=None,
            description="Описание товара"
        )
    ]
    price: Annotated[
        Decimal,
        Field(
            gt=0,
            decimal_places=2,
            description="Цена товара в рублях"
        )
    ]
    image_url: Annotated[
        str | None,
        Field(
            default=None,
            description="URL изображения товара"
        )
    ]
    stock: Annotated[
        int,
        Field(
            description="Количество товара на складе"
        )
    ]
    category_id: Annotated[
        int,
        Field(
            description="ID категории"
        )
    ]
    is_active: Annotated[
        bool,
        Field(
            description="Активность товара"
        )
    ]
    rating: Annotated[
        float,
        Field(
            description='Рейтинг товара'
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """
    Список пагинации для товаров.
    """
    items: Annotated[
        list[Product],
        Field(
            description="Товары для текущей страницы"
        )
    ]
    total: Annotated[
        int,
        Field(
            ge=0,
            description="Общее количество товаров"
        )
    ]
    page: Annotated[
        int,
        Field(
            ge=1,
            description="Номер текущей страницы"
        )
    ]
    page_size: Annotated[
        int,
        Field(
            ge=1,
            description="Количество элементов на странице"
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    Модель для создания и обновления пользователя.
    Используется в POST и PUT запросах.
    """
    email: Annotated[
        EmailStr,
        Field(
            description="Email пользователя"
        )
    ]
    password: Annotated[
        str,
        Field(
            min_length=8,
            description="Пароль (минимум 8 символов)"
        )
    ]
    role: Annotated[
        str,
        Field(
            default="buyer",
            pattern="^(buyer|seller)$",
            description="Роль: 'buyer' или 'seller'"
        )
    ]


class User(BaseModel):
    """
    Модель для ответа с данными пользователя.
    Используется в GET-запросах.
    """
    id: Annotated[
        int,
        Field(
            description="Уникальный идентификатор пользователя"
        )
    ]
    email: Annotated[
        EmailStr,
        Field(description="email пользователя"
              )
    ]
    is_active: Annotated[
        bool,
        Field(
            description="Активность пользователя"
        )
    ]
    role: Annotated[
        str,
        Field(
            description="Роль пользователя"
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    """
    Модель для обновления access-токена и refresh-токена.
    Используется в POST запросе.
    """
    refresh_token: Annotated[
        str,
        Field(
            description="Refresh-токен для получения нового access-токена и refresh-токена"
        )
    ]


class ReviewCreate(BaseModel):
    product_id: Annotated[
        int,
        Field(
            description="ID товара"
        )
    ]
    comment: Annotated[
        str | None,
        Field(
            default=None,
            description="Текст отзыва"
        )
    ]
    grade: Annotated[
        int,
        Field(
            ge=1,
            le=5,
            description="Оценка товара"
        )
    ]


class Review(BaseModel):
    id: Annotated[
        int,
        Field(
            description="Уникальный идентификатор отзыва"
        )
    ]
    user_id: Annotated[
        int,
        Field(
            description="ID пользователя"
        )
    ]
    product_id: Annotated[
        int,
        Field(
            description="ID товара"
        )
    ]
    comment: Annotated[
        str | None,
        Field(
            default=None,
            description="Текст отзыва"
        )
    ]
    comment_date: Annotated[
        datetime,
        Field(
            description="Дата и время отзыва"
        )
    ]
    grade: Annotated[
        int,
        Field(
            description="Оценка товара"
        )
    ]
    is_active: Annotated[
        bool,
        Field(
            description="Активность товара"
        )
    ]

    model_config = ConfigDict(from_attributes=True)


class CartItemBase(BaseModel):
    """
    Базовая модель для корзины
    """
    product_id: int = Field(description="ID товара")
    quantity: int = Field(ge=1, description="Количество товара")


class CartItemCreate(CartItemBase):
    """Модель для добавления нового товара в корзину."""
    pass


class CartItemUpdate(BaseModel):
    """Модель для обновления количества товара в корзине."""
    quantity: int = Field(..., ge=1, description="Новое количество товара")


class CartItem(BaseModel):
    """Товар в корзине с данными продукта."""
    id: int = Field(..., description="ID позиции корзины")
    quantity: int = Field(..., ge=1, description="Количество товара")
    product: Product = Field(..., description="Информация о товаре")

    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    """Полная информация о корзине пользователя."""
    user_id: int = Field(..., description="ID пользователя")
    items: list[CartItem] = Field(default_factory=list, description="Содержимое корзины")
    total_quantity: int = Field(..., ge=0, description="Общее количество товаров")
    total_price: Decimal = Field(..., ge=0, description="Общая стоимость товаров")

    model_config = ConfigDict(from_attributes=True)


class OrderItem(BaseModel):
    """Описывает одну строку заказа"""
    id: int = Field(..., description="ID позиции заказа")
    product_id: int = Field(..., description="ID товара")
    quantity: int = Field(..., ge=1, description="Количество")
    unit_price: Decimal = Field(..., ge=0, description="Цена за единицу на момент покупки")
    total_price: Decimal = Field(..., ge=0, description="Сумма по позиции")
    product: Product | None = Field(None, description="Полная информация о товаре")

    model_config = ConfigDict(from_attributes=True)


class Order(BaseModel):
    """Полное представление заказа"""
    id: int = Field(..., description="ID заказа")
    user_id: int = Field(..., description="ID пользователя")
    status: str = Field(..., description="Текущий статус заказа")
    total_amount: Decimal = Field(..., ge=0, description="Общая стоимость")
    created_at: datetime = Field(..., description="Когда заказ был создан")
    updated_at: datetime = Field(..., description="Когда последний раз обновлялся")
    items: list[OrderItem] = Field(default_factory=list, description="Список позиций")

    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    """Обёртка для пагинированных списков заказов"""
    items: list[Order] = Field(..., description="Заказы на текущей странице")
    total: int = Field(ge=0, description="Общее количество заказов")
    page: int = Field(ge=1, description="Текущая страница")
    page_size: int = Field(ge=1, description="Размер страницы")

    model_config = ConfigDict(from_attributes=True)