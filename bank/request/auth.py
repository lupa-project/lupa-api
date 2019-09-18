import requests
from django.conf import settings
import json

GET_TOKEN_ENDPOINT = '/oauth/2.0/token'
GET_USER_INFO_ENDPOINT = '/user/me'


def get_token(code):
    url = settings.OPEN_PLATFORM_URL + GET_TOKEN_ENDPOINT
    data = {
            "code": code,
            "client_id": settings.OPEN_PLATFORM_API_KEY,
            "client_secret": settings.OPEN_PLATFORM_API_SECRET,
            # TODO urls 에서 받아오는걸로 교체가 좋을듯. 일단 테스트를 위해 localhost
            "redirect_uri": "http://localhost:8000/bank/create_bank_user",
            "grant_type": "authorization_code"
        }
    # )
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        'POST',
        url,
        headers=headers,
        data=data,
        allow_redirects=False,
        timeout=30
    )
    res_dict = response.json()

    if 'rs_code' in res_dict or 'rsp_message' in res_dict:
        # TODO logger 에 error code 적어야함.
        print(res_dict)
        raise ValueError
    if (
            'access_token' not in res_dict
            or 'token_type' not in res_dict
            or 'expires_in' not in res_dict
            or 'refresh_token' not in res_dict
            or 'scope' not in res_dict
            or 'user_seq_no' not in res_dict
    ):
        # TODO error logging
        raise ValueError

    return res_dict


def get_bank_user_info(token, user_seq_no):

    url = settings.OPEN_PLATFORM_URL + GET_USER_INFO_ENDPOINT

    params = {
        'user_seq_no': user_seq_no
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.request('GET', url, headers=headers, params=params, allow_redirects=False, timeout=30)
    res_dict = response.json()
    if res_dict['rsp_code'] != 'A0000':
        # TODO logger 에 error code 적어야함.
        raise ValueError

    return res_dict
