# helpers.py
from typing import Dict

from apps.transations.model import PendingTransaction, SettledTransaction
from core.dependencies.database import database


class TransactionDAO:
    @staticmethod
    def get_pending_txns(user_id: str) -> Dict:
        query = PendingTransaction.select().where(PendingTransaction.c.user_id == user_id)
        result = database.execute(query).fetchall()
        return {item.id: {
            "amount": item.amount,
            "time": item.time
        } for item in result}

    @staticmethod
    def get_settled_txns(user_id: str) -> Dict:
        query = SettledTransaction.select().where(SettledTransaction.c.user_id == user_id)
        result = database.execute(query).fetchall()

        for item in result:
            print(item)

        return {item.id: {
            "amount": item.amount,
            "initial_time": item.initial_time,
            "final_time": item.final_time
        } for item in result}

    @staticmethod
    def save_pending_txn(user_id: str, txn_id: str, amount: float, time: str):
        query = PendingTransaction.insert().values(
            id=txn_id, amount=amount, time=time, user_id=user_id)
        database.execute(query)

    @staticmethod
    def save_settled_txn(user_id: str, txn_id: str, amount: float, initial_time: str, final_time: str):
        query = SettledTransaction.insert().values(
            id=txn_id, amount=amount, initial_time=initial_time, final_time=final_time, user_id=user_id)
        database.execute(query)

    @staticmethod
    def clear_pending_txns(user_id: str):
        query = PendingTransaction.delete().where(PendingTransaction.c.user_id == user_id)
        database.execute(query)

    @staticmethod
    def clear_settled_txns(user_id: str):
        query = SettledTransaction.delete().where(SettledTransaction.c.user_id == user_id)
        database.execute(query)
