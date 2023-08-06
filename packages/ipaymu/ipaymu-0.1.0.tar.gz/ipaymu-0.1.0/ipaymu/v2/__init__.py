import json

import requests

from ..helper import get_url
from .utils import create_headers, create_signature


def direct_payment(
    name,
    phone,
    email,
    amount,
    notifyUrl,
    expired,
    expiredType,
    paymentMethod,
    paymentChannel,
    product=None,
    qty=None,
    price=None,
    weight=None,
    width=None,
    height=None,
    length=None,
    deliveryArea=None,
    deliveryAddress=None,
    comments=None,
):
    url = get_url("/api/v2/payment/direct")
    body = {
        "name": name,
        "phone": phone,
        "email": email,
        "amount": amount,
        "notifyUrl": notifyUrl,
        "expired": expired,
        "expiredType": expiredType,
        "paymentMethod": paymentMethod,
        "paymentChannel": paymentChannel,
    }
    if comments:
        body["comments"] = comments

    if paymentMethod == "cod":
        body["product[]"] = product
        body["qty[]"] = qty
        body["price[]"] = price
        body["weight[]"] = weight
        body["width[]"] = width
        body["height[]"] = height
        body["length[]"] = length
        body["deliveryArea"] = deliveryArea
        body["deliveryAddress"] = deliveryAddress

    data_body = json.dumps(body, separators=(",", ":"))
    signature = create_signature(data_body)
    headers = create_headers(signature)
    resp = requests.post(url, data=data_body, headers=headers).json()
    return resp


def redirect_payment(
    product,
    qty,
    price,
    description,
    returnUrl,
    notifyUrl,
    cancelUrl,
    weight=None,
    dimension=None,
    buyerName=None,
    buyerPhone=None,
    buyerEmail=None,
    paymentMethod=None,
    pickupArea=None,
    pickupAddress=None,
):
    url = get_url("/api/v2/payment")
    body = {
        "product[]": product,
        "qty[]": qty,
        "price[]": price,
        "description[]": description,
        "returnUrl": returnUrl,
        "notifyUrl": notifyUrl,
        "cancelUrl": cancelUrl,
    }
    if weight:
        body["weight[]"] = weight
    if dimension:
        body["dimension[]"] = dimension
    if buyerName:
        body["buyerName"] = buyerName
    if buyerPhone:
        body["buyerPhone"] = buyerPhone
    if buyerEmail:
        body["buyerEmail"] = buyerEmail

    if paymentMethod == "cod":
        if pickupArea:
            body["pickupArea"] = pickupArea
        if pickupAddress:
            body["pickupAddress"] = pickupAddress

    data_body = json.dumps(body, separators=(",", ":"))
    signature = create_signature(data_body)
    headers = create_headers(signature)
    resp = requests.post(url, data=data_body, headers=headers).json()
    return resp
