from database import new_session, KeysOrm
from sqlalchemy import select

from schemas import SKeyAdd, SKey


class KeyRepository:
    @classmethod
    async def add_one(cls, data: SKeyAdd) -> int:
        async with new_session() as session:
            key_dict = data.model_dump()

            key = KeysOrm(**key_dict)
            session.add(key)
            await session.flush()
            await session.commit()
            return key.id

    @classmethod
    async def find_all(cls) -> [SKey]:
        async with new_session() as session:
            query = select(KeysOrm)
            result = await session.execute(query)
            key_models = result.scalars().all()
            # Преобразование экземпляров KeysOrm в словари
            key_dicts = [key_model.__dict__ for key_model in key_models]
            # Использование словарей для создания экземпляров SKey
            key_schemas = [SKey.model_validate(key_dict) for key_dict in key_dicts]
            return key_schemas
