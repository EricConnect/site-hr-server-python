import restapi
from flask_script import Manager, prompt_bool
from restapi.models import User
import uuid
manager = Manager(restapi.app)
dba = restapi.db
@manager.command
def initdb():
    dba.create_all()
    dba.session.add(User(public_id=str(uuid.uuid4()), name='Eric', email='Eric_@gle.com'))
    dba.session.add(User(public_id=str(uuid.uuid4()), name='Chen', email='Chen@ck.com'))
    dba.session.commit()
    print 'Initialized the database'

@manager.command
def dropdb():
    if prompt_bool(
    'Are you sure you want to lose all your data'):
        dba.drop_all()
        print 'Dropped the database'

if __name__ == '__main__':
    manager.run()