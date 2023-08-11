import datetime

from sqlalchemy import Column, BigInteger, VARCHAR, DateTime, Boolean, ForeignKey, Date, Integer, String
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from .. import db_client


class Timesheet(db_client.Model, SerializerMixin):
    __tablename__ = 'timesheet'

    sheet_id = Column(BigInteger, primary_key=True)
    emp_id = Column(BigInteger, nullable=False)
    from_date = Column(Date)
    to_date = Column(Date)
    date = Column(VARCHAR(100))
    total_hrs = Column(NUMERIC(5, 2))
    send = Column(Boolean, default=False)
    sent_at = Column(DateTime)
    status = Column(VARCHAR(50), default='pending')
    status_at = Column(DateTime)
    reason = Column(VARCHAR(255))
    compcode = Column(BigInteger)
    modified_by = Column(VARCHAR(100))
    modified_on = Column(DateTime)
    created_by = Column(VARCHAR(100))
    created_on = Column(DateTime)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)


class TimesheetSelf(db_client.Model, SerializerMixin):
    __tablename__ = 'timesheet_self'

    self_id = Column(BigInteger, primary_key=True)
    sheet_id = Column(BigInteger, nullable=False)
    emp_id = Column(BigInteger)
    task_id = Column(BigInteger)
    sub_task_id = Column(BigInteger)
    category_id = Column(BigInteger)
    project_id = Column(BigInteger)
    page_id = Column(BigInteger)
    description = Column(VARCHAR(500))
    mon = Column(NUMERIC(4, 2))
    tue = Column(NUMERIC(4, 2))
    wed = Column(NUMERIC(4, 2))
    thu = Column(NUMERIC(4, 2))
    fri = Column(NUMERIC(4, 2))
    sat = Column(NUMERIC(4, 2))
    sun = Column(NUMERIC(4, 2))
    hrs_per_task = Column(NUMERIC(5, 2))
    compcode = Column(BigInteger)
    modified_by = Column(VARCHAR(100))
    modified_on = Column(DateTime)
    created_by = Column(VARCHAR(100))
    created_on = Column(DateTime)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

class Notification(db_client.Model, SerializerMixin):
    __tablename__ = 'notification'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer)
    subject = Column(String(255))
    action = Column(String(255))
    type = Column(VARCHAR(25))
    based = Column(VARCHAR(50))#ROQL/Order/Return
    status = Column(String(255), default="Unread")
    reference = Column(String(255))
    ref_id = Column(String(255))
    content = Column(String(1000))
    compcode = Column(BigInteger)
    created_at = Column(DateTime(), default=datetime.datetime.now())
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())
    deleted = Column(Boolean, default=False)
    redis_id = Column(String(255))
