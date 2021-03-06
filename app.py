"""
    Flask Documentation:     http://flask.pocoo.org/docs/
    Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
    Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

    This file creates your application.
    """
import warnings
import os
from flask import Flask,request, redirect, url_for
import sys,json,requests,time,urllib,re
from wit import Wit

import chatbot
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN ='EAACNa20bylsBAGo3VoZAxq8xvBnQcgwM0344Q990f39WE8b0OX9NuWPphqpLxVadjf9zf8ZA3k7ZBTgOLfLSYHZAZBhgPW9l1Nq9GRpKmZANKieUazSsFmF8pogN9tZCOquhlpJXHPSGrKyiKJZBokrDJGhsA068Bg1BtVg4ZAUh9cAZDZD'
bot = None

messageToSend = 'This is default. Something is not correct'
done = False
api_keys=['paxbk6508','xfagr5086','hqvyn6929']
#working file
#railway_api='paxbk6508'
#railway_api='xfagr5086'
#railway_api='hqvyn6929'
railway_api=api_keys[1]


def fetch_stnname(request):
    context = request['context']
    entities = request['entities']
    userinp = first_entity_value(entities, 'location').upper()
    code=stn_name_to_code(userinp)
    if code=='':
        context['stnname'] = 'Not found'
        return context
    context['stnname']=code
    return context

'''
def fetch_stnname(request):
    try:
        context = request['context']
        entities = request['entities']
        userinp = first_entity_value(entities, 'location').upper()
        code,response_code=stn_name_to_code(userinp)
        if str(parsed_json['response_code']) == '404':
            train_status = parsed_json['position']
            context['stnname'] = 'Service Down / Source not responding'
            return context
        if str(parsed_json['response_code']) == '403':
            train_status = parsed_json['position']
            context['stnname'] = 'Quota for the day exhausted.'
            return context
        if str(parsed_json['response_code']) == '204':
            train_status = parsed_json['position']
            context['stnname'] = 'Empty response. Not able to fetch required data.'
            return context
        if name == '':
            context['stnname'] = "Wrong station code or enter in code capital letters"
            return context
        if code=='':
            context['stnname'] = 'Not found'
            return context
        context['stnname']=code
        return context
    except Exception:
        print('Exception occured')
        context['stnname'] = 'Exception occured'
        return context
'''

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    try:
        print('Send Method')
        print(response['text'])
        global messageToSend
        messageToSend = response['text']
        global done
        done = True
    except Exception:
        print('Exception in send')

def fetch_statuspnr(request):
    try:
        context = request['context']
        entities = request['entities']
        pnr = str(first_entity_value(entities, 'number'))
        pnr2 = first_entity_value(entities, 'location')
        if pnr == 'None':
            # print('no pnr from number')
            num = (re.findall(r'\b\d+\b', str(pnr2)))
            if len(num) > 0:
                pnr = num[0]
            else:
                context['missingLocation'] = 'yes'
                return context

        url = 'http://api.railwayapi.com/pnr_status/pnr/' + str(pnr) + '/apikey/' + railway_api + '/'
        print('hello check for delay')
        parsed_json = json.loads(requests.get(url).text)
        print(parsed_json)
        error = (parsed_json['error'])
        print('response code: ' + str(parsed_json['response_code']))
        if str(parsed_json['response_code']) == '410':
            #print('response code: ' + parsed_json['response_code'])
            context['pnr_status'] = 'Flushed PNR / PNR not yet generated'
            return context
        if str(parsed_json['response_code']) == '404':
           # print('response code: ' + parsed_json['response_code'])
            context['pnr_status'] = 'Service Down / Source not responding'
            return context
        if str(parsed_json['response_code']) == '403':
            #print('response code: ' + parsed_json['response_code'])
            context['pnr_status'] = 'Quota exhausted for day'
            return context
        if str(parsed_json['response_code']) == '204':
            #print('response code: ' + parsed_json['response_code'])
            context['pnr_status'] = 'Empty response. Not able to fetch required data'
            return context
        if str(parsed_json['response_code']) == '200':
            print(parsed_json)
            from_stn = parsed_json['from_station']
            des_stn = parsed_json['reservation_upto']
            date_of_jrny = parsed_json['doj']
            total_passengers = parsed_json['total_passengers']
            passengers = parsed_json['passengers']
            status_list = '\nFROM ' + from_stn['name'] + ' TO ' + des_stn[
                'name'] + ' \nDate of Journey ' + date_of_jrny + '\n'
            for x in range(total_passengers):
                passenger_data = passengers[total_passengers - 1]
                status_list = status_list + ' No. ' + str(passenger_data['no']) + ' Status ' + passenger_data[
                    'current_status'] + '  ->' + passenger_data['booking_status'] + '\n'
                total_passengers = total_passengers - 1
            context['pnr_status'] = status_list
            return context
        if str(error).lower() == 'true':
            context['pnr_status'] = 'Error: wrong pnr no./missing pnr'
            return context

    except Exception:

        context['pnr_status'] = 'Exception pnr'
        return context


