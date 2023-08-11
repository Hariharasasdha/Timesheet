from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, Boolean, Date
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy_serializer import SerializerMixin

from .. import db_client


class AssignTask(db_client.Model, SerializerMixin):
    __tablename__ = 'assign_task'

    task_id = Column(BigInteger, primary_key=True)
    emp_id = Column(BigInteger, nullable=False)
    manager_id = Column(BigInteger)
    from_date = Column(Date)
    to_date = Column(Date)
    task = Column(VARCHAR(100))
    sub_task = Column(VARCHAR(100))
    category = Column(VARCHAR(100))
    project_id = Column(BigInteger)
    task_mast_id = Column(BigInteger)
    category_mast_id = Column(BigInteger)
    page_id = Column(BigInteger)
    description = Column(VARCHAR(100))
    compcode = Column(BigInteger)
    modified_by = Column(VARCHAR(100))
    modified_on = Column(DateTime)
    created_by = Column(VARCHAR(100))
    created_on = Column(DateTime)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

