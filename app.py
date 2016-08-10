"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import warnings
import os
from flask import Flask, render_template, request, redirect, url_for

import chatbot
import messenger

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

FACEBOOK_TOKEN = os.environ['FACEBOOK_TOKEN']
bot = None

###
# Routing for your application.
###

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == os.environ['VERIFY_TOKEN']:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        
        response = bot.respond_to(message)
        
        print "Outgoing to %s: %s" % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)
    
    return "ok"

###
# The functions below should be applicable to all Flask apps.
###

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
