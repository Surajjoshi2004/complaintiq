from fastapi.testclient import TestClient
# importing main app from the file
from complaintiq.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}    
    
    