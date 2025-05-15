# UNIT TESTING BACKEND

import pytest
import os 
from app import app
from unittest.mock import patch

# used to create a test client
# sources: https://docs.pytest.org/en/6.2.x/fixture.html, https://flask.palletsprojects.com/en/latest/testing/
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# PASSED 

# testing if the API key is set and accessed correctly
# sources: https://docs.pytest.org/en/stable/how-to/monkeypatch.html, https://flask.palletsprojects.com/en/latest/testing/
def test_get_api_key(monkeypatch):
    monkeypatch.setenv("NYT_API_KEY", "test-key") # temp set API KEY to test-key
    assert os.getenv("NYT_API_KEY") == "test-key" # ensures the API KEY matches "test-key"

# PASSED

#testing API route
# sources: https://docs.pytest.org/en/stable/how-to/monkeypatch.html, https://flask.palletsprojects.com/en/latest/testing/
def test_api_route(client, monkeypatch):
    monkeypatch.setenv("NYT_API_KEY", "test2-key") # temp NYT API KEY
    response = client.get("/api/key") # get request 
    assert response.status_code == 200 # ensures a 200 status code 
    assert response.get_json() == {"apiKey": "test2-key"} # ensures correct api key 

# PASSED 

# test that backend correctly serves static files
# source: https://docs.python.org/3/library/unittest.mock.html
def test_static_file(client):

    # setting a mocked file 
    with patch("app.os.path.exists") as mock_exists, \
         patch("app.send_from_directory") as mock_send:
        mock_exists.return_value = True
        mock_send.return_value = "mocked static file content"
        response = client.get("/test.txt")

        # ensures serving and response is correct
        mock_exists.assert_called_once_with("static/test.txt")
        mock_send.assert_called_once_with("static", "test.txt")
        assert response.data == b"mocked static file content"

