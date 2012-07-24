import time

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/favicon.ico')
def nocontent():
    return None, 204

@app.route('/')
def index():
    dummies = [{'key': 'derp','val': 'herp', 'ts': time.time()}]
    return render_template('index.html', keys=dummies)

@app.route('/api/<key>', methods=['POST'])
def post_event(key):
    val = request.form['value']
    if 'ts' in request.form:
        ts = float(request.form['ts'])
    else:
        ts = time.time()
    return "Setting %s to %s at %s" % (key, val, str(ts))


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
