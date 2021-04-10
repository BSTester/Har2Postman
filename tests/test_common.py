import operator

import pytest

from har2postman.common import extract_params, convert_dict_key, convert_headers, convert_body


class TestCommon:

    @pytest.mark.parametrize('url, expected', [
        ('q=testerhome&encoding=utf-8', [{'key': 'q', 'value': 'testerhome'},
                                         {'key': 'encoding', 'value': 'utf-8'}]),
        ('api_code=eagle.api.checkAppUpdate&clientVersionName=T4.7.35',
         [{'key': 'api_code', 'value': 'eagle.api.checkAppUpdate'}, {'key': 'clientVersionName', 'value': 'T4.7.35'}])
    ])
    def test_extract_params(self, url, expected):
        assert operator.eq(extract_params(url), expected) is True

    @pytest.mark.parametrize('har_headers', [
        ([{'name': 'www', 'value': '1234'}]),
    ])
    def test_change_dict_key(self, har_headers):
        assert 'name' not in convert_dict_key(har_headers)[0].keys()

    def test_change_headers(self):
        headers = [{"name": ":method", "value": "POST"}, {"name": ":authority", "value": "mubu.com"},
                   {"name": ":scheme", "value": "https"}, {"name": ":path", "value": "/api/login/submit"},
                   {"name": "content-length", "value": "49"},
                   {"name": "accept", "value": "application/json, text/javascript, */*; q=0.01"},
                   {"name": "origin", "value": "https://mubu.com"},
                   {"name": "cookie", "value": "reg_focusId=82a02971-d4ce-47fe-baa9-16fa2f81bc9"}]
        for i in convert_headers(headers):
            assert [x for x in i.keys()] == ['value', 'key']

    def test_change_body_error(self):
        har_request = {
            "postData": {
                "mimeType": "123",
                "text": ""
            }
        }
        try:
            convert_body(har_request)
            assert False
        except Exception:
            assert True
