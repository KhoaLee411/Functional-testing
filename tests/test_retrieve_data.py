import os
import sys

from fastapi.testclient import TestClient

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import constants
from api.main import app

client = TestClient(app)


def test_retrieve_data():
    response = client.post(url="/retrieve-data", params={"id": "1"})
    assert response.json() == constants.SAMPLE_DATA
