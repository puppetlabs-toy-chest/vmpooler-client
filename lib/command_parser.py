"""
.. module:: vmpooler_client.lib.command_parser
   :synopsis: A class for configuring the command-line parser.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
import argparse
from util import MAX_LIFETIME

#===================================================================================================
# Functions: Public
#===================================================================================================
def valid_lifetime(lifetime):
  """Validate the lifetime argument.

  Args:
    argv |list| list of command line arguments

  Returns:
    |str| = The valid lifetime in hours.

  Raises:
    |argparse.ArgumentTypeError| If argument 'lifetime' is not a valid lifetime.
  """

  if 0 < int(lifetime) < MAX_LIFETIME:
    return lifetime
  else:
    error = 'The "lifetime" argument must be a value between "0" and "{}"!'.format(MAX_LIFETIME)
    raise argparse.ArgumentTypeError(error)


#===================================================================================================
# Classes: Public
#===================================================================================================
class CommandParser(object):
  """This class builds a command-line parser that uses a two-tiered command structure. Each
  top-level command can have multiple sub-commands. The sub-commands can accept an arbitrary
  number of arguments. Each sub-command can be tied to a function to implement desired behavior
  for the given sub-command.

  Args:
    argv |sys.argv| = The raw command-line input from the user.

  Raises:
    None
  """

  def __init__(self, argv):

    self._argv = argv

    # The main argument parser for commands and subcommands
    self._parser = argparse.ArgumentParser()

    # The argument parser for top-level commands. (i.e. "vm", "token")
    self._sub_parsers = self._parser.add_subparsers()

    self._commands = {}
    self._sub_commands = {}

  def add_command(self, cmd_name, desc):
    """Create a top-level command.

    Args:
      cmd_name |str| = The name of the command.
      desc |str| = A description of the command.

    Returns:
      None

    Raises:
      |KeyError| Command name has already been defined.
    """

    if cmd_name not in self._commands:
      command = self._sub_parsers.add_parser(cmd_name, description=desc)

      # Add a subparser for sub-commands under a top-level command. (i.e. "list" for "vm")
      self._commands[cmd_name] = command.add_subparsers()
    else:
      raise KeyError("The '{}' command has already been defined!".format(cmd_name))

  def add_sub_command(self, parent, sub_cmd_name, desc, func):
    """Create a sub-command for a top-level command.

    Args:
      parent |str| = The name of the parent top-level command.
      sub_cmd_name |str| = The name of the sub-command.
      desc |str| = A description of the sub-command.
      func |function| = A function to handle the request. The function must accept a positional
        argument followed by an arbitrary number of keyword arguments.

    Returns:
      |None|

    Raises:
      |KeyError| Command name has already been defined or parent command specified does not
        exist.
    """

    # Build unique key with composite of parent sub-command name.
    sub_cmd_key = "{}_{}".format(parent, sub_cmd_name)

    if parent not in self._commands:
      raise KeyError("The '{}' parent command has not been defined yet!".format(parent))
    elif sub_cmd_key in self._sub_commands:
      raise KeyError("The '{}' sub-command has already been defined!".format(sub_cmd_key))

    parent_command_sub_parser = self._commands[parent]

    self._sub_commands[sub_cmd_key] = \
      parent_command_sub_parser.add_parser(sub_cmd_name, description=desc)

    self._sub_commands[sub_cmd_key].set_defaults(func=func)

  def add_sub_command_arg(self, parent, sub_cmd_name, **kwargs):
    """Add an argument to a sub-command.

    Args:
      parent |str| = The name of the parent top-level command.
      sub_cmd_name |str| = The name of the sub-command.
      **kwargs |{str:obj}| = An arbitrary number of keyword arguments to pass to the
        "ArgumentParser.add_argument()" method. The "name" keyword argument *must* be
        supplied at a bare minimum!

    Returns:
      |None|

    Raises:
      |KeyError| The parent or sub-command specified does not exist. The **kwargs dictionary
        is missing the required "name" key.
    """

    # Build unique key with composite of parent sub-command name.
    sub_cmd_key = "{}_{}".format(parent, sub_cmd_name)

    if parent not in self._commands:
      raise KeyError("The '{}' parent command has not been defined yet!".format(parent))
    elif sub_cmd_key not in self._sub_commands:
      raise KeyError("The '{}' sub-command has not been defined yet!".format(sub_cmd_key))
    elif 'name' not in kwargs:
      raise KeyError("The keyword argument 'name' must be specified for this method!")

    arg_name = kwargs.pop('name')

    self._sub_commands[sub_cmd_key].add_argument(arg_name, **kwargs)

  def parse_execute(self, **kwargs):
    """Parse the command-line and execute the associated behavior with the given command.

    Args:
      **kwargs |{str:obj}| = An arbitrary number of keyword arguments to pass to the associated
        function for the given command and arguments.

    Returns:
      None

    Raises:
      None
    """

    args = self._parser.parse_args(args=self._argv[1:])

    # Execute the associated function for the given command and arguments.
    args.func(args, **kwargs)
