from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel, PositiveInt
from humps.camel import case

MODEL_TYEP = TypeVar('MODEL_TYEP')

# __all__ = ["PagingParams", "PagingResult", "CamelModel"]


class CamelModel(BaseModel):
    #自动加上下划线转驼峰的别名
    class Config:
        allow_population_by_field_name = True
        alias_generator = case
        use_enum_values = True

    def populate_model(self, model: Type[MODEL_TYEP]) -> MODEL_TYEP:
        data = self.dict(include={c.name for c in model.__table__.columns})
        return model(**data)


class PagingParams(CamelModel):
    offset: PositiveInt
    limit: PositiveInt

    class Config:
        allow_population_by_field_name = True

    def populate_result(self, total: int, items: list[Any], **kwargs) -> 'PagingResult':
        return PagingResult(page=self.offset, per_page=self.limit, total=total, items=items, **kwargs)

    @property
    def skip(self):
        return (self.page - 1) * self.per_page


class PagingResult(PagingParams):
    total: int
    items: list[Any]
