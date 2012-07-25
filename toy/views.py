import time

from flask import g, render_template, request

from toy import app

@app.route('/')
def index():
    '''
        Just list out all our keys and all their vals with ts

        the format of keys here is like this:
            {'key': [(event, ts), (event, ts), ...],
            'key2': [(event, ts),...]}
    '''
    cur = g.db.execute('select key, value, ts from events order by key, ts desc')
    keys = {}
    for row in cur.fetchall():
        if row[0] in keys:
            keys[row[0]].append((row[1], row[2]))
        else:
            keys[row[0]] = [(row[1], row[2])]

    print keys
    return render_template('index.html', keys=keys)

@app.route('/api/<key>', methods=['POST'])
def post_event(key):
    '''accept incomming POST requests to /api/$key with this body:
        value=derp&ts=133723050.00

        ts is optional, with servers current time as default
    '''
    val = float(request.form['value'])
    if 'ts' in request.form:
        ts = float(request.form['ts'])
    else:
        ts = time.time()

    g.db.execute('insert into events (key, value, ts) values (?, ?, ?)',
        (key, val, ts))
    g.db.commit()
    return "Setting %s to %s at %s" % (key, val, str(ts))
