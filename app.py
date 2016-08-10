"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import warnings
import os
from flask import Flask,request, redirect, url_for

import chatbot
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN ='EAAEAj1gffywBAOSBrW6yUKQCBzmVL2Km0bzCZAxmLZALX0PzwE82DO2YvG2I0BXPaTHMYnJWi6ZB3yZBZAxx1nRNTLqwIRHMQUSO1dcAW92IIZCnAr3SzT4naHNjbUEdem0j0fnI2oWHc1kMuAfKH0JP1MbZC2rwV3TvZBTpzomOLAZDZD'
bot = None

###
# Routing for your application.
###

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == 'i_dont_have_password'
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

if __name__ == '__main__':
    app.run(debug=True)
