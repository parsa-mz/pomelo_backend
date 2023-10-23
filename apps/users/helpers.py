from apps.users.models import User
from core.dependencies.database import database


class UserDAO:
    @staticmethod
    def get_user(user_id: int):
        query = User.select().where(User.c.id == user_id)
        result = database.execute(query).fetchone()
        return result

    @staticmethod
    def update_user(user_id: int, credit: float, payable: float):
        query = User.update().where(User.c.id == user_id).values(
            credit=credit, payable=payable)
        database.execute(query)
