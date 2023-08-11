from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, Boolean
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy_serializer import SerializerMixin

from .. import db_client


class PageMast(db_client.Model, SerializerMixin):
    __tablename__ = 'page_config'

    page_id = Column(BigInteger, primary_key=True)
    page_name = Column(VARCHAR(255))
    description = Column(VARCHAR(255))
    compcode = Column(BigInteger)
    modified_by = Column(VARCHAR(100))
    modified_on = Column(DateTime)
    created_by = Column(VARCHAR(100))
    created_on = Column(DateTime)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
