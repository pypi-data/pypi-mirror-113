import requests

from .helper import get_data, get_url


def cod_request_sid(
    product, quantity, price, weight, dimension, address, postal_code, unotify
):
    url = get_url("/api/payment/getsid")
    data = get_data(False)
    data["pay_method"] = "cod"
    data["product"] = product
    data["quantity"] = quantity
    data["price"] = price
    data["weight"] = weight
    data["dimension"] = dimension
    data["address"] = address
    data["postal_code"] = postal_code
    data["unotify"] = unotify
    resp = requests.post(url, data=data).json()
    return resp


def cod_payment(
    sessionID, name, email, phone, address, provinsi, kecamatan, kelurahan, postal_code
):
    url = get_url("/api/payment/cod")
    data = get_data(False)
    data["sessionID"] = sessionID
    data["name"] = name
    data["email"] = email
    data["phone"] = phone
    data["provinsi"] = provinsi
    data["address"] = address
    data["kecamatan"] = kecamatan
    data["kelurahan"] = kelurahan
    data["postal_code"] = postal_code
    resp = requests.post(url, data=data).json()
    return resp


def cod_check_shipping_fee(kode_pos_from, kode_pos_to, weight):
    url = get_url("/api/cod/shippingfee")
    data = get_data(False)
    data["from"] = kode_pos_from
    data["to"] = kode_pos_to
    data["weight"] = weight
    resp = requests.post(url, data=data).json()
    return resp


def cod_get_area():
    url = get_url("/api/cod/getarea")
    resp = requests.get(url).json()
    return resp
