# -*- coding: utf-8 -*-
from __future__ import (absolute_import,unicode_literals)
  
# Import community modules.
import os
import sys
import json
import requests
from subprocess32 import call
from termcolor import cprint

# Import custom modules.
from sloopengine.config import config


# Identity controller.
class identity(object):

  # Initializer.
  def __init__(self,**kwargs):
    self.system = {}
    self.account = {}
    self.user = {}
    self.system['base_home_dir'] = config['system']['base_home_dir']
    self.account['full_domain'] = config['account']['full_domain']
    self.account['scheme'] = config['account']['scheme']
    self.user['api_key_identifier'] = config['user']['api_key_identifier']
    self.user['api_key_token'] = config['user']['api_key_token']

  # Setup base home directory.
  def setup_base_home_dir(self):
    try:
      call(['mkdir','-p',self.system['base_home_dir']])
    except Exception as Error:
      cprint('Error setting-up system base home directory.','red')
      sys.exit(1)

  # Get Identity.
  def get(self,params):
    params = json.loads(params)
    request = requests.get(
      self.account['scheme']+'://'+self.account['full_domain']+'/API/Stack/'+str(params['stack_id'])+'/Identity/'+str(params['identity_id']),
      headers={'Authorization':'SLEN '+self.user['api_key_identifier']+':'+self.user['api_key_token']}
    )
    response = request.json()
    return {'request':request,'response':response}

  # Sync Identity.
  def sync(self,params):
    data = self.get(params)
    if data['request'].status_code==200 and data['response']['status']=='success' and data['response'].has_key('result'):
      identity_data = data['response']['result']['identity']
      if self.exists(identity_data) is True:
        cprint('Identity already exists.','yellow')
        identity_data['home_dir'] = self.system['base_home_dir']+'/'+identity_data['name']
        self.update_keys(identity_data)
        sys.exit(1)
      self.setup_base_home_dir()
      identity_data['home_dir'] = self.system['base_home_dir']+'/'+identity_data['name']
      self.create(identity_data)
      self.configure(identity_data)
      self.update_keys(identity_data)
    else:
      cprint('Error syncing Identity.','red')
      sys.exit(1)

  # Rotate Identity keys.
  def rotate_keys(self,params):
    params = json.loads(params)
    request = requests.get(
      self.account['scheme']+'://'+self.account['full_domain']+'/API/Stack/'+str(params['stack_id'])+'/Identity/'+str(params['identity_id'])+'/RotateKeys',
      headers={'Authorization':'SLEN '+self.user['api_key_identifier']+':'+self.user['api_key_token']}
    )
    response = request.json()
    if request.status_code==200 or response['status']=='success':
      cprint('Identity keys rotated.','green')
    else:
      cprint('Error rotating Identity keys.','red')
      sys.exit(1)

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
