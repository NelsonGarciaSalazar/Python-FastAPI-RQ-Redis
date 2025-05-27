from unittest.mock import patch, MagicMock, AsyncMock

@patch("application.background.JobRepository")
@patch("application.background.AzureBlobClient")
@patch("application.background.process_jobs_csv")
def test_process_jobs(mock_service, mock_repo_class, mock_blob_class, client):
    # Mock Azure Blob Client
    mock_blob = MagicMock()
    mock_blob.download_csv.return_value = [["1", "Developer"], ["2", "Recruiter"]]
    mock_blob_class.return_value = mock_blob

    # Mock Job Repository
    mock_repo = MagicMock()
    mock_repo.insert_jobs = AsyncMock(return_value={
        "jobs": {
            "processed": 2,
            "inserted": 2,
            "already_exists": 0,
            "errors": 0
        }
    })
    mock_repo_class.return_value = mock_repo

    # Mock domain service
    mock_service.return_value = {
        "jobs": {
            "processed": 2,
            "inserted": 2,
            "already_exists": 0,
            "errors": 0
        }
    }

    response = client.post("/process/jobs")
    assert response.status_code == 200
    assert "message" in response.json() or "jobs" in response.json()
