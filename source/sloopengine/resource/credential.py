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


# Credential controller.
class credential(object):

  # Initializer.
  def __init__(self):
    self.account = {
      'url':main_conf['account']['url']
    }
    self.user = {
      'token':credential_conf['user']['token']
    }

  # Create Credential.
  def create(self,name):
    try:
      home_dir = '/home/%s' %(name)
      add_user = call(['useradd','-m','-s','/bin/bash','-d',home_dir,name],stdout=DEVNULL,stderr=STDOUT)
      if add_user!=0:
        raise
      call(['chmod','750',home_dir])
    except Exception as error:
      cprint('Error creating Credential.','red')
      sys.exit(1)
    else:
      cprint('Credential created.','green')

  # Configure Credential.
  def configure(self,name):
    try:
      home_dir = '/home/%s' %(name)

      def ssh_client(home_dir):
        conf_dir = '%s/.ssh' %(home_dir)
        conf_path = '%s/config' %(conf_dir)
        private_key_path = '%s/id_rsa' %(conf_dir)
        authorized_keys_path = '%s/authorized_keys' %(conf_dir)
        if os.path.exists(conf_dir) is False:
          os.mkdir(conf_dir)
          call(['chmod','700',conf_dir])
        if os.path.isfile(conf_path) is False:
          conf_file = open(conf_path,'wt')
          conf_file.write('Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile=/dev/null\n')
          conf_file.close()
          call(['chmod','600',conf_path])
        if os.path.isfile(private_key_path) is False:
          private_key_file = open(private_key_path,'a')
          private_key_file.close()
          call(['chmod','400',private_key_path])
        if os.path.isfile(authorized_keys_path) is False:
          authorized_keys_file = open(authorized_keys_path,'a')
          authorized_keys_file.close()
          call(['chmod','600',authorized_keys_path])
        call(['chown','-R','%s:%s' %(name,name),conf_dir])

      ssh_client(home_dir)
    except Exception as error:
      cprint('Error configuring Credential.','red')
      sys.exit(1)
    else:
      cprint('Credential configured.','green')

  # Update Credential.
  def update(self,name,key):
    try:
      home_dir = '/home/%s' %(name)

      def ssh_client(home_dir):
        conf_dir = '%s/.ssh' %(home_dir)
        private_key_path = '%s/id_rsa' %(conf_dir)
        authorized_keys_path = '%s/authorized_keys' %(conf_dir)
        if os.path.isfile(private_key_path) is True:
          private_key_file = open(private_key_path,'wt')
          private_key_file.write(key['private'])
          private_key_file.close()
        if os.path.isfile(authorized_keys_path) is True:
          authorized_keys_file = open(authorized_keys_path,'wt')
          authorized_keys_file.write(key['public'])
          authorized_keys_file.close()

      ssh_client(home_dir)
    except Exception as error:
      cprint('Error updating Credential.','red')
      sys.exit(1)
    else:
      cprint('Credential updated.','green')

  # Get Credential.
  def get(self,data):
    try:
      self.workspace = data['workspace']
      self.id = data['id']
      url = ''.join(
        '%s/API/Workspace/%s/Credential/%s'
        %(self.account['url'],self.workspace['id'],self.id)
      )
      headers = {
        'Authorization':''.join(
          '%s' %(self.user['token'])
        )
      }
      request = requests.get(url,headers=headers)
      response = request.json()
      if request.status_code==200 and response['status']=='success':
        credential_data = response['result']
      else:
        return
    except Exception as error:
      raise
    else:
      return credential_data

  # Sync Credential.
  def sync(self,data):
    try:
      credential_data = self.get(data)
      assert credential_data is not None,'Credential does not exist.'
      name = credential_data['name']
      key = {
        'private':credential_data['private_key'],
        'public':credential_data['public_key']
      } 
      if self.exist(name) is True:
        cprint('Credential exist.','yellow')
        self.update(name,key)
        sys.exit(0)
      self.create(name)
      self.configure(name)
      self.update(name,key)
    except AssertionError as error:
      cprint(error.args[0],'red')
      sys.exit(1)
    except Exception as error:
      cprint('Error syncing Credential.','red')
      sys.exit(1)
    else:
      cprint('Credential synced.','green')
      sys.exit(0)

  # Delete Credential.
  def delete(self,name):
    try:
      if self.exist(name) is True:
        delete_user = call(['userdel','-r',name],stdout=DEVNULL,stderr=STDOUT)
        if delete_user!=0:
          raise
      else:
        cprint('Credential does not exist.','red')
        sys.exit(1)
    except Exception as error:
      cprint('Error deleting Credential.','red')
      sys.exit(1)
    else:
      cprint('Credential deleted.','green')
      sys.exit(0)

  # Check Credential exist.
  def exist(self,name):
    id = call(['id',name],stdout=DEVNULL,stderr=STDOUT)
    if id==0:
      return True
    else:
      return False
