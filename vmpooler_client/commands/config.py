"""
.. module:: vmpooler_client.lib.commands.config
   :synopsis: Sub-commands for the "config" top-level command.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from ..conf_file import write_config
from ..util import pretty_print

#===================================================================================================
# Subcommands
#===================================================================================================
def list(args, config):
  """Main routine for the config list subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  pretty_print(config)


def get(args, config):
  """Main routine for the config get subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  try:
    print(config[args.key])
  except KeyError:
    raise RuntimeError('Config option "{}" is not set'.format(args.key))


def set(args, config):
  """Main routine for the config set subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  config[args.key] = args.value
  write_config(config)
  print("{}: {}".format(args.key, args.value))


def unset(args, config):
  """Main routine for the config unset subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  try:
    del config[args.key]
    write_config(config)
  except KeyError:
    print('The setting "{}" was not found in the configuration file!'.format(args.key))
    pass
