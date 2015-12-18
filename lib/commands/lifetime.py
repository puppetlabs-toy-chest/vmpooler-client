"""
.. module:: vmpooler_client.lib.commands.lifetime
   :synopsis: Sub-commands for the "lifetime" top-level command.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from ..conf_file import get_vmpooler_url, get_auth_token
from ..service import info_vm, set_vm_lifetime
from ..util import MAX_LIFETIME

#===================================================================================================
# Subcommands
#===================================================================================================
def get(args, config):
  """Main routine for the lifetime get subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  lifetime = info_vm(get_vmpooler_url(config), args.hostname, get_auth_token(config))["lifetime"]

  print("lifetime: {} hours".format(lifetime))


def set(args, config):
  """Main routine for the lifetime set subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  set_vm_lifetime(get_vmpooler_url(config), args.hostname, args.hours, get_auth_token(config))


def extend(args, config):
  """Main routine for the lifetime extend subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |RuntimeError| = If the new lifetime would exceed the maximum allowed lifetime
  """

  vm_info = info_vm(get_vmpooler_url(config), args.hostname, get_auth_token(config))
  running = round(float(vm_info["running"]))
  extension = int(args.hours)

  new_lifetime = int(running + extension)

  if not 0 < new_lifetime < MAX_LIFETIME:
    error = ('The new lifetime would be "{}"" hours. It should be between "0" and "{}"" '
             'hours'.format(new_lifetime, MAX_LIFETIME))
    raise RuntimeError(error)

  set_vm_lifetime(get_vmpooler_url(config), args.hostname, new_lifetime, get_auth_token(config))

  print("Lifetime extended to roughly {} hours from now".format(extension))
