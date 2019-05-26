from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from config import app, db
from apps.fileserver.views import *


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    """Create a python CLI.
    return: Default import object
    type: `Dict`
    """
    return dict(
        app = app,
        db = db,
        User = User,
        )


if __name__ == '__main__':
    manager.run()
