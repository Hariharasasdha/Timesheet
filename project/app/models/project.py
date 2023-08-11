from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from .. import db_client


class ProjectMast(db_client.Model, SerializerMixin):
    __tablename__ = 'project_mast'

    project_id = Column(BigInteger, primary_key=True)
    project_name = Column(VARCHAR(255))
    description = Column(VARCHAR(255))
    from_date = Column(Date)
    to_date = Column(Date)
    compcode = Column(BigInteger)
    modified_by = Column(VARCHAR(100))
    modified_on = Column(DateTime)
    created_by = Column(VARCHAR(100))
    created_on = Column(DateTime)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)


class MainActivities(db_client.Model, SerializerMixin):
    __tablename__ = 'main_activities'

    activity_id = Column(BigInteger, primary_key=True)
    project_id = Column(ForeignKey('project_mast.project_id'), nullable=False)
    activity_name = Column(VARCHAR(255))
    description = Column(VARCHAR(255))
    compcode = Column(BigInteger)
    modified_by = Column(VARCHAR(100))
    modified_on = Column(DateTime)
    created_by = Column(VARCHAR(100))
    created_on = Column(DateTime)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    project_mast = relationship('ProjectMast')
