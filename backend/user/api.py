from datetime import datetime, timezone

from ninja import Router
from ninja_jwt import schema
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import SlidingToken
from user.schemas import (CreateUserSchema, EnableDisableUserOutSchema,
                          EnableDisableUserSchema, UserTokenOutSchema)

router = Router()


@router.post(
"/user/create", response={201: UserTokenOutSchema}, url_name="user-create", auth=None
)
def create_user(request, user_schema: CreateUserSchema):
    """
    Create a new user and return a token.
    """
    user = user_schema.create()
    token = SlidingToken.for_user(user)
    return UserTokenOutSchema(
        user=user,
        token=str(token),
        token_exp_date=datetime.fromtimestamp(token["exp"], tz=timezone.utc),
    )


@router.delete(
    "/user/{int:pk}/delete",
    response=EnableDisableUserOutSchema,
    url_name="user-delete",
    auth=JWTAuth(),
)
def delete_user(request, pk: int):
    """
    Delete a user by ID.
    """
    user_schema = EnableDisableUserSchema(user_id=str(pk))
    user_schema.delete()
    return EnableDisableUserOutSchema(message="User deleted successfully")


@router.post("/user/login", response=UserTokenOutSchema, url_name="login")
def obtain_token(request, user_token: schema.TokenObtainSlidingInputSchema):
    """
    Obtain a token for a user.
    """
    user = user_token._user
    token = SlidingToken.for_user(user)
    return UserTokenOutSchema(
        user=user,
        token=str(token),
        token_exp_date=datetime.fromtimestamp(token["exp"], tz=timezone.utc),
    )


@router.post(
    "/auth/api-token-refresh",
    response=schema.TokenRefreshSlidingOutputSchema,
    url_name="refresh",
    tags=["auth"],
    
)
def refresh_token(request, refresh_token: schema.TokenRefreshSlidingInputSchema):
    """
    Refresh an existing token.
    """
    refresh = schema.TokenRefreshSlidingOutputSchema(**refresh_token.dict())
    return refresh