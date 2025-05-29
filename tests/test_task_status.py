from unittest.mock import patch, MagicMock, AsyncMock

@patch("interfaces.api.task_status.Redis.from_url")
def test_status_invalid_id(mock_redis, client):
    mock_redis.return_value = MagicMock()
    response = client.get("/tasks/invalid-id/status")
    assert response.status_code == 200
    assert "error" in response.json()
