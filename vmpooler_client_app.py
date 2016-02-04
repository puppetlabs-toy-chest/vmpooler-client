#!/usr/bin/env python
"""
.. module:: vmpooler_client
   :synopsis: Manage resources in the vmpooler from the command-line.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
import sys
from vmpooler_client.conf_file import load_config
from vmpooler_client.command_parser import CommandParser, valid_lifetime
from vmpooler_client.commands import config, lifetime, token, vm

#===================================================================================================
# Functions: Private (Subcommands)
#===================================================================================================
def _configure_config_subcommands(cmd_parser):
  """Configure the subcommands for the "config" top-level command.

  Args:
    cmd_parser |vmpooler_client.command_parser.CommandParser| = The command parser.

  Returns:
    |None|

  Raises:
    |None|
  """

  parent = 'config'

  # Set Subcommand
  sub_cmd = 'set'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Set a config value',
                             func=config.set)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='key',
                                 help='The config option to set')
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='value',
                                 help='The value to set for the config option')

  # List Subcommand
  sub_cmd = 'list'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='List all the config settings',
                             func=config.list)

  # Get Subcommand
  sub_cmd = 'get'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Read a config value',
                             func=config.get)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='key',
                                 help='The config option to read')

  # Unset Subcommand
  sub_cmd = 'unset'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Remove a config option from the config',
                             func=config.unset)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='key',
                                 help='The config option to unset')


def _configure_lifetime_subcommands(cmd_parser):
  """Configure the subcommands for the "lifetime" top-level command.

  Args:
    cmd_parser |vmpooler_client.command_parser.CommandParser| = The command parser.

  Returns:
    |None|

  Raises:
    |None|
  """

  parent = 'lifetime'

  # Set Subcommand
  sub_cmd = 'set'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Set the total lifetime (in hours) for a VM instance',
                             func=lifetime.set)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='hostname',
                                 help='The hostname of the VM to set the lifetime expiry')
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='hours',
                                 help='The number of hours to set for the lifetime expiry',
                                 type=valid_lifetime)

  # Get Subcommand
  sub_cmd = 'get'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Get the lifetime (in hours) for a VM instance',
                             func=lifetime.get)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='hostname',
                                 help='Retrieve the lifetime expiry for VM hostname')

  # Extend Subcommand
  sub_cmd = 'extend'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Extend the lifetime (in hours) for a VM',
                             func=lifetime.extend)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='hostname',
                                 help='Extend the lifetime expiry for VM hostname')
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='hours',
                                 help='The number of hours to extend the lifetime expiry',
                                 type=valid_lifetime)


def _configure_token_subcommands(cmd_parser):
  """Configure the subcommands for the "token" top-level command.

  Args:
    cmd_parser |vmpooler_client.command_parser.CommandParser| = The command parser.

  Returns:
    |None|

  Raises:
    |None|
  """

  parent = 'token'

  # Create Subcommand
  cmd_parser.add_sub_command(parent,
                             'create',
                             desc='Generate an authorization token',
                             func=token.create)

  # Validate Subcommand
  sub_cmd = 'validate'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Validate an authorization token',
                             func=token.validate)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='token',
                                 help='The token to validate')

  # Revoke Subcommand
  sub_cmd = 'revoke'

  cmd_parser.add_sub_command(parent,
                             sub_cmd,
                             desc='Revoke an authorization token',
                             func=token.revoke)
  cmd_parser.add_sub_command_arg(parent,
                                 sub_cmd,
                                 name='token',
                                 help='The token to revoke')


def _configure_vm_subcommands(cmd_parser):
  """Configure the subcommands for the "vm" top-level command.

  Args:
    cmd_parser |vmpooler_client.command_parser.CommandParser| = The command parser.

  Returns:
    |None|

  Raises:
    |None|
  """

  parent = 'vm'

  # The string can't have tabs in it because they mess up the formatting
  list_help = """list available templates on VM pooler.
Optionally provide a search string to filter the platforms by.
The search string is matched fuzzily. For example:
"centos-6-x86" will be matched by any of the following:
"cos", "cent86", "tox", "centos86", but not:
"centosbob", "centos-6-x86bob", 'bobcos'.
  """

  # List Subcommand
  sub_cmd = 'list'

  cmd_parser.add_sub_command(parent, sub_cmd, desc=list_help, func=vm.list)
  cmd_parser.add_sub_command_arg(parent, sub_cmd, name='platform', nargs='?', default='')

  # Get Subcommand
  sub_cmd = 'get'

  cmd_parser.add_sub_command(parent, sub_cmd, desc='Get a vm from the pool', func=vm.get)
  cmd_parser.add_sub_command_arg(parent, sub_cmd, name='platform', help='The type of vm to aquire')

  # Info Subcommand
  sub_cmd = 'info'

  cmd_parser.add_sub_command(parent, sub_cmd, desc='Display VM information', func=vm.info)
  cmd_parser.add_sub_command_arg(parent, sub_cmd, name='hostname', help='The hostname of the VM')

  # Destroy Subcommand
  sub_cmd = 'destroy'

  cmd_parser.add_sub_command(parent, sub_cmd, desc='Destroy vm', func=vm.destroy)
  cmd_parser.add_sub_command_arg(parent, sub_cmd, name='hostname', help='VM hostname to destory')

  # Running Subcommand
  sub_cmd = 'running'

  cmd_parser.add_sub_command(parent, sub_cmd, desc='List running VMs', func=vm.running)

  # Destory All Subcommand
  sub_cmd = 'destroy_all'

  cmd_parser.add_sub_command(parent, sub_cmd, desc='Destroy all running VMs', func=vm.destroy_all)


#===================================================================================================
# Functions: Public
#===================================================================================================
def configure_command_parser(argv):
  """Configure the custom command parser.

  Args:
    argv |list| = List of CLI commands and arguments.

  Returns:
    |vmpooler_client.command_parser.CommandParser| = A custom command parser.

  Raises:
    |None|
  """

  # Custom parser for CLI commands and sub-commands
  cmd_parser = CommandParser(argv)

  # Top-level Commands
  cmd_parser.add_command('config', desc='Read and modify the vmpooler configuration file')
  cmd_parser.add_command('lifetime', desc='Manage the lifetime of VM instances')
  cmd_parser.add_command('token', desc='Manage auth tokens')
  cmd_parser.add_command('vm', desc='Discover and reserve VM instances')

  # Configure subcommands
  _configure_config_subcommands(cmd_parser)
  _configure_lifetime_subcommands(cmd_parser)
  _configure_token_subcommands(cmd_parser)
  _configure_vm_subcommands(cmd_parser)

  return cmd_parser


#===================================================================================================
# Main
#===================================================================================================
def main(argv):
  """Main program routine.

  Args:
    argv |sys.argv| = The raw command-line input from the user.

  Returns:
    |int| = The exit code to return to the shell.

  Raises:
    |None|
  """

  exit_code = 0

  try:
    config = load_config()
  except RuntimeError as e:
    print(e)
    # Should succeed the second time
    config = load_config()

  try:
    # Parse the command-line and validate user input
    cmd_parser = configure_command_parser(argv)

    # Execute the associated behavior with given sub-command and arguments
    cmd_parser.parse_execute(config=config)

    print('\nSuccess!')
  except RuntimeError as e:
    exit_code = 1
    print(e)
    print('\nFailed!')

  return exit_code


if __name__ == '__main__':
  sys.exit(main(sys.argv))
