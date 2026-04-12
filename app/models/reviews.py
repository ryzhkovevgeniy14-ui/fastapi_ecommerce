from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.database import Base



class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(default=datetime.now)
    grade: Mapped[int]
    is_active: Mapped[bool] = mapped_column(default=True)

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="reviews"
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews"
    )