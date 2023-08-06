try:
    from django.conf import settings  # noqa
    from django.utils import timezone  # noqa

except ImportError:
    from datetime import datetime

    class settings:
        IPAYMU_URL = "https://sandbox.ipaymu.com"
        IPAYMU_VA_ACCOUNT = "00000000000000000"
        IPAYMU_API_KEY = "XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"

    class Timezone:
        def now(self):
            return datetime.utcnow()

    timezone = Timezone()
