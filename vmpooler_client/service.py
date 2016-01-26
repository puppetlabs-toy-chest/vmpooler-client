"""
.. module:: vmpooler_client.lib.service
   :synopsis: Functions for communicating with the vmpooler API.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from httplib import HTTPConnection
from socket import gaierror
from json import loads
from base64 import standard_b64encode

#===================================================================================================
# Functions: Private
#===================================================================================================
def _make_request(method, host, path, body='', headers={}):
  """
  Makes an HTTP request.

  Args:
    method |str| = Type of request. GET, POST, PUT or DELETE.
    host |str| = The host and port of the server. E.g. vmpooler.myhost.com:8080
    path |str| = The path of the url. E.g. /vm/vm_name
    body |str| = The body data to send with the request.
    headers |{str:str}| = Optional headers for the request.

  Returns:
    |HTTPResponse| = Response from the request.

  Raises:
    |RuntimeError| = If the vmpooler URL can't be reached
  """

  try:
    conn = HTTPConnection(host)
    conn.request(method, path, body, headers)
    resp = conn.getresponse()

    return resp
  except gaierror:
    error = "Couldn't connect to address '{}'. Ensure this is the correct URL for " \
            "the vmpooler".format(host)
    raise RuntimeError(error)
  except:
    print("Unkown error occured while trying to connect to {}".format(host))
    raise


def _create_basic_auth_header(username, password):
  """
  Create request header for basic authentication.

  Args:
    username |str| = The username the header.
    password |str| = The password the header.

  Returns:
    |dict| = Header containing an "Authentication" key

  Raises:
    |None|
  """

  auth = standard_b64encode('{}:{}'.format(username, password)).replace('\n', '')
  headers = {'Authorization': 'Basic {}'.format(auth)}

  return headers


def _create_auth_token_header(auth_token):
  """
  Create request header which supplies an auth token.

  Args:
    auth_token |str| = The auth token

  Returns:
    |dict| = Header containing an "X-AUTH-TOKEN" key

  Raises:
    |None|
  """

  return {'X-AUTH-TOKEN': '{}'.format(auth_token)}


#===================================================================================================
# Functions: Public
#===================================================================================================
def create_auth_token(vmpooler_url, username, password):
  """
  Generate an authorization token.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    username |str| = The username for the authorization token request.
    password |str| = The password for the authorization token request.

  Returns:
    |str| = An authorization token.

  Raises:
    |RuntimeError| = The request was bad or incorrect credentials provided.
  """

  resp = _make_request('POST',
                       vmpooler_url,
                       '/token',
                       headers=_create_basic_auth_header(username, password))

  if resp.status == 401:
    raise RuntimeError('Failed to create authorization token because the provided credentials are '
                       'not authorized!')
  elif resp.status != 200:
    errmsg = ('Failed to create authorization token! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)

  return loads(resp.read())['token']


def get_token_info(vmpooler_url, auth_token, suppress_return=False):
  """
  Verify that an authorization token is still valid.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    auth_token |str| = The authorization token to validate.
    suppress_return |bln| = Suppress returning token information.

  Returns:
    |{str:str}| = A dictionary of token information.

  Raises:
    |RuntimeError| = The request was bad or incorrect credentials provided.
  """

  resp = _make_request('GET', vmpooler_url, '/token/{0}'.format(auth_token))

  if resp.status == 404:
    raise RuntimeError('Token already revoked or invalid token specified!')
  elif resp.status != 200:
    errmsg = ('Could not connect to vmpooler! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)

  if not suppress_return:
    return loads(resp.read())[auth_token]


def revoke_auth_token(vmpooler_url, username, password, auth_token):
  """
  Revoke an authorization token.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    username |str| = The username for the authorization token request.
    password |str| = The password for the authorization token request.
    auth_token |str| = The authorization token to revoke.

  Returns:
    |None|

  Raises:
    |RuntimeError| = The request was bad or incorrect credentials provided.
  """

  resp = _make_request('DELETE',
                       vmpooler_url,
                       '/token/{0}'.format(auth_token),
                       headers=_create_basic_auth_header(username, password))

  if resp.status != 200:
    errmsg = 'Token already revoked, invalid credentials provided or invalid token specified!'
    raise RuntimeError(errmsg)


def list_vm(vmpooler_url, auth_token):
  """Retrieve a list of availabe VM templates from the pooler.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    auth_token |str| = The authentication token for the user

  Returns:
    |[str]| = An array of template names.

  Raises:
    |RuntimeError| = The connection failed or the list of templates could not be
      retrieved for some reason.
  """

  resp = _make_request('GET',
                       vmpooler_url,
                       '/vm',
                       headers=_create_auth_token_header(auth_token))

  if resp.status != 200:
    errmsg = ('Could not connect to vmpooler! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)

  vmpooler_status = loads(resp.read())

  if len(vmpooler_status) == 0:
    raise RuntimeError('Could not retrieve list of templates!')

  return vmpooler_status


def get_vm(vmpooler_url, template_name, auth_token):
  """Retrieve a VM from the vmpooler and return the hostname.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    template_name |str| = The name of the template on the vmpooler.
    auth_token |str| = The authentication token for the user

  Returns:
    |str| = The hostname of the VM.

  Raises:
    |RuntimeError| = The connection failed or template could not be retrieved for some reason.
  """

  resp = _make_request('POST',
                       vmpooler_url,
                       '/vm/{0}'.format(template_name),
                       headers=_create_auth_token_header(auth_token))

  if resp.status == 404:
    raise RuntimeError('Could not retrieve template! Invalid template name provided!')
  elif resp.status != 200:
    errmsg = ('Could not connect to vmpooler! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)

  vmpooler_status = loads(resp.read())

  if not vmpooler_status["ok"]:
    raise RuntimeError('Could not retrieve template! The pool is drained for template!')

  return vmpooler_status[template_name]['hostname']


def info_vm(vmpooler_url, vm_name, auth_token):
  """Retrieve information for a VM in the vmpooler.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    vm_name |str| = The name of the VM from which to retrieve information.
    auth_token |str| = The authentication token for the user

  Returns:
    |{str:str}| = A dictionary of VM information.

  Raises:
    |RuntimeError| = The connection failed or template could not be retrieved for some reason.
  """

  resp = _make_request('GET',
                       vmpooler_url,
                       '/vm/{0}'.format(vm_name),
                       headers=_create_auth_token_header(auth_token))

  if resp.status == 404:
    raise RuntimeError('Could not find VM! Check the VM name and try again!')
  elif resp.status != 200:
    errmsg = ('Could not connect to vmpooler! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)

  return loads(resp.read())[vm_name]


def destroy_vm(vmpooler_url, vm_name, auth_token):
  """Hand a VM back to the vmpooler to be destroyed.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    vm_name |str| = The name of the VM (hostname) to destroy.
    auth_token |str| = The authentication token for the user

  Returns:
    |None|

  Raises:
    |RuntimeError| = The connection failed or invalid 'vm_name' was specified.
  """

  resp = _make_request('DELETE',
                       vmpooler_url,
                       '/vm/{0}'.format(vm_name),
                       headers=_create_auth_token_header(auth_token))

  if resp.status == 404:
    raise RuntimeError('The VM is already destroyed or wrong VM name provided!')
  elif resp.status != 200:
    errmsg = ('Could not connect to vmpooler! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)


def set_vm_lifetime(vmpooler_url, vm_name, lifetime, auth_token):
  """Set the time to live for a VM.

  Args:
    vmpooler_url |str| = The URL of the vmpooler
    vm_name |str| = The name of the VM (hostname) to set time to live.
    lifetime |int| = The number of hours to set the time to live for the VM.
    auth_token |str| = The authentication token for the user

  Returns:
    |None|

  Raises:
    |RuntimeError| = Invalid credentials specified or connection failure.
  """

  resp = _make_request('PUT',
                       vmpooler_url,
                       '/vm/{}'.format(vm_name),
                       body='{{"lifetime":"{}"}}'.format(lifetime),
                       headers=_create_auth_token_header(auth_token))

  if resp.status != 200:
    errmsg = ('Could not connect to vmpooler! '
              'Status Code: {0} Reason: {0}'.format(resp.status, resp.reason))
    raise RuntimeError(errmsg)

  vmpooler_status = loads(resp.read())

  if not vmpooler_status['ok']:
    raise RuntimeError('Invalid credentials provided!')
