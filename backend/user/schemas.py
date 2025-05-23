from datetime import datetime
from typing import List, Optional, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from ninja_schema import ModelSchema, Schema
from pydantic import field_validator

UserModel = get_user_model()


class GroupSchema(Schema):
    class Config:
        model = Group
        include = ("name",)


class CreateUserSchema(ModelSchema):
    class Config:
        model = UserModel
        include = (
            "email",
            "username",
            "is_staff",
            "is_superuser",
            "password",
        )
    @field_validator("username")
    def validate_name(cls, value_data):
        if UserModel.objects.filter(username__icontains=value_data).exists():
            raise ValidationError("Username already exist", code=400)
        return value_data
    def create(self) -> Type[AbstractUser]:
        return UserModel.objects.create_user(**self.dict())





class UserRetrieveSchema(Schema):
    groups: List[GroupSchema]

    class Config:
        model = UserModel
        include = ("email", "first_name", "last_name", "username", "id", "is_active")


class UserTokenOutSchema(Schema):
    token: str
    user: UserRetrieveSchema
    token_exp_date: Optional[datetime]


class EnableDisableUserSchema(Schema):
    user_id: str
    _user = None

    @field_validator(
        "user_id",
    )
    def validate_user_id(cls, value):
        user = UserModel.objects.filter(id=value).first()
        if user:
            cls._user = user
            return value
        raise ValueError("Invalid User Id")

    def update(self):
        self._user.is_active = not self._user.is_active
        self._user.save()
        return self._user

    def delete(self):
        _id = self._user.pk
        self._user.delete()
        return _id


class EnableDisableUserOutSchema(Schema):
    message: str
