# Import community modules.
import json

# Import custom modules.
from sloopengine import main_conf_path
from sloopengine import credential_conf_path


# Load main.conf configuration file.
def main_conf(path):
  file = open(path,'r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  return conf

# Load credential.conf configuration file.
def credential_conf(path):
  file = open(path,'r')
  conf = file.read()
  conf = json.loads(conf)
  file.close()
  return conf


# Invoke functions.
main_conf = main_conf(main_conf_path)
credential_conf = credential_conf(credential_conf_path)
