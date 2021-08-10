# Import community modules.
import os
import json

# Import custom modules.
from sloopengine import main_conf_path
from sloopengine import credential_conf_path


# Load main.conf configuration file.
def main_conf(path):
  if os.path.isfile(path) is True:
    file = open(path,'r')
    conf = file.read()
    conf = json.loads(conf)
    file.close()
    return conf
  else:
    return {}

# Load credential.conf configuration file.
def credential_conf(path):
  if os.path.isfile(path) is True:
    file = open(path,'r')
    conf = file.read()
    conf = json.loads(conf)
    file.close()
    return conf
  else:
    return {}


# Invoke functions.
main_conf = main_conf(main_conf_path)
credential_conf = credential_conf(credential_conf_path)
