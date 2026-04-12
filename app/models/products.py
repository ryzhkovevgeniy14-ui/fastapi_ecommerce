from sqlalchemy import ForeignKey, String, Numeric, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from decimal import Decimal

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] = mapped_column(String(200))
    stock: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[float] = mapped_column(Float, default=0.0, server_default="0")

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products"
    )
    seller: Mapped["User"] = relationship(
        "User",
        back_populates="products"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="product"
    )