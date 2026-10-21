from pydantic import BaseModel, ConfigDict

class ComplaintRequest(BaseModel):
    customer_id: int
    complaint_text:str
    


class ComplaintResponse(BaseModel):
    id:int
    message:str
    customer_id:int
    complaint_text:str
    predicted_category: str
    confidence: float
    
    
class ComplaintRecord(BaseModel):
    id:int
    customer_id:int
    complaint_text:str
    predicted_category:str
    confidence:float
    
    model_config = ConfigDict(from_attributes=True)
    