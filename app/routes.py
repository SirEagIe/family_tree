from app import app

@app.route('/')
@app.route('/index')
def insex():
    return 'Hello, World!'

