import os

import requests
import schedule
import time
from typing import List, Dict
from sqlalchemy.orm import sessionmaker
from database import get_session, engine
from mock_data import get_mock_data
from models import Base, User, EventSession, Connection


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


def insert_data_into_db(data: List[Dict]) -> None:
    session = get_session()

    for user_data in data:
        user = User(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data['name'],
            second_name=user_data['secondName'],
            patr_name=user_data.get('patrName', ''),
            phone=user_data['phone'],
            sex=user_data['sex']
        )

        for session_data in user_data['eventSessions']:
            event_session = EventSession(
                id=session_data['id'],
                user_id=user.id,
                name=session_data['name'],
                starts_at=session_data['startsAt'],
                ends_at=session_data['endsAt'],
                duration=session_data['duration'],
                event_id=session_data['eventId'],
                question_count=session_data['questionCount'],
                chat_message_count=session_data['chatMessageCount'],
                user_chat_message_count=session_data['userChatMessageCount'],
                user_question_count=session_data['userQuestionCount'],
                additional_field_values=session_data['additionalFieldValues'],
                actual_involvement=session_data['actualInvolvement'],
                speech_duration=session_data['speechDuration'],
                percent_of_total_speech_duration=session_data['percentOfTotalSpeechDuration'],
                users_reaction_clicks=session_data['usersReactionClicks'],
                percent_of_total_reaction_clicks=session_data['percentOfTotalReactionClicks'],
                actual_participant_activity_percent=session_data['actualParticipantActivityPercent'],
                rating=session_data['rating'],
                attention_control=session_data['attentionControl']
            )

            for connection_data in session_data['connections']:
                connection = Connection(
                    session_id=event_session.id,
                    joined=connection_data['joined'],
                    leaved=connection_data['leaved'],
                    duration=connection_data['duration'],
                    country=connection_data['country'],
                    city=connection_data['city'],
                    platform=connection_data['platform']
                )
                event_session.connections.append(connection)

            user.event_sessions.append(event_session)

        session.merge(user)

    session.commit()
    session.close()


def job():
    from_date = "2022-01-01+00:00:00"
    data = fetch_data_from_api(from_date)
    insert_data_into_db(data)


schedule.every().day.at("23:38").do(job)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    while True:
        schedule.run_pending()
        time.sleep(1)
