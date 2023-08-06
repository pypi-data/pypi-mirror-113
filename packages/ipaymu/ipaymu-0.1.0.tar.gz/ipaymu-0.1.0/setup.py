# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipaymu', 'ipaymu.v2']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'ipaymu',
    'version': '0.1.0',
    'description': 'IPaymu Client For Python (UNOFFICIAL)',
    'long_description': '# IPaymu Client (UNOFFICIAL)\n\nipaymu-python adalah klien untuk ipaymu (payment gateway) dibuat menggunakan python.\n\n## Fitur\n\n* Dukungan API v1 dan v2 ipaymu.\n* Dukungan untuk proyek Django\n\n\n## Catatan\n\nAda beberapa API yang belum dites, jika ada bug silahkan buat isu [disini](https://github.com/aprilahijriyan/ipaymu-python/issues).\n\n\n## Usage\n\n* Konfigurasi\n\n    Melalui fungsi `ipaymu.init`:\n\n    ```python\n    import ipaymu\n\n    ipaymu.init(\n        url="https://sandbox.ipaymu.com",\n        va_account="00000000000000000",\n        api_key="XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"\n    )\n    ```\n\n    Melalui environment variable (Setelah membuat variable, anda harus memanggil fungsi `ipaymu.init()` tanpa parameter):\n\n    ```sh\n    export IPAYMU_URL = "https://sandbox.ipaymu.com"\n    export IPAYMU_VA_ACCOUNT = "00000000000000000"\n    export IPAYMU_API_KEY = "XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"\n    ```\n\n    Atau, melalui konfigurasi `settings.py` pada proyek Django.\n\n    ```python\n    # settings.py\n    IPAYMU_URL = "https://sandbox.ipaymu.com"\n    IPAYMU_VA_ACCOUNT = "00000000000000000"\n    IPAYMU_API_KEY = "XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"\n    ```\n\n* Cek Saldo\n\n    ```python\n    ipaymu.cek_saldo()\n    ```\n\n    Dan masih banyak lagi...\n\n\n* API v2\n\n    ```python\n    ipaymu.v2.direct_payment\n    ipaymu.v2.redirect_payment\n    ```\n',
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aprilahijriyan/ipaymu-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
