import json

import httpretty
import pytest
import requests
from requests import Response

from jsm_user_services.services.email_validations import check_response_payload
from jsm_user_services.services.email_validations import check_response_payload_error
from jsm_user_services.support.email_utils import perform_email_validators
from jsm_user_services.support.email_utils import validate_format_email
from jsm_user_services.support.http_utils import get_response_body
from jsm_user_services.support.settings_utils import get_from_settings_or_raise_missing_config

EVEREST_API_URL = get_from_settings_or_raise_missing_config(
    "EVEREST_API_URL", "https://api.everest.validity.com/api/2.0/validation/addresses"
)

class TestValidateEmail:

    invalid_emails = [
        "ayron.araujo",
        "loiraojuntossomosmais.io",
        "leydsonjuntossomosmais.lol",
        "aldojuntossomosmais.com.br",
        "ayron41.@gmail.com",
        "emailqualquer@@juntossomosmais.com.br",
        "???@outlook.com",
        "",
    ]

    valid_emails = [
        "ayron41@gmail.com",
        "ayron.araujo@juntossomosmais.com.br",
        "ayron.style@hotmail.com",
    ]

    @pytest.mark.parametrize("email", invalid_emails)
    def test_should_return_false_when_email_is_invalid(self, email: str):

        assert perform_email_validators(
            [
                validate_format_email
            ],
            email
        ) is False

    @pytest.mark.parametrize("email", valid_emails)
    def test_should_return_true_when_email_is_valid(self, email: str):

        assert perform_email_validators(
            [
                validate_format_email
            ],
            email
        ) is True


class TestValidateEmailRequest:

    @httpretty.activate
    def test_should_retry_request_when_status_code_returned_is_504(self):

        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        mocked_error_response = {"status": "Gateway Timeout"}
        mocked_response = {"results": {"status": "risky"}}
        error_timeout_httpretty = httpretty.Response(body=json.dumps(mocked_error_response), status=504)
        success_response_httpretty = httpretty.Response(body=json.dumps(mocked_response), status=200)
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                error_timeout_httpretty,
                error_timeout_httpretty,
                error_timeout_httpretty,
                success_response_httpretty,
            ]
        )
        response1: Response = requests.get(url)
        payload1 = get_response_body(response1)
        assert check_response_payload(payload1) is False

        response2: Response = requests.get(url)
        payload2 = get_response_body(response2)
        assert check_response_payload(payload2) is False

        response3: Response = requests.get(url)
        payload3 = get_response_body(response3)
        assert check_response_payload(payload3) is False

        response4: Response = requests.get(url)
        payload4 = get_response_body(response4)
        assert check_response_payload(payload4) is True

    @httpretty.activate
    def test_should_return_message_when_email_is_valid_and_result_is_none(self):

        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        mocked_response = None
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(status=504, body=json.dumps(mocked_response))
            ],
        )
        response: Response = requests.get(url)
        payload = get_response_body(response)
        assert check_response_payload_error(payload) == "Everest is out!"

    @httpretty.activate
    def test_should_return_message_when_email_is_valid_and_result_is_empty(self):

        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        mocked_response = ""
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(status=504, body=json.dumps(mocked_response))
            ],
        )
        response: Response = requests.get(url)
        payload = get_response_body(response)
        assert check_response_payload_error(payload) == "Everest is out!"

    @httpretty.activate
    def test_should_return_message_when_response_dict_is_empty(self):

        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        mocked_response = {}
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(status=504, body=json.dumps(mocked_response))
            ],
        )
        response: Response = requests.get(url)
        payload = get_response_body(response)
        assert check_response_payload_error(payload) == "Everest is out!"

    @httpretty.activate
    def test_should_return_true_when_status_is_valid(self):

        mocked_response = {"results": {"status": "valid"}}
        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(body=json.dumps(mocked_response), status=200)
            ],
        )
        response: Response = requests.get(url)
        payload = get_response_body(response)
        assert check_response_payload(payload) is True

    @httpretty.activate
    def test_should_return_false_when_status_is_invalid(self):

        mocked_response = {"results": {"status": "invalid"}}
        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(body=json.dumps(mocked_response), status=200)
            ],
        )
        response: Response = requests.get(url)
        payload = get_response_body(response)
        assert check_response_payload(payload) is False

    @httpretty.activate
    def test_should_return_false_when_response_dict_is_empty(self):

        mocked_response = {}
        email: str = "ayron.araujo@juntossomosmais.com.br"
        url: str = f"{EVEREST_API_URL}/{email}"
        httpretty.register_uri(
            httpretty.GET,
            url,
            responses=[
                httpretty.Response(body=json.dumps(mocked_response), status=200)
            ],
        )
        response: Response = requests.get(url)
        payload = get_response_body(response)
        assert check_response_payload(payload) is False
