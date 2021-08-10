# Import community modules.
import os
import sys
import argparse
import json
from subprocess32 import call
from textwrap import dedent
from termcolor import cprint


# Global variables.
version = '1.1.5'
base_dir = '/opt/sloopengine'
data_dir = '%s/data' %(base_dir)
log_dir = '%s/log' %(base_dir)
conf_dir = '%s/conf' %(base_dir)
main_conf_path = '%s/main.conf' %(conf_dir)
credential_conf_path = '%s/credential.conf' %(conf_dir)
main_log_path = '%s/main.log' %(log_dir)


# Import custom modules.
from sloopengine.includes.common import url_validate
from sloopengine.includes.common import api_key_id_validate
from sloopengine.includes.common import api_key_token_validate
from sloopengine.resource.identity import identity


# CLI controller.
class cli(object):

  # Constructor.
  def __new__(self):
    # Run only as sudo/root user.
    if not os.geteuid()==0:
      cprint('Run this command as sudo/root user.','red')
      sys.exit(1)
    return super(cli,self).__new__(self)

  # Initializer.
  def __init__(self):
    self.version = version
    self.base_dir = base_dir
    self.data_dir = data_dir
    self.log_dir = log_dir
    self.conf_dir = conf_dir
    self.main_conf_path = main_conf_path
    self.credential_conf_path = credential_conf_path
    self.main_log_path = main_log_path
    parser = argparse.ArgumentParser(
      prog='sloopengine',
      description=dedent('''
        SloopEngine CLI for managing resources and agent.

        Commands:
          init          Initialize CLI.
          configure     Configure CLI.
          identity      Manage Identities.
          agent         Manage Agent.
          version       Print CLI version.
      '''),
      formatter_class=argparse.RawDescriptionHelpFormatter,
      argument_default='version',
      usage='%(prog)s <command> [<args>]',
      add_help=True,
      allow_abbrev=True,
      epilog=dedent('''
        Website: https://sloopengine.io
        Email: support@sloopstash.com
      ''')
    )
    parser.add_argument(
      'command',
      nargs='?',
      default='version',
      choices=['init','configure','identity','agent','version']
    )
    args = parser.parse_args(sys.argv[1:2])
    if args.command=='init':
      self.initialize()
    elif args.command=='configure':
      self.configure()
    elif args.command=='identity':
      self.identity()
    elif args.command=='agent':
      self.agent()
    elif args.command=='version':
      cprint('SloopEngine CLI version: %s' %(self.version),'white')
      sys.exit(0)
    else:
      cprint('Invalid command.','red')
      sys.exit(1)

  # Initialize CLI.
  def initialize(self):
    try:
      if os.path.exists(self.base_dir) is False:
        os.mkdir(self.base_dir)
        call(['chmod','750',self.base_dir])
      if os.path.exists(self.data_dir) is False:
        os.mkdir(self.data_dir)
        call(['chmod','750',self.data_dir])
      if os.path.exists(self.log_dir) is False:
        os.mkdir(self.log_dir)
        call(['chmod','750',self.log_dir])
      if os.path.exists(self.conf_dir) is False:
        os.mkdir(self.conf_dir)
        call(['chmod','750',self.conf_dir])
      if os.path.isfile(self.main_conf_path) is False:
        main_conf_file = open(self.main_conf_path,'wt')
        main_conf_file.write(json.dumps({}))
        main_conf_file.close()
        call(['chmod','600',self.main_conf_path])
      if os.path.isfile(self.credential_conf_path) is False:
        credential_conf_file = open(self.credential_conf_path,'wt')
        credential_conf_file.write(json.dumps({}))
        credential_conf_file.close()
        call(['chmod','600',self.credential_conf_path])
      if os.path.isfile(self.main_log_path) is False:
        main_log_file = open(self.main_log_path,'a')
        main_log_file.close()
        call(['chmod','600',self.main_log_path])
      call(['chown','-R','root:root',self.base_dir])
    except Exception as error:
      cprint('Error initializing CLI.','red')
      sys.exit(1)
    else:
      cprint('CLI initialized.','green')
      sys.exit(0)

  # Configure CLI.
  def configure(self):
    try:
      assert os.path.exists(self.base_dir) is True,'CLI not initialized.'
      assert os.path.exists(self.conf_dir) is True,'CLI not initialized.'
      assert os.path.isfile(self.main_conf_path) is True,'CLI not initialized.'
      assert os.path.isfile(self.credential_conf_path) is True,'CLI not initialized.'
      params = {
        'main':{
          'account':{
            'url':None
          } 
        },
        'credential':{
          'user':{
            'api_key':{
              'id':None,
              'token':None
            }
          }
        }
      }
      params['main']['account']['url'] = input('Enter Account url: ')
      if url_validate(params['main']['account']['url']) is not True:
        sys.exit(1)
      params['credential']['user']['api_key']['id'] = input('Enter User API key identifier: ')
      if api_key_id_validate(params['credential']['user']['api_key']['id']) is not True:
        sys.exit(1)
      params['credential']['user']['api_key']['token'] = input('Enter User API key token: ')
      if api_key_token_validate(params['credential']['user']['api_key']['token']) is not True:
        sys.exit(1)
      main_conf_file = open(self.main_conf_path,'wt')
      main_conf_file.write(json.dumps(
        params['main'],indent=2,sort_keys=False)
      )
      main_conf_file.close()
      credential_conf_file = open(self.credential_conf_path,'wt')
      credential_conf_file.write(json.dumps(
        params['credential'],indent=2,sort_keys=False)
      )
      credential_conf_file.close()
    except AssertionError as error:
      cprint(error.args[0],'red')
      sys.exit(1)
    except Exception as error:
      cprint('Error configuring CLI.','red')
      sys.exit(1)
    else:
      cprint('CLI configured.','green')
      sys.exit(0)

  # Manage Identities using CLI.
  def identity(self):
    try:
      assert os.path.exists(self.base_dir) is True,'CLI not initialized.'
      assert os.path.exists(self.conf_dir) is True,'CLI not initialized.'
      assert os.path.isfile(self.main_conf_path) is True,'CLI not initialized.'
      assert os.path.isfile(self.credential_conf_path) is True,'CLI not initialized.'
      parser = argparse.ArgumentParser(
        prog='sloopengine identity',
        description=dedent('''
          Manage Identities using SloopEngine CLI.

          Commands:
            sync          Sync Identity.
            delete        Delete Identity from the machine.
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='%(prog)s [<args>]',
        add_help=True,
        allow_abbrev=True,
        epilog=dedent('''
          Website: https://sloopengine.io
          Email: support@sloopstash.com
        ''')
      )
      parser.add_argument('command',choices=['sync','delete'])
      parser.add_argument('--stack-id',type=int,metavar='<integer>',help='Stack identifier.')
      parser.add_argument('--id',type=int,metavar='<integer>',help='Identity identifier.')
      parser.add_argument('--name',metavar='<string>',help='Identity name.')
      args = parser.parse_args(sys.argv[2:])

      if args.command=='sync':
        if args.stack_id is None or args.id is None:
          cprint('Invalid args.','red')
          sys.exit(1)
        params = {
          'stack':{
            'id':args.stack_id
          },
          'id':args.id
        }
        identity().sync(params)
      elif args.command=='delete':
        if args.name is None:
          cprint('Invalid args.','red')
          sys.exit(1)
        identity().delete(args.name)
      else:
        cprint('Invalid command.','red')
        sys.exit(1)
    except AssertionError as error:
      cprint(error.args[0],'red')
      sys.exit(1)

  # Manage Agent using CLI.
  def agent(self):
    try:
      assert os.path.exists(self.base_dir) is True,'CLI not initialized.'
      assert os.path.exists(self.conf_dir) is True,'CLI not initialized.'
      assert os.path.isfile(self.main_conf_path) is True,'CLI not initialized.'
      assert os.path.isfile(self.credential_conf_path) is True,'CLI not initialized.'
      parser = argparse.ArgumentParser(
        prog='sloopengine agent',
        description=dedent('''
          Manage Agent using SloopEngine CLI.

          Commands:
            start       Start Agent.
            stop        Stop Agent.
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='%(prog)s <arg>',
        add_help=True,
        allow_abbrev=True,
        epilog=dedent('''
          Website: https://sloopengine.io
          Email: support@sloopstash.com
        ''')
      )
      parser.add_argument('command',choices=['start','stop'])
      args = parser.parse_args(sys.argv[2:])
      if args.command=='start':
        cprint('Agent not yet implemented.','red')
        sys.exit(0)
      elif args.command=='stop':
        cprint('Agent not yet implemented.','red')
        sys.exit(0)
      else:
        cprint('Invalid command.','red')
        sys.exit(1)
    except AssertionError as error:
      cprint(error.args[0],'red')
      sys.exit(1)
