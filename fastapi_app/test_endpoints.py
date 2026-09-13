"""
Test FastAPI Prediction Endpoints with TestClient
"""
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock redis and minio before importing main
mock_redis = MagicMock()
mock_minio = MagicMock()

with patch.dict("sys.modules", {"redis": MagicMock(), "minio": MagicMock()}):
    sys.path.insert(0, "C:/eco/friday/fastapi_app")
    import main

from fastapi.testclient import TestClient

client = TestClient(main.app)

class TestFastAPIPrediction(unittest.TestCase):
    def setUp(self):
        # Reset mocks on main.redis_client
        main.redis_client = MagicMock()

    def test_predict_endpoint_post(self):
        main.redis_client.get.return_value = "PENDING"
        response = client.post("/predict", json={"text": "Apple is looking at buying U.K. startup for $1 billion"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("job_id", data)
        self.assertEqual(data["status"], "PENDING")
        self.assertTrue(main.redis_client.rpush.called)

    def test_predict_endpoint_v1_post(self):
        main.redis_client.get.return_value = "PENDING"
        response = client.post("/api/v1/predict", json={"text": "Steve Jobs founded Apple"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("job_id", data)
        self.assertEqual(data["status"], "PENDING")

    def test_predict_status_get(self):
        main.redis_client.get.side_effect = lambda key: {
            "job:test_job_123:status": "COMPLETED",
            "predict_job:test_job_123": '{"job_id": "test_job_123", "status": "COMPLETED"}',
            "job:test_job_123:result": '{"entities": [{"entity": "ORG", "word": "Apple", "score": 0.99}]}'
        }.get(key, None)

        response = client.get("/predict/test_job_123")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["job_id"], "test_job_123")
        self.assertEqual(data["status"], "COMPLETED")
        self.assertIsNotNone(data["result"])

    def test_models_status_get(self):
        main.redis_client.get.return_value = '{"model_name": "bert-ner", "run_id": "run_001"}'
        main.redis_client.llen.return_value = 0
        main.redis_client.zcard.return_value = 0

        response = client.get("/api/v1/models/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("latest_model_info", data)

if __name__ == "__main__":
    unittest.main()
