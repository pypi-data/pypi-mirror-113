import logging
from typing import Callable
from typing import Dict
from typing import List

from requests import Response

from jsm_user_services.exception import EmailValidationError
from jsm_user_services.support.email_utils import perform_email_validators
from jsm_user_services.support.email_utils import validate_format_email
from jsm_user_services.support.http_utils import get_response_body
from jsm_user_services.support.http_utils import request
from jsm_user_services.support.settings_utils import get_from_settings_or_raise_missing_config

logger = logging.getLogger(__name__)


DEFAULT_VALIDATORS_FUNCTION = [validate_format_email]


def email_is_valid(
    email: str,
    use_callback_function_validator: bool = False,
    functions_to_validate_email: List[Callable] = DEFAULT_VALIDATORS_FUNCTION,
):
    """
    Returns if the given e-mail is valid
        Parameters:
            `email (str)`: the e-mail that will be validated
            `use_callback_function_validator (bool)`: indicates if some validators must be considered if the `status_code`
            is different from 200 (success), otherwise raises an exception
            `functions_to_validate_email (List[Callable])`: a list of validators that will be considered if the `status_code`
            is different from 200 (success) and the `use_callback_function_validator` is `True`

    """
    EVEREST_API_KEY = get_from_settings_or_raise_missing_config("EVEREST_API_KEY")
    EVEREST_API_URL = get_from_settings_or_raise_missing_config(
        "EVEREST_API_HOST", "https://api.everest.validity.com/api/2.0/validation/addresses"
    )

    with request(status_forcelist=(429, 500, 502, 503, 504)) as r:
        url: str = f"{EVEREST_API_URL}/{email}"
        headers: Dict = {"X-API-KEY": EVEREST_API_KEY}

        response: Response = r.get(url, headers=headers)
        payload: Dict = get_response_body(response)
        if response.status_code == 400:
            status: str = check_response_payload_error(payload)
            logger.warning(f"Everest API Response: {response.status_code} - {status}")
            return False
        if response.status_code != 200:
            status: str = check_response_payload_error(payload)
            logger.warning(f"{response.status_code} - {status}")
            if use_callback_function_validator:
                return perform_email_validators(
                    functions_to_validate_email=functions_to_validate_email,
                    email=email
                )
            raise EmailValidationError
        logger.info(f"Everest API Response: {payload}")
        return check_response_payload(payload)


def check_response_payload(payload: Dict) -> bool:
    """
    Checks if the response received from Everest indicated if the email is valid
        Example of success payload:
        {
            "meta": {},
            "results": {
                "category": "valid",
                "status": "valid",
                "name": "Valid",
                "definition": "The email has a valid account associated with it.",
                "reasons": [],
                "risk": "low",
                "recommendation": "send",
                "address": "ayron41@gmail.com",
                "diagnostics": {
                "role_address": false,
                "disposable": false,
                "typo": false
                }
            }
        }
    """
    results: Dict = payload.get("results") or {}
    status: str = results.get("status")
    if status:
        return status != "invalid"
    return False


def check_response_payload_error(payload: Dict) -> str:
    """
    Check the error received from Everest
        Example of error payload:
        ```{"status": "Bad Request: Invalid email address."}```
    """
    if payload:
        status: str = payload.get("status")
        return status
    return "Everest is out!"
