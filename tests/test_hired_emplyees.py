from unittest.mock import patch, MagicMock

MOCK_ROWS = [["1", "Alice", "2021-06-01T12:00:00Z", "1", "1"]] * 10

@patch("interfaces.api.hired_employees.AzureBlobClient")
@patch("interfaces.api.hired_employees.Redis.from_url")
@patch("interfaces.api.hired_employees.Queue")
def test_enqueue_hired_employees(mock_queue_class, mock_redis_class, mock_blob_client, client):
    # Mock blob
    mock_blob = MagicMock()
    mock_blob.download_csv.return_value = MOCK_ROWS
    mock_blob_client.return_value = mock_blob

    # Mock Redis
    mock_redis = MagicMock()
    mock_redis_class.return_value = mock_redis

    # Mock Queue
    mock_queue = MagicMock()
    mock_job = MagicMock()
    mock_job.id = "mock-task-id"
    mock_queue.enqueue.return_value = mock_job
    mock_queue_class.return_value = mock_queue

    response = client.post("/process/hired_employees?start=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "mock-task-id"
    assert data["limit"] == 10