from toy import app

if app.config['DEBUG']:
    app.debug = True

app.run()
