from app import db
from app.models import User
from manage import app

def create_all():
    with app.app_context():
        create_participants()
        create_judges()


def create_participants():
    participant1 = User(username='the-exterminators', email='duy1@duy.com',
                        name='The Exterminators', proj_name='Electric Gun', is_judge=False)
    participant2 = User(username='penguins', email='duy2@duy.com',
                        name='Penguins', proj_name='Project Winter', is_judge=False)
    participant3 = User(username='lions', email='duy3@duy.com',
                        name='Lions', proj_name='Groceries Organizer', is_judge=False)
    participant4 = User(username='batman-family', email='duy4@duy.com',
                        name='Batman Family', proj_name='Bat Cave Management', is_judge=False)
    participant5 = User(username='speedsters', email='duy5@duy.com',
                        name='Speedsters', proj_name='Project 567', is_judge=False)
    participant6 = User(username='participant-6', email='duy6@duy.com',
                        name='Participant 6', proj_name='Project 6', is_judge=False)
    participant7 = User(username='participant-7', email='duy7@duy.com',
                        name='Participant 7', proj_name='Project 7', is_judge=False)
    participant1.set_password('123456abcdef')
    participant2.set_password('123456abcdef')
    participant3.set_password('123456abcdef')
    participant4.set_password('123456abcdef')
    participant5.set_password('123456abcdef')
    participant6.set_password('123456abcdef')
    participant7.set_password('123456abcdef')
    db.session.add(participant1)
    db.session.add(participant2)
    db.session.add(participant3)
    db.session.add(participant4)
    db.session.commit()
    db.session.add(participant5)
    db.session.add(participant6)
    db.session.add(participant7)
    db.session.commit()


def create_judges():
    judge1 = User(username='vu-quang-huy', email='duy8@duy.com',
                  name='Vũ Quang Huy', is_judge=True)
    judge2 = User(username='nguyen-phuong-thao', email='duy9@duy.com',
                  name='Nguyễn Phương Thảo', is_judge=True)
    judge1.set_password('123456abcdef')
    judge2.set_password('123456abcdef')
    db.session.add(judge1)
    db.session.add(judge2)
    db.session.commit()


create_all()
