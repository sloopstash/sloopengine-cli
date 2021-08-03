# Import community modules.
import os
import sys
import argparse
from textwrap import dedent
from termcolor import cprint


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
    parser = argparse.ArgumentParser(
      prog='sloopengine',
      description=dedent('''
        SloopEngine CLI for managing resources and agent.

        Commands:
          configure   Manage configuration.
          identity    Manage Identities.
          agent       Manage Agent.
          version     Print version.
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
      choices=['configure','identity','agent','version']
    )
    args = parser.parse_args(sys.argv[1:2])
    if args.command=='configure':
      self.configure()
    elif args.command=='identity':
      self.identity()
    elif args.command=='agent':
      self.agent()
    elif args.command=='version':
      self.version()
    else:
      cprint('Invalid command.','red')
      sys.exit(1)

  # Manage CLI configuration.
  def configure(self):
    cprint('Manage configuration.','green')

  # Manage Identities using CLI.
  def identity(self):
    parser = argparse.ArgumentParser(
      prog='sloopengine identity',
      description=dedent('''
        Manage Identity using SloopEngine CLI.

        Commands:
          sync          Sync Identity.
          rotate-keys   Rotate keys of an Identity.
          remove        Remove Identity from the machine.
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
    parser.add_argument(
      'command',
      choices=['sync','rotate-keys','remove']
    )
    args = parser.parse_args(sys.argv[2:])
    if args.command=='sync':
      cprint('Sync Identity.','green')
      sys.exit(0)
    elif args.command=='rotate-keys':
      cprint('Rotate keys of an Identity.','green')
      sys.exit(0)
    elif args.command=='clear':
      cprint('Remove Identity from the machine.','green')
      sys.exit(0)
    else:
      cprint('Invalid command.','red')
      sys.exit(1)

  # Manage Agent using CLI.
  def agent(self):
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
      cprint('Start Agent.','green')
      sys.exit(0)
    elif args.command=='stop':
      cprint('Stop Agent.','green')
      sys.exit(0)
    else:
      cprint('Invalid command.','red')
      sys.exit(1)

  # Print CLI version.
  def version(self):
    cprint('Print version.','green')
    sys.exit(0)
