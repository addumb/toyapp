from toy import app

if app.config['DEBUG']:
    app.debug = True

app.run(host="0.0.0.0")
