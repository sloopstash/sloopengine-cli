# Import community modules.
import os
import sys
import requests
from subprocess32 import call
from subprocess32 import DEVNULL,STDOUT
from termcolor import cprint

# Import custom modules.
from sloopengine.config import main_conf
from sloopengine.config import credential_conf


# Identity controller.
class identity(object):

  # Initializer.
  def __init__(self):
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
  def create(self,name):
    try:
      home_dir = '/home/%s' %(name)
      add_user = call(['useradd','-m','-s','/bin/bash','-d',home_dir,name],stdout=DEVNULL,stderr=STDOUT)
      if add_user!=0:
        raise
      call(['chmod','750',home_dir])
    except Exception as error:
      cprint('Error creating Identity.','red')
      sys.exit(1)
    else:
      cprint('Identity created.','green')

  # Configure Identity.
  def configure(self,name):
    try:
      home_dir = '/home/%s' %(name)

      def ssh_client(home_dir):
        conf_dir = '%s/.ssh' %(home_dir)
        conf_path = '%s/config' %(conf_dir)
        private_key_path = '%s/id_rsa' %(conf_dir)
        authorized_keys_path = '%s/authorized_keys' %(conf_dir)
        call(['mkdir',conf_dir])
        call(['chmod','-R','700',conf_dir])
        call(['touch',conf_path])
        call(['chmod','600',conf_path])
        call(['touch',private_key_path])
        call(['chmod','400',private_key_path])
        call(['touch',authorized_keys_path])
        call(['chmod','600',authorized_keys_path])
        call(['chown','-R','%s:%s' %(name,name),conf_dir])
        if os.path.isfile(conf_path):
          conf_file = open(conf_path,'wt')
          conf_file.write('Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile=/dev/null\n')
          conf_file.close()

      ssh_client(home_dir)
    except Exception as error:
      cprint('Error configuring Identity.','red')
      sys.exit(1)
    else:
      cprint('Identity configured.','green')

  # Update Identity.
  def update(self,name,key):
    try:
      home_dir = '/home/%s' %(name)

      def ssh_client(home_dir):
        conf_dir = '%s/.ssh' %(home_dir)
        private_key_path = '%s/id_rsa' %(conf_dir)
        authorized_keys_path = '%s/authorized_keys' %(conf_dir)
        if os.path.isfile(private_key_path):
          private_key_file = open(private_key_path,'wt')
          private_key_file.write(key['private'])
          private_key_file.close()
        if os.path.isfile(authorized_keys_path):
          authorized_keys_file = open(authorized_keys_path,'wt')
          authorized_keys_file.write(key['public'])
          authorized_keys_file.close()

      ssh_client(home_dir)
    except Exception as error:
      cprint('Error updating Identity.','red')
      sys.exit(1)
    else:
      cprint('Identity updated.','green')

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
      name = identity_data['name']
      key = {
        'private':identity_data['private_key'],
        'public':identity_data['public_key']
      } 
      if self.exists(name) is True:
        cprint('Identity already exists.','yellow')
        self.update(name,key)
        sys.exit(0)
      self.create(name)
      self.configure(name)
      self.update(name,key)
    except AssertionError as error:
      cprint(error.args[0],'red')
      sys.exit(1)
    except Exception as error:
      cprint('Error syncing Identity.','red')
      sys.exit(1)
    else:
      cprint('Identity synced.','green')
      sys.exit(0)

  # Delete Identity.
  def delete(self,name):
    try:
      if self.exists(name) is True:
        delete_user = call(['userdel','-r',name],stdout=DEVNULL,stderr=STDOUT)
        if delete_user!=0:
          raise
      else:
        cprint('Identity does not exist.','red')
        sys.exit(1)
    except Exception as error:
      cprint('Error deleting Identity.','red')
      sys.exit(1)
    else:
      cprint('Identity deleted.','green')
      sys.exit(0)

  # Check Identity exists.
  def exists(self,name):
    id = call(['id',name],stdout=DEVNULL,stderr=STDOUT)
    if id==0:
      return True
    else:
      return False
