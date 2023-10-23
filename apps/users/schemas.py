from pydantic import BaseModel as BaseSchema


class UserSchema(BaseSchema):
    id: str
    name: str
    credit: float
    payable: float

    @classmethod
    def serialize(cls, item):
        return cls(
            id=item.id,
            name=item.name,
            credit=item.credit,
            payable=item.payable,
        )


class UserCreateSchema(BaseSchema):
    name: str
