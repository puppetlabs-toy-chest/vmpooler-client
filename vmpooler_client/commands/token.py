"""
.. module:: vmpooler_client.lib.commands.token
   :synopsis: Sub-commands for the "token" top-level command.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from ..conf_file import write_config, get_credentials, get_vmpooler_url
from ..service import create_auth_token, get_token_info, revoke_auth_token
from ..util import pretty_print

#===================================================================================================
# Subcommands
#===================================================================================================
def create(args, config):
  """Main routine for the token create subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """
  (username, password) = get_credentials(config)

  config['auth_token'] = create_auth_token(get_vmpooler_url(config), username, password)

  write_config(config)
  print('\nToken: {0}'.format(config['auth_token']))


def validate(args, config):
  """Main routine for the token validate subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  pretty_print(get_token_info(get_vmpooler_url(config), args.token))


def revoke(args, config):
  """Main routine for the token revoke subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  (username, password) = get_credentials(config)
  print('')
  revoke_auth_token(get_vmpooler_url(config), username, password, args.token)

  config['auth_token'] = ''

  write_config(config)
