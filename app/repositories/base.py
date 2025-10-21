from fastapi.encoders import jsonable_encoder
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Any, List, Optional, Type, TypeVar, Generic

from app.models import User


ModelType = TypeVar('ModelType')


class CRUDBase(Generic[ModelType]):
    """Базовый CRUD-класс для работы с моделями SQLAlchemy."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получает объект по его ID.

        Args:
            obj_id: Идентификатор объекта.
            session: Асинхронная сессия для работы с базой данных.

        Returns:
            Найденный объект или None, если не найден.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id  # type: ignore
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        """Получает все объекты модели.

        Args:
            session: Асинхронная сессия для работы с базой данных.

        Returns:
            Список всех объектов модели.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        **kwargs: Any
    ) -> ModelType:
        """Создаёт новый объект в базе данных.

        Args:
            obj_in: Данные для создания объекта (Pydantic-модель).
            session: Асинхронная сессия для работы с базой данных.
            user: Пользователь, от имени которого создаётся объект
                (опционально, используется для установки user_id).
            **kwargs: Дополнительные поля для создания объекта.

        Returns:
            Созданный объект.
        """
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        obj_in_data.update(kwargs)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: ModelType,
        obj_in,
        session: AsyncSession,
    ) -> ModelType:
        """Обновляет существующий объект.

        Args:
            db_obj: Объект из базы данных для обновления.
            obj_in: Данные для обновления (Pydantic-модель).
            session: Асинхронная сессия для работы с базой данных.

        Returns:
            Обновлённый объект.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удаляет объект из базы данных.

        Args:
            db_obj: Объект из базы данных для удаления.
            session: Асинхронная сессия для работы с базой данных.

        Returns:
            Удалённый объект.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attributes(
        self,
        session: AsyncSession,
        **filters: Any,
    ) -> List[ModelType]:
        """Получить объекты по атрибутам модели.

        Args:
            session: Асинхронная сессия.
            **filters: Параметры фильтрации (поле=значение).

        Returns:
            List[ModelType]: Список найденных объектов.
        """
        query = select(self.model)
        for field, value in filters.items():
            query = query.where(getattr(self.model, field) == value)

        db_objs = await session.execute(query)
        return db_objs.scalars().all()

    async def get_one_by_attributes(
        self,
        session: AsyncSession,
        **filters: Any,
    ) -> Optional[ModelType]:
        """Получить один объект по атрибутам модели.

        Args:
            session: Асинхронная сессия.
            **filters: Параметры фильтрации (поле=значение).

        Returns:
            Optional[ModelType]: Найденный объект или None.
        """
        query = select(self.model)
        for field, value in filters.items():
            query = query.where(getattr(self.model, field) == value)

        db_obj = await session.execute(query)
        return db_obj.scalars().first()

    async def get_open_objects(
        self,
        session: AsyncSession,
    ) -> List[ModelType]:
        """Получить незакрытые объекты (для инвестирования).

        Args:
            session: Асинхронная сессия.

        Returns:
            List[ModelType]: Список незакрытых объектов.
        """
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(false())  # type: ignore
            ).order_by(
                self.model.create_date  # type: ignore
            )
        )
        return objects.scalars().all()
