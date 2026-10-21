from fastapi import FastAPI, Request,Query
from complaintiq.schemas import ComplaintResponse,ComplaintRequest,ComplaintRecord
from contextlib import asynccontextmanager
from pathlib import Path
import joblib
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session 
from complaintiq.database import get_db
from complaintiq.models import Complaint

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = Path("artifacts/complaint_classifier.joblib")
    app.state.classifier = joblib.load(model_path)
    
    yield

"""tells app top run lifespan function at startup and shutdown"""
app = FastAPI(title = "ComplaintIQ", lifespan=lifespan,)

@app.get('/health')
def health_check():
    return {"status": "ok"}

@app.post("/complaints", response_model=ComplaintResponse)
def create_complaint(
    complaint: ComplaintRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)]
)->ComplaintResponse:
    predicted_category = request.app.state.classifier.predict([complaint.complaint_text])[0]
    probabilites = request.app.state.classifier.predict_proba([complaint.complaint_text])[0]
    confidence = float(max(probabilites))
    new_complaint = Complaint(
        customer_id= complaint.customer_id,
        complaint_text=complaint.complaint_text,
        predicted_category=predicted_category,
        confidence=confidence,      
    )
    db.add(new_complaint)
    try:
        db.commit()
        db.refresh(new_complaint)
    except Exception:
        db.rollback()
        raise
    
    return ComplaintResponse(
        id= new_complaint.id,
        message= "Complaint received successfully",
        customer_id= complaint.customer_id,
        complaint_text= complaint.complaint_text,
        predicted_category=predicted_category,
        confidence=confidence
    )
        
@app.get("/complaints",response_model=list[ComplaintRecord])
def get_complaints(
    db: Annotated[Session , Depends(get_db)],
    skip: int = Query(default=0,ge= 0),
    limit: int= Query(default=10,ge=1, le=100)
)-> list[ComplaintRecord]:
    
    complaints= (
        db.query(Complaint)
        .order_by(Complaint.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return complaints

    