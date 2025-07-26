import os
import sys
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

client = TestClient(app)


def test_predict_by_id_with_external_call(sample_inference_payload):
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_inference_payload
        mock_post.return_value = mock_response

        response = client.post(url="/predict-by-id", params={"id": "1"})
        assert response.json()["predictions"][0] == 130728.52589683191


def test_invalid_df_for_model_prediction_with_id(sample_inference_payload):
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_inference_payload
        mock_post.return_value = mock_response

        with patch("api.main.model.predict") as mock_predict:
            # Mock the behavior of model.predict
            mock_predict.side_effect = ValueError(
                "Invalid DataFrame format"
            )  # Example exception
            response_with_id = client.post(url="/predict-by-id", params={"id": "1"})

            # Assert that model.predict was called with the expected DataFrame
            assert mock_predict.call_count == 1
            # Similarly, test the endpoint using id payload
            assert response_with_id.status_code == 500
            assert response_with_id.json() == {"detail": "Invalid DataFrame format"}


def test_invalid_df_for_model_prediction(sample_inference_payload):
    with patch("api.main.model.predict") as mock_predict:
        # Mock the behavior of model.predict
        mock_predict.side_effect = ValueError(
            "Invalid DataFrame format"
        )  # Example exception
        response = client.post(url="/predict", json=sample_inference_payload)

        # Assert that model.predict was called with the expected DataFrame
        assert mock_predict.call_count == 1
        # Check that the endpoint returns the expected error response
        assert response.status_code == 500
        assert response.json() == {"detail": "Invalid DataFrame format"}


def test_correct_inference(sample_inference_payload):
    response = client.post(url="/predict", json=sample_inference_payload)
    assert response.json() == {"predictions": [130728.52589683191]}