'''
def fetch_statuspnr(request):
    context = request['context']
    entities = request['entities']
    pnr = str(first_entity_value(entities, 'number'))
    pnr2 = first_entity_value(entities, 'location')
    if pnr == 'None':
        # print('no pnr from number')
        num = (re.findall(r'\b\d+\b', str(pnr2)))
        if len(num) > 0:
            pnr = num[0]
        else:
            context['missingLocation'] = 'yes'
            return context

    url = 'http://api.railwayapi.com/pnr_status/pnr/' + str(pnr) + '/apikey/' + railway_api + '/'
    parsed_json = json.loads(requests.get(url).text)
    error = (parsed_json['error'])
    if str(error).lower() == 'true':
        context['pnr_status'] = 'Error: wrong pnr no./missing pnr'
        return context
    print(parsed_json)
    from_stn = parsed_json['from_station']
    des_stn = parsed_json['reservation_upto']
    date_of_jrny = parsed_json['doj']
    total_passengers = parsed_json['total_passengers']
    passengers = parsed_json['passengers']
    status_list = '\nFROM ' + from_stn['name'] + ' TO ' + des_stn['name'] + ' \nDate of Journey ' + date_of_jrny + '\n'
    for x in range(total_passengers):
        passenger_data = passengers[total_passengers - 1]
        status_list = status_list + ' No. ' + str(passenger_data['no']) + ' Status ' + passenger_data[
            'current_status'] + '  ->' + passenger_data['booking_status'] + '\n'
        total_passengers = total_passengers - 1
    context['pnr_status'] = status_list
    return context
'''
'''
def fetch_statustrain(request):
    context = request['context']
    entities = request['entities']
    trainno = str(first_entity_value(entities, 'number'))
    trainno2 = first_entity_value(entities, 'location')
    if trainno == 'None':
        num = (re.findall(r'\b\d+\b', str(trainno2)))

        trainno = num[0]

    url = 'http://api.railwayapi.com/live/train/' + str(trainno) + '/doj/' + str(
        time.strftime("%Y%m%d")) + '/apikey/' + railway_api + '/'
    parsed_json = json.loads(requests.get(url).text)
    print(parsed_json)
    if str(parsed_json['response_code']) == '204':
        context['train_status'] = 'Wrong Train no'
        return context
    if str(parsed_json['response_code']) == '510':
        context['train_status'] = parsed_json['error']
        return context
    train_status = parsed_json['position']
    context['train_status'] = train_status
    return context
'''
def fetch_statustrain(request):
    try:
        context = request['context']
        entities = request['entities']
        trainno = str(first_entity_value(entities, 'number'))
        trainno2 = first_entity_value(entities, 'location')
        if trainno == 'None':
            num = (re.findall(r'\b\d+\b', str(trainno2)))
            trainno = num[0]
        print(trainno)
        url = 'http://api.railwayapi.com/live/train/' + str(trainno) + '/doj/' + str(
            time.strftime("%Y%m%d")) + '/apikey/' + railway_api + '/'
        parsed_json = json.loads(requests.get(url).text)
        print(parsed_json)
        print(parsed_json['response_code'])
        if str(parsed_json['response_code']) == '200':
            train_status = parsed_json['position']
            context['train_status'] = train_status
            return context
        elif str(parsed_json['response_code']) == '204':
            context['train_status'] = 'Wrong Train no'
            return context
        elif str(parsed_json['response_code']) == '510':
            context['train_status'] = parsed_json['error']
            return context
        elif str(parsed_json['response_code']) == '403':
            context['train_status'] = 'Quota for the day exhausted.'
            return context
        elif str(parsed_json['response_code']) == '404':
            context['train_status'] = 'Service Down / Source not responding'
            return context
        elif str(parsed_json['response_code']) == '404':
            train_status = parsed_json['position']
            context['train_status'] = train_status
            return context


    except Exception:
        print('Exception')
        context['train_status'] = 'Exception train status'
        return context

