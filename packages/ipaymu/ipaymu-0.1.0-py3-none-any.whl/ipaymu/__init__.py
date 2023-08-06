import os

import requests

from . import v2  # noqa
from .bank import transfer_bca  # noqa
from .cod import (  # noqa
    cod_check_shipping_fee,
    cod_get_area,
    cod_payment,
    cod_request_sid,
)
from .compat import settings
from .cstore import alfamart_payment, indomaret_payment  # noqa
from .helper import get_data, get_url
from .va import va_bag, va_bni, va_cimb_niaga, va_mandiri  # noqa

__version__ = "0.1.0"


def init(url=None, va_account=None, api_key=None):
    url = url or os.environ.get("IPAYMU_URL")
    va_account = va_account or os.environ.get("IPAYMU_VA_ACCOUNT")
    api_key = api_key or os.environ.get("IPAYMU_API_KEY")
    if url:
        settings.IPAYMU_URL = url
    if va_account:
        settings.IPAYMU_VA_ACCOUNT = va_account
    if api_key:
        settings.IPAYMU_API_KEY = api_key


def cek_saldo():
    url = get_url("/api/saldo")
    data = get_data()
    resp = requests.post(url, data=data).json()
    return resp


def cek_transaksi(id):
    url = get_url("/api/transaksi")
    data = get_data()
    data["id"] = id
    resp = requests.post(url, data=data).json()
    return resp


def qris(name, phone, email, amount, notifyUrl, zipCode, city):
    url = get_url("/api/payment/qris")
    data = get_data(False)
    data["name"] = name
    data["phone"] = phone
    data["email"] = email
    data["amount"] = amount
    data["notifyUrl"] = notifyUrl
    data["zipCode"] = zipCode
    data["city"] = city
    resp = requests.post(url, data=data).json()
    return resp


def akulaku(name, phone, email, amount, notifyUrl):
    url = get_url("/api/payment/akulaku")
    data = get_data(False)
    data["name"] = name
    data["phone"] = phone
    data["email"] = email
    data["amount"] = amount
    data["notifyUrl"] = notifyUrl
    resp = requests.post(url, data=data).json()
    return resp


def redirect_payment(
    product,
    price,
    quantity,
    comments,
    ureturn,
    unotify,
    ucancel,
    pay_method,
    pay_channel=None,
    buyer_name=None,
    buyer_phone=None,
    buyer_email=None,
    weight=None,
    dimensi=None,
    postal_code=None,
    address=None,
    cod_province=None,
    cod_city=None,
    auto_redirect=None,
    expired=None,
):
    url = get_url("/payment")
    data = get_data()
    data["action"] = "payment"
    data["product[]"] = product
    data["price[]"] = price
    data["quantity[]"] = quantity
    data["comments[]"] = comments
    data["ureturn"] = ureturn
    data["unotify"] = unotify
    data["ucancel"] = ucancel
    data["pay_method"] = pay_method
    if pay_method == "cstore" and pay_channel:
        data["pay_channel"] = pay_channel

    if buyer_name:
        data["buyer_name"] = buyer_name
    if buyer_phone:
        data["buyer_phone"] = buyer_phone
    if buyer_email:
        data["buyer_email"] = buyer_email
    if auto_redirect:
        data["auto_redirect"] = auto_redirect
    if expired:
        data["expired"] = expired
    if pay_method == "cod":
        if weight:
            data["weight"] = weight
        if dimensi:
            data["dimensi"] = dimensi
        if postal_code:
            data["postal_code"] = postal_code
        if address:
            data["address"] = address
        if cod_province:
            data["cod_province"] = cod_province
        if cod_city:
            data["cod_city"] = cod_city

    resp = requests.post(url, data=data).json()
    return resp
