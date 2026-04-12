from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categories import Category as CategoryModel
from app.schemas import Category as CategorySchema, CategoryCreate
from app.db_depends import get_async_db
from app.auth import get_admin


# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


async def get_active_category(category_id: int, db: AsyncSession) -> CategoryModel:
    """
    Проверка существования активной категории.
    """
    stmt = select(CategoryModel).where(CategoryModel.id == category_id,
                                       CategoryModel.is_active == True)
    category = await db.scalar(stmt)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found or inactive"
                            )
    return category


# Проверка существования parent_id
async def get_parent_id(parent_id: int, db: AsyncSession):
    """
    Проверка существования parent_id у категории.
    """
    stmt = select(CategoryModel).where(CategoryModel.id == parent_id,
                                       CategoryModel.is_active == True)
    parent = await db.scalar(stmt)
    if parent is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Parent category not found"
                            )


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных категорий.
    """
    stmt = select(CategoryModel).where(CategoryModel.is_active == True)
    result = await db.scalars(stmt)
    categories = result.all()
    return categories


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
        category: CategoryCreate,
        db: AsyncSession = Depends(get_async_db),
        _ = Depends(get_admin)
):
    """
    Создаёт новую категорию.
    """
    if category.parent_id is not None:
        await get_parent_id(category.parent_id, db)

    # Создание новой категории
    new_category = CategoryModel(**category.model_dump())
    db.add(new_category)
    await db.commit()
    return new_category


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
        category_id: int,
        category: CategoryCreate,
        db: AsyncSession = Depends(get_async_db),
        _ = Depends(get_admin)
):
    """
    Обновляет категорию по её ID.
    """
    db_category = await get_active_category(category_id, db)

    if category.parent_id is not None:
        await get_parent_id(category.parent_id, db)

    # Обновляем категорию
    update_data = category.model_dump(exclude_unset=True)
    await db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(**update_data)
    )
    await db.commit()
    return db_category


@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        db: AsyncSession = Depends(get_async_db),
        _ = Depends(get_admin)
):
    """
    Логически удаляет категорию по её ID.
    """
    category = await get_active_category(category_id, db)

    # Логическое удаление категории (установка is_active=False)
    category.is_active = False
    await db.commit()

    return category