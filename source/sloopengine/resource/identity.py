# Import community modules.
import os
import sys
import requests
from subprocess32 import call
from termcolor import cprint

# Import custom modules.
from sloopengine.config import main_conf
from sloopengine.config import credential_conf


# Identity controller.
class identity(object):

  # Initializer.
  def __init__(self,**kwargs):
    self.account = {
      'url':main_conf['account']['url']
    }
    self.user = {
      'api_key':{
        'id':credential_conf['user']['api_key']['id'],
        'token':credential_conf['user']['api_key']['token']
      }
    }

  # Create Identity.
  def create(self,data):
    try:
      add_user = call(['useradd','-m','-s','/bin/bash','-d',data['home_dir'],data['name']])
      if add_user!=0:
        raise
      call(['chmod','-R','o-rwx',data['home_dir']])
      cprint('Identity created.','green')
    except Exception as Error:
      self.remove(data)
      cprint('Error creating Identity.','red')
      sys.exit(1)

  # Get Identity.
  def get(self,data):
    try:
      self.stack = data['stack']
      self.id = data['id']
      url = ''.join(
        '%s/API/Stack/%s/Identity/%s'
        %(self.account['url'],self.stack['id'],self.id)
      )
      headers = {
        'Authorization':''.join(
          'SloopEngine %s:%s'
          %(self.user['api_key']['id'],self.user['api_key']['token'])
        )
      }
      request = requests.get(url,headers=headers)
      response = request.json()
      if request.status_code==200 and response['status']=='success':
        identity_data = response['result']['identity']
      else:
        return
    except Exception as error:
      raise
    else:
      return identity_data

  # Sync Identity.
  def sync(self,data):
    try:
      identity_data = self.get(data)
      assert identity_data is not None,'Identity does not exist.'
      if self.exists(identity_data) is True:
        cprint('Identity already exists.','yellow')
        self.update_keys(identity_data)
        sys.exit(0)
      self.create(identity_data)
      self.configure(identity_data)
      self.update_keys(identity_data)
    except AssertionError as error:
      cprint(error.args[0],'red')
      sys.exit(1)
    except Exception as error:
      cprint('Internal error.','red')
      sys.exit(1)
    else:
      return Response

  # Delete Identity.
  def delete(self,params):
    data = self.get(params)
    if data['request'].status_code==200 and data['response']['status']=='success' and data['response'].has_key('result'):
      identity_data = data['response']['result']['identity']
      if self.exists(identity_data) is False:
        cprint('Identity does not exist.','yellow')
        sys.exit(1)
      self.remove(identity_data)
    else:
      cprint('Error deleting Identity.','red')
      sys.exit(1)

  # Check Identity exists.
  def exists(self,data):
    id = call(['id',data['name']])
    if id==0:
      return True
    else:
      return False



  # Configure Identity.
  def configure(self,data):
    try:
      def keys(data):
        call(['touch',data['home_dir']+'/.ssh/authorized_keys'])
        call(['chmod','600',data['home_dir']+'/.ssh/authorized_keys'])
        call(['touch',data['home_dir']+'/.ssh/id_rsa'])
        call(['chmod','400',data['home_dir']+'/.ssh/id_rsa'])

      def permission(data):
        call(['chmod','-R','700',data['home_dir']+'/.ssh'])

      def ownership(data):
        call(['chown','-R',data['name']+':'+data['name'],data['home_dir']+'/.ssh'])

      def settings(data):
        call(['touch',data['home_dir']+'/.ssh/config'])
        config_path = data['home_dir']+'/.ssh/config'
        if os.path.isfile(config_path):
          config_file = open(config_path,'wt')
          config_file.write('Host *\n\tStrictHostKeyChecking no\n')
          config_file.close()

      ssh_dir = call(['mkdir',data['home_dir']+'/.ssh'])
      if ssh_dir!=0:
        raise
      permission(data)
      keys(data)
      settings(data)
      ownership(data)
    except Exception as Error:
      self.remove(data)
      cprint('Error configuring Identity.','red')
      sys.exit(1)

  # Update Identity keys.
  def update_keys(self,data):
    try:
      authorized_keys = data['home_dir']+'/.ssh/authorized_keys'
      if os.path.isfile(authorized_keys):
        public_key = open(authorized_keys,'wt')
        public_key.write(data['public_key'])
        public_key.close()
      id_rsa = data['home_dir']+'/.ssh/id_rsa'
      if os.path.isfile(id_rsa):
        private_key = open(id_rsa,'wt')
        private_key.write(data['private_key'])
        private_key.close()
      cprint('Identity keys updated.','green')
    except Exception as Error:
      self.remove(data)
      cprint('Error updating Identity keys.','red')
      sys.exit(1)

  # Remove Identity.
  def remove(self,data):
    try:
      delete_user = call(['userdel','-r',data['name']])
      if delete_user!=0:
        raise
    except Exception as Error:
      cprint('Error deleting Identity.','red')
      sys.exit(1)
    else:
      cprint('Identity deleted.','green')
