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
    # just grab everything!
    cur = g.db.execute('select key, value, ts from events order by key, ts desc')
    # we'll build this up as we go, but pass it to render all at once :(
    keys = {}
    # the rendering will appreciate knowing the x- and y-ranges
    minval = maxval = None
    mints = maxts = None

    # again, we just caught them all :
    for row in cur.fetchall():
        #we haven't set min/max val yet!
        if minval == None or maxval == None:
            minval = row[1]
            maxval = row[1]
        minval = min(minval, row[1])
        maxval = max(maxval, row[1])

        # we haven't set min/max ts yet!
        if mints == None or maxts == None:
            mints = row[2]
            maxts = row[2]
        mints = min(mints, row[2])
        maxts = max(maxts, row[2])
        # if we have already seen this key, add an event
        if row[0] in keys:
            keys[row[0]].append((row[1], row[2]))
        # means we haven't seen it, so set it to a 1-list
        else:
            keys[row[0]] = [(row[1], row[2])]

    # here, just spit out all the raw text over to jinja
    return render_template('index.html', keys=keys, tsrange=(mints, maxts),
        valrange=(minval, maxval))

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