def fetch_stncode(request):
    context = request['context']
    entities = request['entities']
    userinp=str(first_entity_value(entities,'location')).upper()
    #print(userinp)
    name=stn_code_name(userinp)
    if name=='':
        context['stncode'] = "Wrong station code or enter in code capital letters"
        return context
    context['stncode'] = name
    return context
'''
def fetch_stncode(request):
    try:
        print("code to name")
        context = request['context']
        entities = request['entities']
        userinp=str(first_entity_value(entities,'location')).upper()
        print(userinp)
        name,response_code=stn_code_name(userinp)
        print(response_code )
        if str(parsed_json['response_code']) == '200':
            if name == '':
                context['stncode'] = "Wrong station code or enter in code capital letters"
                return context
            context['stncode'] = str(name)
            return context
        if str(parsed_json['response_code']) == '404':
            context['stncode'] = 'Service Down / Source not responding'
            return context
        if str(parsed_json['response_code']) == '403':
            context['stncode'] = 'Quota for the day exhausted.'
            return context
        if str(parsed_json['response_code']) == '204':
            context['stncode'] = 'Empty response. Not able to fetch required data.'
            return context

    except Exception:

        print('Exception in code to name')
        context['stncode'] = 'exception occureed'
        return context
'''
def stn_code_name(userinp):
    url = 'http://api.railwayapi.com/code_to_name/code/' + str(userinp).upper() + '/apikey/' + railway_api + '/'
    parsed_json = json.loads(requests.get(url).text)
    print(parsed_json)
    stations = parsed_json['stations']
    l_of_s = len(stations)
    searchobj = userinp
    name_code = ''
    response_code=parsed_json['response_code']
    while l_of_s > 0:
        data = stations[l_of_s - 1]
        if data['code'] == searchobj:
            name_code = (data['fullname'])
            break
        l_of_s = l_of_s - 1
    return name_code


def stn_name_to_code(userinp):
    url = 'http://api.railwayapi.com/name_to_code/station/' + userinp + '/apikey/' + railway_api + '/'
    parsed_json = json.loads(requests.get(url).text)
    print(parsed_json)
    stations = parsed_json['stations']
    l_of_s = len(stations)
    searchobj = userinp
    response_code=parsed_json['response_code']
    name_code = ''
    while l_of_s > 0:
        data = stations[l_of_s - 1]
        if data['fullname'] == searchobj:
            name_code = (data['code'])
            break
        l_of_s = l_of_s - 1
    return name_code


def fetch_train(requests):
    context = requests['context']
    entities = requests['entities']
    a=str(first_entity_value(entities, 'origin')).upper()
    b=str(first_entity_value(entities, 'destination')).upper()
    origin = stn_name_to_code(a)
    dest = stn_name_to_code(b)
    dt = first_entity_value(entities, 'datetime')
    '''
    if str(response_code1)or str(response_code2) =='404':
        context['train_list'] = 'Service Down / Source not responding'
        return context
    elif str(response_code1)or str(response_code2) == '204':
        context['train_list'] = 'Not able to fetch required data.'
        return context
    elif str(response_code1)or str(response_code2) == '403':
        context['train_list'] = 'Quota for the day exhausted.'
        return context
    '''
    month = dt[5:7]
    date = dt[8:10]
    url = 'http://api.railwayapi.com/between/source/' + str(origin) + '/dest/' + str(dest) + '/date/' + str(
        date) + '-' + str(month) + '/apikey/' + railway_api + '/'
    train_list = train_btw_stn(url)
    context['train_list'] = train_list
    return context
    '''
    try:

    except Exception:
        context['train_list'] = 'Exception train b/w stn'
        return context
    '''

def train_btw_stn(url):
    parsed_json = json.loads(requests.get(url).text)
    a = parsed_json['train']
    train_list = 'Train name   DEPT  ARVL \n'
    for x in range(len(a)):
        b = a[x]
        train_list = train_list + b['name'] + ' ' + b['src_departure_time'] + ' ' + b['dest_arrival_time'] + '\n'
    return train_list

