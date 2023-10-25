from fastapi import APIRouter, Depends

from apps.users.models import User
from apps.users.schemas import UserSchema, UserCreateSchema
from core.dependencies.authenticate import auth_middleware
from core.dependencies.database import database
from core.dependencies.permission import IS_AUTHENTICATED, ALLOW_ANY
from core.utils import make_uid

router = APIRouter()


@router.get("/me", dependencies=[])
async def current_user_info(
        user=Depends(IS_AUTHENTICATED)
) -> UserSchema:
    """
    get current user
    """
    return UserSchema.serialize(user)


@router.post("/add", dependencies=[])
async def add_user(
        data: UserCreateSchema,
) -> dict:
    """
    add a new user
    """
    user_id = make_uid(5)
    query = User.insert().values(
        id=user_id,
        name=data.name,
        credit=1000.0,
        payable=0.0,
    )
    database.execute(query)
    # create jwt
    access_token = auth_middleware.generate_token({
        "user_id": user_id,
    })

    return {
        "access_token": access_token,
    }


@router.post("/get-token", dependencies=[])
def login(data: UserCreateSchema):
    try:
        query = User.select().where(User.c.name == data.name)
        result = database.execute(query).fetchall()

        access_token = auth_middleware.generate_token({"user_id": result[0].id,})
        return {
            "access_token": access_token,
        }
    except Exception as e:
        print(e)
        return {"message": "no user found!"}
