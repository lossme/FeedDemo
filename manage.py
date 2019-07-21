import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_app, db


here = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(here, 'config.py')

app = create_app(config_file)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
