# IPaymu Client (UNOFFICIAL)

ipaymu-python adalah klien untuk ipaymu (payment gateway) dibuat menggunakan python.

## Fitur

* Dukungan API v1 dan v2 ipaymu.
* Dukungan untuk proyek Django


## Catatan

Ada beberapa API yang belum dites, jika ada bug silahkan buat isu [disini](https://github.com/aprilahijriyan/ipaymu-python/issues).


## Usage

* Konfigurasi

    Melalui fungsi `ipaymu.init`:

    ```python
    import ipaymu

    ipaymu.init(
        url="https://sandbox.ipaymu.com",
        va_account="00000000000000000",
        api_key="XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"
    )
    ```

    Melalui environment variable (Setelah membuat variable, anda harus memanggil fungsi `ipaymu.init()` tanpa parameter):

    ```sh
    export IPAYMU_URL = "https://sandbox.ipaymu.com"
    export IPAYMU_VA_ACCOUNT = "00000000000000000"
    export IPAYMU_API_KEY = "XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"
    ```

    Atau, melalui konfigurasi `settings.py` pada proyek Django.

    ```python
    # settings.py
    IPAYMU_URL = "https://sandbox.ipaymu.com"
    IPAYMU_VA_ACCOUNT = "00000000000000000"
    IPAYMU_API_KEY = "XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX"
    ```

* Cek Saldo

    ```python
    ipaymu.cek_saldo()
    ```

    Dan masih banyak lagi...


* API v2

    ```python
    ipaymu.v2.direct_payment
    ipaymu.v2.redirect_payment
    ```
