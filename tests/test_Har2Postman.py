import pytest
import jsonpath
from har2postman.har2postman import Har2Postman


class TestHar2Postman:

    @pytest.mark.parametrize('har_path, count', [
        ('./tests/datas/postman_echo.har', 4),
    ])
    def test_run1(self, har_path, count):
        har2 = Har2Postman(har_path)
        har2.run()
        result_list = jsonpath.jsonpath(har2.postman_collection, '$.item')[0]
        assert len(result_list) == count

    def test_run2(self):
        har_path = './datas/chanjet.har'
        har2 = Har2Postman(har_path)
        har2.run()
