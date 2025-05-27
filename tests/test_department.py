from unittest.mock import patch, MagicMock, AsyncMock

@patch("interfaces.api.departments.AzureBlobClient")
@patch("interfaces.api.departments.DepartmentRepository")
def test_process_departments(mock_repo_class, mock_blob_class, client):
    # Mock blob CSV
    mock_blob = MagicMock()
    mock_blob.download_csv.return_value = [["1", "Engineering"], ["2", "HR"]]
    mock_blob_class.return_value = mock_blob

    # Mock repo with async method
    mock_repo = MagicMock()
    mock_repo.insert_departments = AsyncMock(return_value={
        "departments": {
            "processed": 2,
            "inserted": 2,
            "already_exists": 0,
            "errors": 0
        }
    })
    mock_repo_class.return_value = mock_repo

    response = client.post("/process/departments")
    assert response.status_code == 200
    assert response.json()["departments"]["processed"] == 2
