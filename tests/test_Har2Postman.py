import json
from os import path
from jsonschema.validators import validate

import jmespath
import pytest

from har2postman.har2postman import Har2Postman

BASE_PATH = path.dirname(__file__)


class TestHar2Postman:

    @pytest.mark.parametrize('har_path, count', [
        (path.join(BASE_PATH, 'datas', 'postman_echo.har'), 4),
        (path.join(BASE_PATH, 'datas', 'mubu.har'), 10),
        (path.join(BASE_PATH, 'datas', 'Content-Type.har'), 3)
    ])
    def test_run1(self, har_path, count):
        har2 = Har2Postman(har_path)
        har2.run()
        result_list = jmespath.search('item', har2.postman_collection)
        assert len(result_list) == count

    def test_collection_schema(self):
        h2p = Har2Postman(path.join(BASE_PATH, 'datas', 'mubu.har'))
        h2p.run()
        with open(path.join(BASE_PATH, 'datas', 'postman_collection_schema.json'), 'r', encoding='utf-8') as f:
            schema = json.load(f)
            validate(instance=h2p.postman_collection, schema=schema)
