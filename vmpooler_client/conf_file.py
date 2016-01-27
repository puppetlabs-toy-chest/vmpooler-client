"""
.. module:: vmpooler_client.lib.config
   :synopsis: Functions for reading and writing the configuration file.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from json import loads, dumps
from os import environ
from os.path import join, isfile
from platform import system
from getpass import getpass

#===================================================================================================
# Globals
#===================================================================================================
CONFIG_NAME = '.vmpooler.conf'

#===================================================================================================
# Functions: Public
#===================================================================================================
def locate_config():
  """
  Locate the configuration file path.

  Args:
    |None|

  Returns:
    |str| = The path to the configuration file.

  Raises:
    |RuntimeError| = Unsupported platform.
  """

  system_platform = system()

  # Locate path for configuration file.
  if (system_platform in ['Linux', 'Darwin']) or ('CYGWIN' in system_platform):
    config_path = join(environ['HOME'], CONFIG_NAME)
  elif system_platform == 'Windows':
    try:
      config_path = join(environ['APPDATA'], CONFIG_NAME)
    except KeyError:
      raise RuntimeError('Windows 2008 or greater is required to run this program!')
  else:
    raise RuntimeError('The platform "{}" is not supported '
                       'by this program!'.format(system_platform))

  return config_path


def write_config(config):
  """
  Write the configuration file for the program.

  Args:
    config |{str:str}| = A dictionary of settings for the configuration file.

  Returns:
    |None|

  Raises:
    |IOError| = Failed to write the configuration file.
  """

  config_path = locate_config()

  with open(config_path, 'w') as f:
    f.write(dumps(config))


def load_config():
  """
  Load the configuration file for the program.

  Args:
    |None|

  Returns:
    |{str:str}| = A dictionary of settings from the configuration file.

  Raises:
    |RuntimeError| = Unsupported platform, default configuration file or
      invalid configuration file.
  """

  config_path = locate_config()
  default_config = {'auth_token': ''}

  # Create configuration file if none exists.
  if not isfile(config_path):
    write_config(default_config)

  # Read configuration file.
  try:
    with open(config_path, 'r') as f:
      config = loads(f.read())
  except ValueError:
    # Invalid JSON file
    write_config(default_config)
    raise RuntimeError('The "{}" configuration file is invalid! '
                       'Replaced with default configuration file!\n'.format(locate_config()))

  return config


def get_auth_token(config):
  """Ensures an auth token exists. If a token is already present in the config, returns the token
  Otherwise prompts the user to create one or set one manually.

  Args:
    config |{str:str}| = A dictionary of settings from the configuration file.

  Returns:
    auth_token |str| = The user's auth token.

  Raises:
    |None|
  """

  if "auth_token" not in config or len(config["auth_token"]) == 0:
    error = ('Error: No authentication token found!\n\n'
      'Run the "token create" subcommand or manually update the\n'
      'configuration file with a valid authorization token using\n'
      '"vmpooler_client config set auth_token AUTH_TOKEN"')
    raise RuntimeError(error)

  return config["auth_token"]


def request_config_value(config, value_name, prompt=None):
  """Returns a config value if it exists.
  Otherwise asks for that value and saves to it the config

  Args:
    config |{str:str}| = A dictionary of configuration values.
    value_name |str| = The config value's name
    prompt |str| = An optional prompt to display. If none given, defaults to value_name

  Returns:
    |str| = The config value

  Raises:
    |None|
  """

  if not prompt:
    prompt = value_name

  if value_name not in config:
    config[value_name] = raw_input('{}: '.format(prompt))
    write_config(config)

  return config[value_name]


def get_credentials(config):
  """Request username and password from the user.
    If a username is found in the config, defaults to that username,
    otherwise requests a username and updates the config

  Args:
    config |{str:str}| = A dictionary of configuration values.

  Returns:
    |(username, password)| = A tuple of credentials.

  Raises:
    |None|
  """
  creds_title = 'Please provide LDAP credentials for the VM pooler\n'
  print(creds_title)

  if "username" not in config:
    config["username"] = request_config_value(config, "username", "Username")
  else:
    print "Using username: {}".format(config["username"])

  return (config["username"], getpass('Password: '))


def get_vmpooler_url(config):
  """Request the vmpooler URL from the user.
    If a URL is found in the config, defaults to that URL,
    otherwise requests a URL and updates the config

  Args:
    config |{str:str}| = A dictionary of configuration values.

  Returns:
    vmpooler_url |str| = The vmpooler url

  Raises:
    |None|
  """
  prompt = "Please enter the URL of the vmpooler. This will only be requested once"
  return request_config_value(config, "vmpooler_url", prompt)
