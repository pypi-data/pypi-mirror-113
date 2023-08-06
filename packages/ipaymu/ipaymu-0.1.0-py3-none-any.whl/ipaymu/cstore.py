import functools

import requests

from .helper import get_data, get_url


def cstore_payment(channel, name, phone, email, amount, unotify, active, expired_type):
    url = get_url("/api/payment/cstore")
    data = get_data(False)
    data["channel"] = channel
    data["name"] = name
    data["phone"] = phone
    data["email"] = email
    data["amount"] = amount
    data["unotify"] = unotify
    data["active"] = active
    data["expired_type"] = expired_type
    resp = requests.post(url, data=data).json()
    return resp


indomaret_payment = functools.partial(cstore_payment, "indomaret")
alfamart_payment = functools.partial(cstore_payment, "alfamart")
