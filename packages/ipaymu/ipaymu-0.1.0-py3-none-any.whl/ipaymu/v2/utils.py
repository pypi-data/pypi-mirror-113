import hashlib
import hmac

from ..compat import settings, timezone


def create_signature(data_body: str):
    encrypt_body = hashlib.sha256(data_body.encode()).hexdigest()
    stringtosign = "{}:{}:{}:{}".format(
        "POST", settings.IPAYMU_VA_ACCOUNT, encrypt_body, settings.IPAYMU_API_KEY
    )
    signature = (
        hmac.new(
            settings.IPAYMU_API_KEY.encode(), stringtosign.encode(), hashlib.sha256
        )
        .hexdigest()
        .lower()
    )
    return signature


def create_headers(signature: str):
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    headers = {
        "Content-type": "application/json",
        "signature": signature,
        "va": settings.IPAYMU_VA_ACCOUNT,
        "timestamp": timestamp,
    }
    return headers
