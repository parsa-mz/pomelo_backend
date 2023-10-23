#!/bin/python3

import math
import os
import random
import re
import sys


def summarize(inputJSON):
    """

    When
        Txn_Auth -> get from credit
        Txn_cleared -> give credit back
        Txn_settled -> remove temp hold + get the new amount + update payable
        payment_init -> update payable
        payment_cancelled -> update payable
        payment_posted -> give back credit (already update payable on payment_init)
    """

    input_data = eval(inputJSON)
    available_credit = input_data["creditLimit"]
    payable_balance = 0

    pending_txns = {}
    settled_txns = {}

    for event in input_data["events"]:
        event_type = event["eventType"]
        txn_id = event["txnId"]
        event_time = event["eventTime"]

        if event_type == 'TXN_AUTHED':
            amount = event["amount"]
            pending_txns[txn_id] = {
                "amount": amount,
                "time": event_time
            }
            # subtract from credit
            available_credit -= amount

        elif event_type == 'TXN_AUTH_CLEARED':
            if txn_id in pending_txns:
                available_credit += pending_txns[txn_id]['amount']
                del pending_txns[txn_id]

        elif event_type == 'TXN_SETTLED':
            if txn_id in pending_txns:
                settled_txns[txn_id] = {
                    "amount": event["amount"],
                    "initial_time": pending_txns[txn_id]["time"],
                    "final_time": event_time
                }
                # return the original amount
                available_credit += pending_txns[txn_id]['amount']
                # subtract the new amount
                available_credit -= event['amount']
                payable_balance += event['amount']

                del pending_txns[txn_id]

        elif event_type == 'PAYMENT_INITIATED':
            amount = event["amount"]
            pending_txns[txn_id] = {
                "amount": amount,
                "time": event_time
            }
            # when temp payment -> update payable
            payable_balance += amount

        elif event_type == 'PAYMENT_CANCELED':
            if txn_id in pending_txns:
                payable_balance -= pending_txns[txn_id]['amount']
                del pending_txns[txn_id]

        elif event_type == 'PAYMENT_POSTED':
            if txn_id in pending_txns:
                settled_txns[txn_id] = {
                    # we have to get the amount from init_payment
                    "amount": pending_txns[txn_id]['amount'],
                    "initial_time": pending_txns[txn_id]["time"],
                    "final_time": event_time
                }
                # return credit back
                available_credit -= pending_txns[txn_id]['amount']
                del pending_txns[txn_id]

    sorted_settled_txns = sorted(settled_txns.items(), key=lambda x: x[1]['final_time'], reverse=True)

    output = f"Available credit: ${available_credit}\n"
    output += f"Payable balance: ${payable_balance}\n\n"

    output += "Pending transactions:\n"
    for txn_id, txn_data in pending_txns.items():
        amount = txn_data['amount']
        str_amount = f"${amount}" if txn_data['amount'] >= 0 else f"-${abs(amount)}"
        output += f"{txn_id}: {str_amount} @ time {txn_data['time']}\n"

    output += "\nSettled transactions:\n"
    for txn_id, txn_data in sorted_settled_txns:
        amount = txn_data['amount']
        str_amount = f"${amount}" if amount >= 0 else f"-${abs(amount)}"
        output += f"{txn_id}: {str_amount} @ time {txn_data['initial_time']} (finalized @ time {txn_data['final_time']})\n"

    return output.strip()


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    inputJSON = input()

    result = summarize(inputJSON)

    fptr.write(result + '\n')

    fptr.close()
