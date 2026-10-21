from complaintiq.database import engine
from complaintiq.models import Base,Complaint

Base.metadata.create_all(bind=engine)

print("Database tables created successfully")