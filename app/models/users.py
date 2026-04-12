from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(String, default="buyer")

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="seller"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user"
    )