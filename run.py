import sqlalchemy as sa
import sqlalchemy.orm as so
from bgben import create_app, db
from bgben.models import User, Post, Notification, Message, Notification, Task

app = create_app()

@app.shell_context_processor
def make_shell_context():
  return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post, 
          'Notification': Notification, 'Message': Message, 'Tasks': Task}

if __name__ == "__main__":
  app.run()