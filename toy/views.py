import time

from flask import render_template, request

from toy import app

@app.route('/')
def index():
    '''Just list out all our keys and all their vals with ts'''
    #just a temporary holder... the final data won't look like this
    dummies = [{'key': 'derp','val': 'herp', 'ts': time.time()}]
    return render_template('index.html', keys=dummies)

@app.route('/api/<key>', methods=['POST'])
def post_event(key):
    '''accept incomming POST requests to /api/$key with this body:
        value=derp&ts=133723050.00

        ts is optional, with servers current time as default
    '''
    val = request.form['value']
    if 'ts' in request.form:
        ts = float(request.form['ts'])
    else:
        ts = time.time()
    return "Setting %s to %s at %s" % (key, val, str(ts))
