import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


CRM_URL = "http://127.0.0.1:8001"

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()
session.mount("http://", adapter)


def get_customer_details(customer_id: int):

    try:
        response = session.get(
            f"{CRM_URL}/customers/{customer_id}",
            timeout=5
        )

        response.raise_for_status()

        return {
            "success": True,
            "customer": response.json()
        }

    except requests.exceptions.HTTPError as e:

        if e.response is not None and e.response.status_code == 404:
            return {
                "success": False,
                "error": f"Customer {customer_id} not found."
            }

        return {
            "success": False,
            "error": "CRM server error."
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "CRM request timed out."
        }

    except requests.exceptions.RequestException:

        return {
            "success": False,
            "error": "Unable to connect to CRM."
        }