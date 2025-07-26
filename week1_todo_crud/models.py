from pydantic import BaseModel, Field , EmailStr,model_validator
from typing import  Optional, Annotated
from fastapi import Query
from Utils import Utils, configs
import re 

class Task(BaseModel):
    id: int
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: Annotated[str, Field(min_length=1, max_length=200)]
    completed: bool = False

class FilterParams(BaseModel):
    skip: Annotated[int, Query(ge=0, description="Items to skip")] = 0
    limit: Annotated[int, Query(ge=1, le=100, description="Items to return")] = configs.DB_LEN
    order_by: Optional[str] = Query(None, pattern="^(asc|desc)$")

class SignupModel(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20)]
    password: Annotated[str, Field(min_length=6, max_length=20)]
    email: Annotated[EmailStr, Field(description="User's email address")]
    confirm_password: Annotated[str, Field(min_length=6, max_length=20)]

   
 
class LoginModel(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=20)
    password: Annotated[str, Field(min_length=6, max_length=20)]
    email: Optional[EmailStr] = None

    @model_validator(mode='after')
    def validate_login(self):
        if not self.username and not self.email:
            raise ValueError("Either username or email must be provided for login.")
        return self