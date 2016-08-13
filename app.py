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

FACEBOOK_TOKEN ='EAAEAj1gffywBADfUP6JTpuI9nmvz9IlGfkvxKZBsXg7kO4ZA3TaSQy6PfbSZB3ZCMqEX3uzjUTVrq4g40CXk6LyOc5rekZBL1ZCBhpjWYulAPHHXZAfS3wpLwGp5EE9N0yAP3eIlD2mfZCAiAMW8HEUmf7bpG8AZCZAc4l5ZBZCloxnVlQZDZD'
bot = None

###
# Routing for your application.
###

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == 'i_dont_have_password':
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)
        
        print "Outgoing to %s: %s" % (sender, 'all is well')
        messenger.send_message(FACEBOOK_TOKEN, sender, 'all is well')
    
    return "ok"

###
# The functions below should be applicable to all Flask apps.
###

if __name__ == '__main__':
    app.run(debug=True)
