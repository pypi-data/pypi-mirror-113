import functools

import requests

from .helper import get_data, get_url


def va_payment(
    url, customer_name, customer_email, customer_phone, price, notify_url, expired
):
    url = get_url(url)
    data = get_data(False)
    data["customer_name"] = customer_name
    data["customer_email"] = customer_email
    data["customer_phone"] = customer_phone
    data["price"] = price
    data["notify_url"] = notify_url
    data["expired"] = expired
    resp = requests.post(url, data=data).json()
    return resp


va_cimb_niaga = functools.partial(va_payment, "/api/getva")

va_bni = functools.partial(va_payment, "/api/getbniva")

va_bag = functools.partial(va_payment, "/api/getbagva")

va_mandiri = functools.partial(va_payment, "/api/getmandiriva")
