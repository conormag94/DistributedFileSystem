from flask_script import Manager

from project import create_app, db
from project.models import File

app = create_app()
manager = Manager(app)

@manager.command
def recreate_db():
    """Recreate a new empty database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    db.session.add(File(filename="init1.txt", content="Seeding the database"))
    db.session.commit()

if __name__ == '__main__':
    manager.run()
    