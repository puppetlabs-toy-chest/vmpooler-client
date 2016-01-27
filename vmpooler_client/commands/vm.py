"""
.. module:: vmpooler_client.lib.commands.vm
   :synopsis: Sub-commands for the "vm" top-level command.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from ..conf_file import get_vmpooler_url, get_auth_token
from ..service import get_vm, list_vm, info_vm, destroy_vm, get_token_info
from ..util import pretty_print

#===================================================================================================
# Functions: Private
#===================================================================================================
def _fuzzy_match(match, search_string):
  """
  Fuzzily matches match against search_string
  e.g.: a_long_variable_name can be matched by:
    alvn, aloname
  but not:
    a_bob, namebob, a_long_variable_name2

  Args:
    match |str| = The string to match against a list of strings
    search_string |str| = The string to match

  Returns:
    |bln| = Whether or not the string matches

  Raises:
    |None|
  """

  next_match = 0

  for match_char in match:
    next_match = search_string.find(match_char, next_match)
    # Bail out if there are no more matches
    if next_match < 0:
      return False

  return True


def _fuzzy_filter(match, string_list):
  """
  Filters out strings from a list of strings based on a fuzzy string match

  Args:
    match |str| = The string to match against a list of strings
    string_list |[str]| = The list of strings to match

  Returns:
    |[str]| = A list of strings that matched 'match'

  Raises:
    |None|
  """

  return [vm for vm in string_list if _fuzzy_match(match, vm)]


def _list_running_vms(vmpooler_url, auth_token):
  """Returns a list of the running vms for a given auth token.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    auth_token |str| = The authentication token for the user

  Returns:
    |None|

  Raises:
    |None|
  """

  token_info = get_token_info(vmpooler_url, auth_token)

  if "vms" in token_info:
    return token_info["vms"]["running"]
  else:
    return []


#===================================================================================================
# Subcommands
#===================================================================================================
def list(args, config):
  """Main routine for the list subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  search_string = args.platform
  templates = list_vm(get_vmpooler_url(config), get_auth_token(config))

  if search_string:
    templates = (template for template in _fuzzy_filter(search_string, templates))
    if not any(templates):
      print("No templates found matching '{0}'".format(search_string))

  for template in templates:
    print(template)


def get(args, config):
  """Main routine for the get subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  hostname = get_vm(get_vmpooler_url(config), args.platform, get_auth_token(config))
  print('Hostname: {0}'.format(hostname))


def info(args, config):
  """Main routine for the info subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  pretty_print(info_vm(get_vmpooler_url(config), args.hostname, get_auth_token(config)))


def destroy(args, config):
  """Main routine for the destroy subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  destroy_vm(get_vmpooler_url(config), args.hostname, get_auth_token(config))


def destroy_all(args, config):
  """Main routine for the destroy_all subcommand
     Destroys all running VMs created by the user.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |dict| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  vmpooler_url = get_vmpooler_url(config)
  auth_token = get_auth_token(config)
  vm_list = _list_running_vms(vmpooler_url, auth_token)

  for vm in vm_list:
    print("Destroying {}".format(vm))
    destroy_vm(vmpooler_url, vm, auth_token)

  if not vm_list:
    print("No VMs to destroy")


def running(args, config):
  """Main routine for the running subcommand.

  Args:
    args |argparse.Namespace| = A collection of arguments and flags.
    config |dict| = A dictionary of settings from the configuration file.

  Returns:
    |None|

  Raises:
    |None|
  """

  vmpooler_url = get_vmpooler_url(config)
  auth_token = get_auth_token(config)
  vm_list = _list_running_vms(vmpooler_url, auth_token)

  # Associate the hostname with its info
  vm_info_dict = dict((vm, info_vm(vmpooler_url, vm, auth_token)) for vm in vm_list)

  # Sort on how long they've been running
  sorted_vm_info = sorted(vm_info_dict.items(),
                          key=lambda (k, v): float(v["running"]),
                          reverse=True)

  for hostname, info in sorted_vm_info:
    print("{} | Running: {} hours | {}".format(hostname, info["running"], info["template"]))

  if not vm_list:
    print("No VMs running for this user")
