from functools import cached_property

from pydantic import BaseModel, Field, computed_field, PostgresDsn


class DBSettings(BaseModel):
    username: str
    password: str
    host: str
    port: int
    path: str = Field(..., alias="db_name")

    @computed_field
    @cached_property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql", **self.model_dump(exclude={"dsn"})
        )
