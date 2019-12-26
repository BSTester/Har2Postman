import operator

import pytest

from har2postman.common import extract_path, extract_params, change_dict_key


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
