import operator

import pytest

from har2postman.common import extract_path, extract_params, change_dict_key, extract_hosts, change_headers


class TestCommon:

    @pytest.mark.parametrize('url, expected', [
        ('https://baidu.com', []),
        ('https://baidu.com/as', ['as']),
        ('https://baidu.com/as/1.0.0/____', ['as', '1.0.0', '____']),
        ('https://baidu.com/as?', ['as']),
        ('https://baidu.com/as?a=2', ['as']),
        ('http://sit-api.scooper.news/eagle-api/api?api_code=eagle.api.checkAppUpdate&clientVersionName=T4.7.35',
         ['eagle-api', 'api'])
    ])
    def test_extract_path(self, url, expected):
        result = extract_path(url)
        assert result == expected

    @pytest.mark.parametrize('url, expected', [
        ('https://www.baidu.com/wd?q=testerhome&encoding=utf-8', [{'key': 'q', 'value': 'testerhome'},
                                                                  {'key': 'encoding', 'value': 'utf-8'}]),
        ('http://sit-api.scooper.news/eagle-api/api?api_code=eagle.api.checkAppUpdate&clientVersionName=T4.7.35',
         [{'key': 'api_code', 'value': 'eagle.api.checkAppUpdate'}, {'key': 'clientVersionName', 'value': 'T4.7.35'}])
    ])
    def test_extract_params(self, url, expected):
        assert operator.eq(extract_params(url), expected) is True

    @pytest.mark.parametrize('har_headers', [
        ([{'name': 'www', 'value': '1234'}]),
    ])
    def test_change_dict_key(self, har_headers):
        assert 'name' not in change_dict_key(har_headers)[0].keys()

    @pytest.mark.parametrize('url, expected', [
        ('https://baidu.com', ('baidu.com', None)),
        ('https://baidu.com/as', ('baidu.com', None)),
        ('https://192.168.2.1/baidu.com/as/1.0.0/', ('192.168.2.1', None))
    ])
    def test_extract_hosts(self, url, expected):
        assert extract_hosts(url) == expected

    def test_change_headers(self):
        headers = [{"name": ":method", "value": "POST"}, {"name": ":authority", "value": "mubu.com"},
                   {"name": ":scheme", "value": "https"}, {"name": ":path", "value": "/api/login/submit"},
                   {"name": "content-length", "value": "49"},
                   {"name": "accept", "value": "application/json, text/javascript, */*; q=0.01"},
                   {"name": "origin", "value": "https://mubu.com"},
                   {"name": "cookie", "value": "reg_focusId=82a02971-d4ce-47fe-baa9-16fa2f81bc9"}]
        for i in change_headers(headers):
            assert [x for x in i.keys()] == ['value', 'key']
