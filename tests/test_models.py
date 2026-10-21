import pytest 
from pydantic import ValidationError
from complaintiq.main import ComplaintRequest
from fastapi.testclient import TestClient
from complaintiq.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

# we are  expecting a valid customer 
def test_valid_complaint_requests():
    complaint = ComplaintRequest(
        complaint_text = "My bank charged me twice",
        customer_id=101,
    )
    
    assert complaint.customer_id == 101
    assert complaint.complaint_text == "My bank charged me twice"

def test_invalid_customer_id():
    with pytest.raises(ValidationError):
        ComplaintRequest(
            complaint_text = "My bank charged me twice",
            customer_id = "abc",
        )
        
def test_create_complaint(client):
    payload = {
        "customer_id": 101, 
        "complaint_text": "My bank charged me thrice",
    }
    
    response = client.post("/complaints", json= payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Complaint received successfully"
    assert data["customer_id"] == 101
    assert data["id"] > 0
    assert data["complaint_text"] == "My bank charged me thrice"
    assert isinstance(data["predicted_category"],str)
    assert data["predicted_category"].strip() !=""

def test_create_complaint_invalid_customer_id(client):
    payload = {
        "customer_id": "abc",
        "complaint_text": "My bank charged me thrice",
    }
    
    response = client.post("/complaints",json= payload)
    
    assert response.status_code == 422
    
def test_get_complaints(client):
    response = client.get("/complaints")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert isinstance(data, list)
    
    for complaint in data:
        assert isinstance(complaint["id"],int)
        assert isinstance(complaint["customer_id"], int)
        assert isinstance(complaint["complaint_text"],str)
        assert isinstance(complaint["predicted_category"],str)
        assert isinstance(complaint["confidence"],float)
        
        ids = ["complaint[id] for compaint in data"]
        
        assert ids == sorted(ids, reverse=True)

def test_get_complaints_negative_skipt(client):
    response = client.get("/complaints?skip=-1")
    assert response.status_code == 422
    
def test_get_complaints_limit_too_large(client):
    response = client.get("/complaints?limit=101")
    
    assert response.status_code == 422