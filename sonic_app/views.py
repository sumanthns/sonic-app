from app import app
from flask import request, render_template, url_for
from lib.amqp_client import publish_message
from werkzeug.utils import redirect


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write_signal')
def write_signal():
    led = int(request.args.get('led'))
    output = False
    if request.args.get('output') == "1":
        output = True
    message = {'write_signal': {'led': led, 'output': output}}
    publish_message("pi1", message)
    return redirect(url_for('index'))