def fetch_cancelled(request):
    try:
        context = request['context']
        entities = request['entities']
        dateinp=str(first_entity_value(entities, 'datetime'))
        print(dateinp)
        if dateinp=='None':
            print('no date')
            context['missingDate']=True
            return context
        url='http://api.railwayapi.com/cancelled/date/'+dateinp[8:10]+'-'+dateinp[5:7]+'-'+dateinp[0:4]+'/apikey/'+railway_api+'/'
        parsed_json = json.loads(requests.get(url).text)
        response_code=parsed_json['response_code']
        print(response_code)
        if str(response_code)=='204':
            context['cancel_train'] = 'Not able to fetch required data.'
            return context
        elif str(response_code)=='404':
            context['cancel_train'] = 'Service Down / Source not responding'
            return context
        elif str(response_code) == '403':
            context['cancel_train'] = 'Quota for the day exhausted.'
            return context
        elif str(response_code) == '200':
            trains = parsed_json['trains']
            cancel_train = ''
            for x in range(len(trains)):
                data = trains[x]
                train = data['train']
                name = train['name']
                num = train['number']
                cancel_train = cancel_train + name + ' ' + num + '\n'
            context['cancel_train']=cancel_train
            return context
    except Exception:
        context['cancel_train']='exception cancelled'
        return context


def fetch_reschedule(request):
    try:
        context = request['context']
        entities = request['entities']
        dateinp=str(first_entity_value(entities,'datetime'))
        print(dateinp)
        if dateinp == 'None':
            print('no date')
            context['missingDate'] = True
            return context
        #url = 'http://api.railwayapi.com/rescheduled/date/20-07-2016/apikey/paxbk6508/'
        url = 'http://api.railwayapi.com/rescheduled/date/' + dateinp[8:10] + '-' + dateinp[5:7] + '-' + dateinp[0:4] + '/apikey/' + railway_api + '/'
        parsed_json = json.loads(requests.get(url).text)
        response_code = parsed_json['response_code']
        print(response_code)
        if str(response_code) == '204':
            context['reschedule_train'] = 'Not able to fetch required data.'
            return context
        elif str(response_code) == '404':
            context['reschedule_train'] = 'Service Down / Source not responding'
            return context
        elif str(response_code) == '403':
            context['reschedule_train'] = 'Quota for the day exhausted.'
            return context
        elif str(response_code) == '200':
            print(parsed_json)
            trains = parsed_json['trains']
            reschleduled_train = ''
            for x in range(len(trains)):
                data = trains[x]
                name = data['name']
                num = data['number']
                reschleduled_train = reschleduled_train + name + ' ' + num + '\n'
            #print(reschleduled_train)
            context['reschedule_train']=str(reschleduled_train)
            return context
    except Exception:
        print('Exception rescheduled')
        context['reschedule_train'] = 'Exception rescheduled'
        return context


def say(session_id, context, msg):
    global messageToSend
    messageToSend = str(msg)
    global done
    done = True


def error(session_id, context, e):
    print(str(e))

actions = {
    'send': send,
    'say': say,
    'error': error,
    'fetch-statuspnr': fetch_statuspnr,
    'fetch-stncode': fetch_stncode,
    'fetch-stnname': fetch_stnname,
    'fetch-statustrain': fetch_statustrain,
    'fetch-train':fetch_train,
    'fetch-cancelled':fetch_cancelled,
    'fetch-reschedule':fetch_reschedule,
}

client = Wit(access_token='M6QM6SA2BEQN4WRMEWN7XU2AFVAUNFDL', actions=actions)

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
        print("Incoming from "+str(sender)+": "+str(message))
        client.run_actions(sender, message, {})
        if done:
            print("Outgoing to "+str(sender)+": "+str(messageToSend ))
            len_of_msg=len(str(messageToSend))
            print(str(len_of_msg))
            if len_of_msg>=319:
                msg = str(messageToSend).split('\n')
                print(len(msg))
                for x in range(int(len(msg)-2)):
                    print(msg[x])
                    messenger.send_message(FACEBOOK_TOKEN, sender, msg[x])
            else:
                messenger.send_message(FACEBOOK_TOKEN, sender, messageToSend)
        else:
            print("Outgoing to " + str(sender) + ": " + 'some problem interpreting')
            #print "Outgoing to %s: %s" % (sender, 'some problem interpreting')
            messenger.send_message(FACEBOOK_TOKEN, sender, 'some problem interpreting')
    return "ok"

@app.route('/',methods=['GET'])
def home():
    return "Server is Online."

###
# The functions below should be applicable to all Flask apps.
###

if __name__ == '__main__':
    app.run(debug=True)

