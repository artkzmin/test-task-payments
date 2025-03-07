from pydantic import BaseModel
from src.database import BaseOrm
from typing import TypeVar


DBModelType = TypeVar("DBModelType", bound=BaseOrm)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, db_model):
        return cls.schema.model_validate(db_model, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(data.model_dump())
