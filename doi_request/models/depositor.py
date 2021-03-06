from datetime import datetime
from doi_request.models import Base
from sqlalchemy import func, ForeignKey, Column, Unicode, Integer, String, Boolean, Text, DateTime, Float
from sqlalchemy.orm import relationship


class Deposit(Base):
    __tablename__ = 'deposit'
    code = Column('code', String(27), unique=True, nullable=False, primary_key=True, index=True)
    pid = Column('pid', String(23), unique=True, nullable=False, index=True)
    issn = Column('issn', String(9), nullable=False, index=True)
    volume = Column('volume', String(16))
    number = Column('number', String(16))
    issue_label = Column('issue_label', String(32))
    journal = Column('journal', String(256), nullable=False, index=True)
    journal_acronym = Column('journal_acronym', String(16), nullable=False, index=True)
    collection_acronym = Column('collection_acronym', String(3), nullable=False)
    publication_year = Column('publication_year', Integer, index=True)
    xml_file_name = Column('xml_file_name', String(32), nullable=False)
    prefix = Column('prefix', String(16), nullable=False, index=True)
    doi = Column('doi', String(128), index=True)
    doi_batch_id = Column('doi_batch_id', String(32))
    is_xml_valid = Column('is_xml_valid', Boolean, default=False)
    started_at = Column('started_at', DateTime(timezone=True), nullable=False, index=True)
    updated_at = Column('updated_at', DateTime(timezone=True), nullable=False)
    submission_xml = Column('submission_xml', Text, default='')
    submission_status = Column('submission_status', String(16), default='unknow', index=True)
    submission_updated_at = Column('submission_updated_at', DateTime(timezone=True))
    submission_response = Column('submission_response', Text, default='')
    has_submission_xml_valid_references = Column('has_submission_xml_valid_references', Boolean, index=True)
    feedback_xml = Column('feedback_xml', Text, default='')
    feedback_status = Column('feedback_status', String(16), index=True)
    feedback_updated_at = Column('feedback_updated_at', DateTime(timezone=True))
    log_events = relationship('LogEvent', back_populates='deposit', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return 'Deposit(code="%s", pid="%s", doi="%s")' % (self.code, self.pid,
                self.doi)

    @property
    def timeline(self):
        return sorted(self.log_events, key=lambda event: event.date)

    @property
    def is_pending(self):
        pending_list = ['', 'waiting']
        if (self.submission_status in pending_list or 
            self.feedback_status in pending_list) and self.submission_xml:
            return True
        else:
            return False


class LogEvent(Base):
    __tablename__ = 'logevent'
    id = Column(Integer, primary_key=True)
    date = Column('date', DateTime(timezone=True), nullable=False, default=datetime.now)
    title = Column('title', Text, nullable=False)
    body = Column('body', Text, default='')
    type = Column('type', String(16), nullable=False)
    status = Column('status', String(16))
    deposit_code = Column('deposit_code', ForeignKey('deposit.code'), index=True)
    deposit = relationship("Deposit", back_populates="log_events")


class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    retro = Column('retro', Boolean, index=True)
    publication_year = Column('publication_year', Integer, index=True)
    registry_date = Column('registry_date', DateTime(timezone=True), default=datetime.now)
    doi = Column('doi', String(128), index=True)
    cost = Column('cost', Float, nullable=False)
