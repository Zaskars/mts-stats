import requests
import schedule
import time
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database import get_session, engine
from models import Base, User, Event, UserEventStat, Connection
from mock_data import get_mock_data  # Импортируем функцию для получения статических данных
import os

# Константы из переменных окружения
API_URL = os.getenv('API_URL')
API_TOKEN = os.getenv('API_TOKEN')


def fetch_data_from_api(from_date: str) -> List[Dict]:
    # headers = {
    #     "x-auth-token": API_TOKEN,
    #     "Content-Type": "application/x-www-form-urlencoded"
    # }
    # response = requests.get(API_URL, headers=headers, params={"from": from_date})
    # response.raise_for_status()
    return get_mock_data()


def insert_or_update_user(session, user_data):
    user = session.query(User).filter_by(id=user_data['id']).first()
    if user:
        user.email = user_data['email']
        user.name = user_data['name']
        user.second_name = user_data['secondName']
        user.patr_name = user_data.get('patrName', '')
        user.phone = user_data['phone']
        user.sex = user_data['sex']
    else:
        user = User(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data['name'],
            second_name=user_data['secondName'],
            patr_name=user_data.get('patrName', ''),
            phone=user_data['phone'],
            sex=user_data['sex']
        )
        session.add(user)
    return user


def insert_or_update_event(session, event_data):
    event = session.query(Event).filter_by(id=event_data['id']).first()
    if event:
        event.name = event_data['name']
        event.starts_at = event_data['starts_at']
        event.ends_at = event_data['ends_at']
        event.duration = event_data['duration']
    else:
        event = Event(
            id=event_data['id'],
            name=event_data['name'],
            starts_at=event_data['starts_at'],
            ends_at=event_data['ends_at'],
            duration=event_data['duration']
        )
        session.add(event)
    return event


def insert_or_update_user_event_stat(session, user_event_stat_data):
    user_event_stat = session.query(UserEventStat).filter_by(
        user_id=user_event_stat_data['user_id'],
        event_id=user_event_stat_data['event_id']
    ).first()
    if user_event_stat:
        user_event_stat.question_count = user_event_stat_data['question_count']
        user_event_stat.chat_message_count = user_event_stat_data['chat_message_count']
        user_event_stat.user_chat_message_count = user_event_stat_data['user_chat_message_count']
        user_event_stat.user_question_count = user_event_stat_data['user_question_count']
        user_event_stat.additional_field_values = user_event_stat_data['additional_field_values']
        user_event_stat.actual_involvement = user_event_stat_data['actual_involvement']
        user_event_stat.speech_duration = user_event_stat_data['speech_duration']
        user_event_stat.percent_of_total_speech_duration = user_event_stat_data['percent_of_total_speech_duration']
        user_event_stat.users_reaction_clicks = user_event_stat_data['users_reaction_clicks']
        user_event_stat.percent_of_total_reaction_clicks = user_event_stat_data['percent_of_total_reaction_clicks']
        user_event_stat.actual_participant_activity_percent = user_event_stat_data[
            'actual_participant_activity_percent']
        user_event_stat.rating = user_event_stat_data['rating']
        user_event_stat.attention_control = user_event_stat_data['attention_control']
    else:
        user_event_stat = UserEventStat(
            user_id=user_event_stat_data['user_id'],
            event_id=user_event_stat_data['event_id'],
            question_count=user_event_stat_data['question_count'],
            chat_message_count=user_event_stat_data['chat_message_count'],
            user_chat_message_count=user_event_stat_data['user_chat_message_count'],
            user_question_count=user_event_stat_data['user_question_count'],
            additional_field_values=user_event_stat_data['additional_field_values'],
            actual_involvement=user_event_stat_data['actual_involvement'],
            speech_duration=user_event_stat_data['speech_duration'],
            percent_of_total_speech_duration=user_event_stat_data['percent_of_total_speech_duration'],
            users_reaction_clicks=user_event_stat_data['users_reaction_clicks'],
            percent_of_total_reaction_clicks=user_event_stat_data['percent_of_total_reaction_clicks'],
            actual_participant_activity_percent=user_event_stat_data['actual_participant_activity_percent'],
            rating=user_event_stat_data['rating'],
            attention_control=user_event_stat_data['attention_control']
        )
        session.add(user_event_stat)
    return user_event_stat


def insert_or_update_connection(session, connection_data):
    connection = session.query(Connection).filter_by(
        user_id=connection_data['user_id'],
        joined=connection_data['joined']
    ).first()
    if connection:
        connection.leaved = connection_data['leaved']
        connection.duration = connection_data['duration']
        connection.country = connection_data['country']
        connection.city = connection_data['city']
        connection.platform = connection_data['platform']
    else:
        connection = Connection(
            user_id=connection_data['user_id'],
            event_id=connection_data['event_id'],
            joined=connection_data['joined'],
            leaved=connection_data['leaved'],
            duration=connection_data['duration'],
            country=connection_data['country'],
            city=connection_data['city'],
            platform=connection_data['platform']
        )
        session.add(connection)
    return connection


def insert_data_into_db(data: List[Dict]) -> None:
    session = get_session()

    for user_data in data:
        user = insert_or_update_user(session, user_data)

        for session_data in user_data['eventSessions']:
            event_data = {
                'id': session_data['eventId'],
                'name': session_data['name'],
                'starts_at': session_data['startsAt'],
                'ends_at': session_data['endsAt'],
                'duration': session_data['duration']
            }
            event = insert_or_update_event(session, event_data)

            user_event_stat_data = {
                'user_id': user.id,
                'event_id': event.id,
                'question_count': session_data['questionCount'],
                'chat_message_count': session_data['chatMessageCount'],
                'user_chat_message_count': session_data['userChatMessageCount'],
                'user_question_count': session_data['userQuestionCount'],
                'additional_field_values': session_data['additionalFieldValues'],
                'actual_involvement': session_data['actualInvolvement'],
                'speech_duration': session_data['speechDuration'],
                'percent_of_total_speech_duration': session_data['percentOfTotalSpeechDuration'],
                'users_reaction_clicks': session_data['usersReactionClicks'],
                'percent_of_total_reaction_clicks': session_data['percentOfTotalReactionClicks'],
                'actual_participant_activity_percent': session_data['actualParticipantActivityPercent'],
                'rating': session_data['rating'],
                'attention_control': session_data['attentionControl']
            }
            insert_or_update_user_event_stat(session, user_event_stat_data)

            for connection_data in session_data['connections']:
                connection_data.update({'user_id': user.id, 'event_id': event.id})
                insert_or_update_connection(session, connection_data)

    session.commit()
    session.close()


def job():
    from_date = "2022-01-01+00:00:00"
    data = fetch_data_from_api(from_date)
    insert_data_into_db(data)


schedule.every().day.at("00:26").do(job)

if __name__ == "__main__":
    # Создаем таблицы, если их нет
    Base.metadata.create_all(engine)

    while True:
        schedule.run_pending()
        time.sleep(1)
