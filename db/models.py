from sqlalchemy import Column, String, Boolean, DateTime
from db.dbconfig import Base

class Mention(Base):
    __tablename__ = "mentions"

    id = Column(String, primary_key=True)
    parent_text = Column(String)
    mention_text = Column(String)
    timestamp = Column(DateTime)
    mention_url = Column(String)
    replied = Column(Boolean, default=False)
    replied_at = Column(DateTime, nullable=True)
    reply = Column(String, nullable=True)
