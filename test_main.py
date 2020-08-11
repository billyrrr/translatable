import pytest
from flask.testing import FlaskClient

import main


@pytest.fixture
def app():
    main.app.testing = True
    client = main.app.test_client()
    return client


def test_translate(app: FlaskClient):
    import os

    path = './'
    files = os.listdir(path)

    files_txt = [i for i in files if
                 i.endswith('.md') and not i.endswith('.zh.md')]
    for file_path in files_txt:
        with open(path + file_path, 'r') as f:
            ss = f.read()
            res = app.post('/translate', data=ss, content_type='text/plain')
            assert res.get_data(as_text=True) != ""


def test_translate_list(app: FlaskClient):
    ss = """
1.   Front end sends HTTP request to Server 
2.   Server queries datastore
3.   Server returns response
    """
    res = main.change(ss)
    assert res == ""
