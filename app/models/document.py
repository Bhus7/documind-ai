from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped,  mapped_column
from datetime import datetime
from app.db.database import Base

class Document(Base):
    __tablename__  =  "documents"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
