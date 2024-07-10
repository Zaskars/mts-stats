from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String)
    name = Column(String)
    second_name = Column(String)
    patr_name = Column(String, nullable=True)
    phone = Column(String)
    sex = Column(String)
    event_sessions = relationship('EventSession', back_populates='user')


class EventSession(Base):
    __tablename__ = 'event_sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    name = Column(String)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    duration = Column(Integer)
    event_id = Column(String)
    question_count = Column(Integer)
    chat_message_count = Column(Integer)
    user_chat_message_count = Column(Integer)
    user_question_count = Column(Integer)
    additional_field_values = Column(JSON)
    actual_involvement = Column(Float)
    speech_duration = Column(Integer)
    percent_of_total_speech_duration = Column(Float)
    users_reaction_clicks = Column(Integer)
    percent_of_total_reaction_clicks = Column(Float)
    actual_participant_activity_percent = Column(Float)
    rating = Column(Integer)
    attention_control = Column(JSON)
    connections = relationship('Connection', back_populates='event_session')
    user = relationship('User', back_populates='event_sessions')

    __table_args__ = (UniqueConstraint('id', 'user_id', name='_event_session_uc'),)


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('event_sessions.id'))
    joined = Column(DateTime)
    leaved = Column(DateTime)
    duration = Column(Integer)
    country = Column(String)
    city = Column(String)
    platform = Column(String)
    event_session = relationship('EventSession', back_populates='connections')

    __table_args__ = (UniqueConstraint('session_id', 'joined', name='_connection_uc'),)
