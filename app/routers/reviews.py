from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_async_db
from app.auth import get_current_buyer


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)


async def update_product_rating(product_id: int, db: AsyncSession):
    """
    Пересчёт рейтинга товара.
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating


async def get_active_product(product_id: int, db: AsyncSession):
    """
    Проверка наличия активного товара.
    """
    stmt = select(ProductModel).where(ProductModel.id == product_id,
                                      ProductModel.is_active == True)
    product = await db.scalar(stmt)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found or inactive")

    return product


@router.get("/", response_model=list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех активных отзывов.
    """
    stmt = select(ReviewModel).where(ReviewModel.is_active == True)
    result = await db.scalars(stmt)
    reviews = result.all()

    return reviews


@router.get("/products/{product_id}", response_model= list[ReviewSchema], status_code=status.HTTP_200_OK)
async def get_review_by_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Получение всех активных отзывов о товаре.
    """
    await get_active_product(product_id, db)

    # Получение списка отзывов о товаре
    stmt = select(ReviewModel).where(ReviewModel.product_id == product_id,
                                     ReviewModel.is_active == True)
    result = await db.scalars(stmt)
    reviews_by_product = result.all()

    return reviews_by_product


@router.post("/", response_model= ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
        review: ReviewCreate,
        db: AsyncSession = Depends(get_async_db),
        current_user: UserModel = Depends(get_current_buyer)
):
    """
    Создание нового отзыва о товаре.
    """
    product = await get_active_product(review.product_id, db)

    # Создание нового отзыва
    new_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(new_review)

    # Пересчёт рейтинга товара
    await update_product_rating(product.id, db)
    await db.commit()
    await db.refresh(new_review)

    return new_review


@router.delete("/{review_id}")
async def delete_review(
        review_id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: UserModel = Depends(get_current_buyer)
):
    """
    Удаление отзыва о товаре
    """
    # Проверка наличия активного отзыва
    stmt = select(ReviewModel).where(ReviewModel.id == review_id,
                                     ReviewModel.is_active == True)
    review = await db.scalar(stmt)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Review not found or inactive")

    # Проверка авторства отзыва
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not allowed to delete this review")

    # Логическое удаление товара (установка is_active=False)
    review.is_active = False

    # Пересчёт рейтинга товара
    await update_product_rating(review.product_id, db)
    await db.commit()
    await db.refresh(review)

    return {"message": "Review deleted"}