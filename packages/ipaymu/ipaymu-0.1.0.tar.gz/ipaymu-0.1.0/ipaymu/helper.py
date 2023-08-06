from .compat import settings


def get_url(path: str):
    return settings.IPAYMU_URL + path


def get_data(json_format=True):
    data = {"key": settings.IPAYMU_API_KEY}
    if json_format:
        data["format"] = "json"
    return data
