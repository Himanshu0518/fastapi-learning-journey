from fastapi import  Query
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from pydantic import BaseModel

class HeroFilter(BaseModel):
    order: Annotated[str, Query(default="asc", description="Order of results: 'asc' or 'desc'",pattern="^(asc|desc)$")] = "asc"
    order_by : Annotated[str, Query(default="id" , description="Column to sort by", pattern="^(id|name|power|age)$")]
    skip:Annotated[int, Query(ge=0, description="Items to skip")] = 0 
    limit:Annotated[int, Query(ge=1, le=100, description="Items to return")] = 10 

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    power : Annotated[int, Field(default=0, description="Hero's power")] 

class Hero(HeroBase, table=True):
    """
    This model is for how we store the hero in the database.
    It includes the fields that are required to store a hero.
    table =True means that this model is a table in the database.
    """
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    """
     This model is for how  we show the hero to the user.
     It does not include the secret_name field.
    """
    id: int 

class HeroCreate(HeroBase):
    """
   This model is structure for what to ask from the user when creating a new hero.
   It includes the fields that are required to create a new hero.
    """
    secret_name: str


class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    power: int | None = None 
