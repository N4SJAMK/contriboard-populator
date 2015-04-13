import json
import random
import pprint

import requests
import loremipsum

import helper_functions as h

API_URL = "http://localhost:9002/api{0}"
JSON_HEADER = {'Content-type': 'application/json'}

DEFAULT_USER = "user{0}@user.com"
DEFAULT_PASSWD = "password{0}"

def get_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def get_random_data(users, min_boards, max_boards, min_tickets, max_tickets):
    data = []
    for i in range(users):
        user_name = DEFAULT_USER.format(str(i))
        password = DEFAULT_PASSWD.format(str(i))
        user = {'email': user_name, 'password': password, 'boards': []}
        for _ in range(random.randint(min_boards, max_boards)):
            lorem = loremipsum.get_sentence()
            board = {'name': lorem, 'tickets': []}
            for _ in range(random.randint(min_tickets, max_tickets)):
                lorem = loremipsum.get_sentence()
                ticket = {'content': lorem}
                board['tickets'].append(ticket)
            user['boards'].append(board)
        data.append(user)
    return data

def populate(data):
    read_conf()
    message = {
            'users':    {'created': 0},
            'boards':   {'created': 0},
            'tickets':  {'created': 0},
        }
    msg = map(create_user, data)

    return stitch_message(message, msg)

def create_user(user):
    message = {
            'users':    {'created': 0},
            'boards':   {'created': 0},
            'tickets':  {'created': 0},
        }
    new_user = request_create_user(user)

    if not new_user.get('id'):
        err = new_user.get('message') or "error"
        message['users'][err] = message['users'].get(err, 0) + 1
    else:
        message['users']['created'] += 1
        access_token = login(user)

        msg = map(create_board(access_token), user['boards'])
        message = stitch_message(message, msg)

    return message

def create_board(access_token):

    def _create_board(board):
        new_board = request_create_board(board, access_token)
        message = {
                'boards':  {'created': 0},
                'tickets': {'created': 0},
            }

        if not new_board.get('id'):
            err = new_board.get('message') or "error"
            message['boards'][err] = message['boards'].get(err, 0) + 1
        else:
            message['boards']['created'] += 1

            msg = map(create_ticket(new_board['id'], access_token), board['tickets'])
            message = stitch_message(message, msg)

        return message

    return _create_board

def create_ticket(board_id, access_token):

    def _create_ticket(ticket):
        new_ticket = request_create_ticket(ticket, board_id, access_token)
        message = {'tickets': {'created': 0}}

        if not new_ticket.get('id'):
            err = new_board.get('message') or "error"
            message['boards'][err] = message['boards'].get(err, 0) + 1
        else:
            message['tickets']['created'] += 1

        return message

    return _create_ticket

def read_conf(filename = "conf.yml"):

    global API_URL
    global DEFAULT_PASSWD
    global DEFAULT_USER

    conf = h.parse_config("conf.yml")
    if conf.get('api_url'):
        API_URL = conf['api_url'] + "{0}"
    if conf.get('default_passwd'):
        DEFAULT_PASSWD = conf['default_passwd']
    if conf.get('default_user'):
        DEFAULT_USER = conf['default_user']

def request_create_user(user):
    resource_url = API_URL.format("/auth/register")

    payload = json.dumps({'email': user['email'], 'password': user['password']})
    new_user = requests.post(resource_url, data = payload, headers = JSON_HEADER)
    return new_user.json()

def login(user):
    resource_url = API_URL.format("/auth/login")

    payload = json.dumps({'email': user['email'], 'password': user['password']})
    response = requests.post(resource_url, data = payload, headers = JSON_HEADER)
    return "Bearer {0}".format(response.headers['x-access-token'])

def request_create_board(board, access_token):
    headers = {'Content-type': 'application/json', 'Authorization': access_token}
    resource_url = API_URL.format("/boards")

    payload = json.dumps({'name': board['name']})
    new_board = requests.post(resource_url, data = payload, headers = headers)
    return new_board.json()

def request_create_ticket(ticket, board_id, access_token):
    headers = {'Content-type': 'application/json', 'Authorization': access_token}
    uri = "/boards/{0}/tickets".format(board_id)
    resource_url = API_URL.format(uri)

    payload = json.dumps({'content': ticket['content']})
    new_ticket = requests.post(resource_url, data = payload, headers = headers)
    return new_ticket.json()

def stitch_message(message, msg):
    for i in msg:
        for key, _ in i.iteritems():
            message[key] = message.get(key, {})
            for k, v in i[key].iteritems():
                message[key][k] = message[key].get(k, 0) + v
    return message

if __name__ == "__main__":
    data = get_data("populator_data.json")
    #data = get_random_data(100, 3, 10, 13, 20)
    populate(data)
