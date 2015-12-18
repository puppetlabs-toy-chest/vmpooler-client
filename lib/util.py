"""
.. module:: vmpooler_client.lib.util
   :synopsis: Utility function used by other modules in the vmpooler_client package.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Globals
#===================================================================================================
# The maximum lifetime allowed for a VM reservation in hours.
MAX_LIFETIME = 1440

#===================================================================================================
# Functions: Public
#===================================================================================================
def pretty_print(dictionary, indent=0):
  """
  Pretty print a nested dictionary data structure.

  Args:
    dictionary |{}| = A nested dictionary of arbitrary depth.
    indent |int| = The level of indentation.

  Returns:
    |None|

  Raises:
    |None|
  """

  for key, value in dictionary.iteritems():
    print '  ' * indent + str(key) + ':'
    if isinstance(value, dict):
      pretty_print(value, indent + 1)
    elif isinstance(value, list):
      for item in value:
        print '  ' * (indent + 1) + '"{}"'.format(str(item))
    else:
      print '  ' * (indent + 1) + '"{}"'.format(str(value))
