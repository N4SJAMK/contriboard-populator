import os
import pprint

import fabric
import populator
import helper_functions as h

CONF_FILE = "conf.yml"

def take_snapshot(name = None):
    conf = h.parse_config(CONF_FILE)
    dir_name, err = h.create_dir(name, conf['snapshots_dir'])
    if err:
        fabric.utils.abort(err)

    mongo_conf = conf['mongo']
    command = "mongodump -h {0} -d {1} -o {2}"
    host = "{0}:{1}".format(mongo_conf['host'], mongo_conf['port'])

    with fabric.context_managers.lcd(conf['snapshots_dir']):
        fabric.operations.local(command.format(host, mongo_conf['db'], dir_name))

    h.set_symlink("latest", dir_name, conf['snapshots_dir'])

def list_snapshots():
    conf = h.parse_config(CONF_FILE)
    snapshots = h.list_dirs(conf['snapshots_dir'])
    fabric.utils.puts("\n".join(snapshots))

def restore(snapshot = "latest"):
    conf = h.parse_config(CONF_FILE)
    mongo_conf = conf['mongo']

    command = "mongorestore -h {0} -d {1} {2}"
    db_dir = os.path.join(snapshot, mongo_conf['db'])
    host = "{0}:{1}".format(mongo_conf['host'], mongo_conf['port'])

    with fabric.context_managers.lcd(conf['snapshots_dir']):
        fabric.operations.local(command.format(host, mongo_conf['db'], db_dir))

def clear_db():
    pass

def populate(filename = "populator_data.json"):
    data = populator.get_data(filename)
    ret = populator.populate(data)
    message = pprint.pformat(ret)
    fabric.utils.puts(message)

def populate_random(users = 15, min_board = 1, max_board = 10, min_tickets = 5, max_tickets = 25):
    data = populator.get_random_data(users, min_board, max_board, min_tickets, max_tickets)
    ret = populator.populate(data)
    message = pprint.pformat(ret)
    fabric.utils.puts(message)
