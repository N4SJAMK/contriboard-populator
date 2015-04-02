import fabric
import helper_functions as h

CONF_FILE = "conf.yml"

def take_snapshot(name = None):
    conf = h.parse_config(CONF_FILE)
    dir_name, err = h.create_dir(name)
    if err:
        fabric.utils.abort(err)

    mongo_conf = conf['mongo']
    command = "mongodump -h {0} -d {1} -o {2}"
    host = "{0}:{1}".format(mongo_conf['host'], mongo_conf['port'])

    with fabric.lcd(conf['snapshot_dirs']):
        fabric.local(command.format(host, mongo_conf['db'], dir_name))
        h.set_symlink("latest", dir_name)

def list_snapshots():
    conf = h.parse_config(CONF_FILE)
    snapshots = h.list_dirs(conf['snapshot_dirs'])
    fabric.utils.puts("\n".join(snapshots))

def restore(snapshot = "latest"):
    conf = h.parse_config(CONF_FILE)
    mongo_conf = conf['mongo']

    command = "mongorestore -h {0} -d {1} {2}"
    host = "{0}:{1}".format(mongo_conf['host'], mongo_conf['port'])

    with fabric.lcd(conf['snapshot_dirs']):
        fabric.local(command.format(host, mongo_conf['db'], snapshot))
