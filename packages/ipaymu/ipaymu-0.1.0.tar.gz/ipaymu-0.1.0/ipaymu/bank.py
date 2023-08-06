import requests

from .helper import get_data, get_url


def transfer_bca(amount, notifyUrl, name, phone, email):
    url = get_url("/api/bcatransfer")
    data = get_data(False)
    data["amount"] = amount
    data["notifyUrl"] = notifyUrl
    data["name"] = name
    data["phone"] = phone
    data["email"] = email
    resp = requests.post(url, data=data).json()
    return resp
