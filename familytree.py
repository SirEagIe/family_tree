from app import app, db
from app.models import User, Human

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Human': Human}

app.run('0.0.0.0')
