from datetime import datetime,timezone

from sqlalchemy import DateTime,Float, Integer,String,Text
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column


class Base(DeclarativeBase):
    pass


class Complaint(Base):
    __tablename__ = "complaints"
    
    id: Mapped[int]= mapped_column(
        Integer, primary_key=True, index=True
    )
    
    customer_id: Mapped[int] = mapped_column(Integer,nullable=False)
    complaint_text: Mapped[str] = mapped_column(String,nullable=False)
    predicted_category: Mapped[str]= mapped_column(String(150),nullable=False )
    confidence : Mapped[float]= mapped_column(Float,nullable=False)
    createdAt: Mapped[datetime]=mapped_column(DateTime(timezone=True),
                                              default=lambda:datetime.now(timezone.utc))