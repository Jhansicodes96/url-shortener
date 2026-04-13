from sqlalchemy import column, Integer, String, DateTime, Column
from datetime import datetime
from database import Base
class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    original_url = Column(String,nullable=False)
    short_code = Column(String,unique=True ,index=True,nullable=False)
    clicks = Column(Integer,default=0)
    created_at = Column(DateTime,default=datetime.utcnow())