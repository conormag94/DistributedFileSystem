from flask_script import Manager

from project import create_app, db

app = create_app()
manager = Manager(app)

@manager.command
def recreate_db():
    """Recreate a new empty database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    manager.run()
    