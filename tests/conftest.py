import pytest
import json
import os

@pytest.fixture
def load_person_mock():
    def _loader(page):
        # Localiza a pasta mocks relativa a este arquivo
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, 'mocks', f'page_{page}.json')
        with open(file_path, 'r') as f:
            return json.load(f)
    return _loader