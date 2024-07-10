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
    user_event_stats = relationship('UserEventStat', back_populates='user', cascade='all, delete-orphan')
    connections = relationship('Connection', back_populates='user', cascade='all, delete-orphan')


class Event(Base):
    __tablename__ = 'events'
    id = Column(String, primary_key=True)
    name = Column(String)
    starts_at = Column(DateTime)
    ends_at = Column(DateTime)
    duration = Column(Integer)
    user_event_stats = relationship('UserEventStat', back_populates='event', cascade='all, delete-orphan')
    connections = relationship('Connection', back_populates='event', cascade='all, delete-orphan')


class UserEventStat(Base):
    __tablename__ = 'user_event_stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'))
    event_id = Column(String, ForeignKey('events.id', ondelete='CASCADE'))
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
    user = relationship('User', back_populates='user_event_stats')
    event = relationship('Event', back_populates='user_event_stats')

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='_user_event_stat_uc'),)


class Connection(Base):
    __tablename__ = 'connections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE'))
    event_id = Column(String, ForeignKey('events.id', ondelete='CASCADE'))
    joined = Column(DateTime)
    leaved = Column(DateTime)
    duration = Column(Integer)
    country = Column(String)
    city = Column(String)
    platform = Column(String)
    user = relationship('User', back_populates='connections')
    event = relationship('Event', back_populates='connections')

    __table_args__ = (UniqueConstraint('user_id', 'joined', name='_connection_uc'),)
