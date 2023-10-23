from fastapi import APIRouter, Depends

from apps.transations.helpers import TransactionDAO
from apps.transations.model import PendingTransaction, SettledTransaction
from apps.transations.schemas import EventSchema, InputData
from apps.users.helpers import UserDAO
from apps.users.models import User
from core.dependencies.database import database
from fastapi import APIRouter

from core.dependencies.database import database
from core.dependencies.permission import IS_AUTHENTICATED

router = APIRouter()


@router.get("/all/")
def get_all():
    st_query = SettledTransaction.select()
    st_result = database.execute(st_query).fetchall()

    pt_query = PendingTransaction.select()
    pt_result = database.execute(pt_query).fetchall()

    return {"settled_transactions": st_result, "pending_transactions": pt_result}


def handle_txn_authed(event, pending_txns, settled_txns, available_credit, payable_balance):
    amount = event.amount
    pending_txns[event.txnId] = {
        "amount": amount,
        "time": event.eventTime
    }
    available_credit[0] -= amount


def handle_txn_auth_cleared(event, pending_txns, settled_txns, available_credit, payable_balance):
    if event.txnId in pending_txns:
        available_credit[0] += pending_txns[event.txnId]['amount']
        del pending_txns[event.txnId]


def handle_txn_settled(event, pending_txns, settled_txns, available_credit, payable_balance):
    if event.txnId in pending_txns:
        settled_txns[event.txnId] = {
            "amount": event.amount,
            "initial_time": pending_txns[event.txnId]["time"],
            "final_time": event.eventTime
        }
        available_credit[0] += pending_txns[event.txnId]['amount']
        available_credit[0] -= event.amount
        payable_balance[0] += event.amount

        del pending_txns[event.txnId]


def handle_payment_initiated(event, pending_txns, settled_txns, available_credit, payable_balance):
    amount = event.amount
    pending_txns[event.txnId] = {
        "amount": amount,
        "time": event.eventTime
    }
    payable_balance[0] += amount


def handle_payment_canceled(event, pending_txns, settled_txns, available_credit, payable_balance):
    if event.txnId in pending_txns:
        payable_balance[0] -= pending_txns[event.txnId]['amount']
        del pending_txns[event.txnId]


def handle_payment_posted(event, pending_txns, settled_txns, available_credit, payable_balance):
    if event.txnId in pending_txns:
        settled_txns[event.txnId] = {
            "amount": pending_txns[event.txnId]['amount'],
            "initial_time": pending_txns[event.txnId]["time"],
            "final_time": event.eventTime
        }
        available_credit[0] -= pending_txns[event.txnId]['amount']
        del pending_txns[event.txnId]


EVENT_TYPES = {
    "TXN_AUTHED": handle_txn_authed,
    "TXN_AUTH_CLEARED": handle_txn_auth_cleared,
    "TXN_SETTLED": handle_txn_settled,
    "PAYMENT_INITIATED": handle_payment_initiated,
    "PAYMENT_CANCELED": handle_payment_canceled,
    "PAYMENT_POSTED": handle_payment_posted
}


@router.post("/summarize")
def summarize_events(
        input_data: InputData,
        user: User = Depends(IS_AUTHENTICATED)
):
    # The reason we use list here is because we want to pass by reference (no need to return)
    # Our simple but yet effective way to pass by reference in Python
    available_credit = [1000]
    payable_balance = [0]

    pending_txns = TransactionDAO.get_pending_txns(user.id)
    settled_txns = TransactionDAO.get_settled_txns(user.id)

    for event in input_data.events:
        handler = EVENT_TYPES.get(event.eventType)
        if handler:
            handler(event, pending_txns, settled_txns, available_credit, payable_balance)

    # Sort settled transactions
    sorted_settled_txns = sorted(settled_txns.items(), key=lambda x: x[1]['final_time'], reverse=True)

    for txn_id, item in pending_txns.items():
        TransactionDAO.save_pending_txn(user.id, txn_id, item['amount'], item['time'])

    for txn_id, item in sorted_settled_txns:
        TransactionDAO.save_settled_txn(user.id, txn_id, item['amount'], item['initial_time'], item['final_time'])

    # update user credit and payable
    UserDAO.update_user(user.id, available_credit[0], payable_balance[0])

    pending_output = []
    for txn_id, txn_data in pending_txns.items():
        amount = txn_data['amount']
        str_amount = f"${amount}" if txn_data['amount'] >= 0 else f"-${abs(amount)}"
        pending_output.append(f"{txn_id}: {str_amount} @ time {txn_data['time']}")

    settled_output = []
    for txn_id, txn_data in sorted_settled_txns:
        amount = txn_data['amount']
        str_amount = f"${amount}" if amount >= 0 else f"-${abs(amount)}"
        settled_output.append(
            f"{txn_id}: {str_amount} @ time {txn_data['initial_time']} (finalized @ time {txn_data['final_time']})")

    return {
        "available_credit": available_credit[0],
        "payable_balance": payable_balance[0],
        "pending_txns": pending_output,
        "settled_txns": settled_output
    }


@router.post("/clear")
def clear_events(
        user: User = Depends(IS_AUTHENTICATED)
):

    TransactionDAO.clear_pending_txns(user.id)
    TransactionDAO.clear_settled_txns(user.id)

    return {"status": "success"}