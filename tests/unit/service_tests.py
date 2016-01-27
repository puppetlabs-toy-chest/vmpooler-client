"""
.. module:: vmpooler_client.tests.unit.service_tests
   :synopsis: Unit tests for functions interacting with the vmpooler API.
   :platform: Unix, Linux, Windows
   :license: BSD
.. moduleauthor:: Ryan Gard <ryan.gard@puppetlabs.com>
.. moduleauthor:: Joe Pinsonault <joe.pinsonault@puppetlabs.com>
"""

#===================================================================================================
# Imports
#===================================================================================================
from vmpooler_client import service
from unittest import main, TestCase, skipIf
from mock import patch

#===================================================================================================
# Globals
#===================================================================================================
SKIP_EVERYTHING = False

#===================================================================================================
# Mocks
#===================================================================================================
class _HttpResponse(object):
  def __init__(self, status, return_value='default', reason='default'):
    self.status = status
    self.reason = reason
    self._return_value = return_value

  def read(self):
    return self._return_value

#===================================================================================================
# Tests
#===================================================================================================
class ServiceTests(TestCase):
  """Tests for the ResourceConfig class in the config module."""

  def setUp(self):
    self.vmpooler_url = 'vmpooler.delivery.puppetlabs.net'
    self.template_name = 'centos-4-x86_64'
    self.hostname = 'j2bgvv6x1ihqslx'
    self.auth_token = 'bdct6vxix5yfxndry32kmark0pyhriq9'

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test01_get_vm(self):
    """Happy path test to verify retrieving VM instances from the pooler."""

    # Construct mock return object.
    json_body = """
      {{
        "ok": true,
        "{0}": {{
          "hostname": "{1}",
          "ok": true
        }},
        "domain": "delivery.puppetlabs.net"
      }}""".format(self.template_name, self.hostname)

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      self.assertEqual(service.get_vm(self.vmpooler_url,
                                      self.template_name,
                                      self.auth_token),
                       self.hostname)

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test02_get_vm_neg(self):
    """Negative test case for attempting to retrieve non-existent VM instance."""

    # Construct mock return object.
    json_body = '{"ok": false}'

    resp = _HttpResponse(404, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      with self.assertRaises(RuntimeError) as cm:
        service.get_vm(self.vmpooler_url, self.template_name, self.auth_token)

        excep = cm.exception

        self.assertEqual(excep.msg,
                         'Could not retrieve template! Invalid template name provided!')

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test03_list_vm(self):
    """Happy path test to verify retrieving the list of available VM instances."""

    # Init
    expected_machines = ['fake_machine_1', 'fake_machine_1']

    # Construct mock return object.
    json_body = '[\n  "{0}",\n  "{1}"\n]'.format(expected_machines[0], expected_machines[1])

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      self.assertListEqual(service.list_vm(self.vmpooler_url,
                                           self.auth_token),
                           expected_machines)

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test04_info_vm(self):
    """Happy path test to verify retrieving info about a VM instance."""

    # Init
    expected_info = {"template": self.template_name,
                     "lifetime": 23,
                     "running": 6.7,
                     "state": "running",
                     "domain": "delivery.puppetlabs.net"}

    # Construct mock return object.
    json_body = """
      {{
        "ok": true,
        "{0}": {{
          "template": "{template}",
          "lifetime": {lifetime},
          "running": {running},
          "state": "{state}",
          "domain": "{domain}"
        }}
      }}""".format(self.hostname, **expected_info)

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      self.assertDictEqual(service.info_vm(self.vmpooler_url,
                                           self.hostname,
                                           self.auth_token),
                           expected_info)

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test05_destroy_vm(self):
    """Happy path test to verify destruction of VM instances."""

    # Construct mock return object.
    json_body = '{"ok": true}'

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      service.destroy_vm(self.vmpooler_url, self.hostname, self.auth_token)

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test06_destroy_vm_neg(self):
    """Negative test case for attempting to destroy non-existent VM instance."""

    # Construct mock return object.
    json_body = '{"ok": false}'

    resp = _HttpResponse(404, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      with self.assertRaises(RuntimeError) as cm:
        service.destroy_vm(self.vmpooler_url, self.hostname, self.auth_token)

        excep = cm.exception

        self.assertEqual(excep.msg, 'The VM is already destroyed or wrong VM name provided!')

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test07_set_vm_lifetime(self):
    """Happy path test to verify that the TTL can be manipulated on VM instances."""

    # Init
    lifetime = 25

    # Construct mock return object.
    json_body = '{"ok": true}'

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      service.set_vm_lifetime(self.vmpooler_url, self.hostname, lifetime, self.auth_token)

  @skipIf(SKIP_EVERYTHING, 'Skip if we are creating/modifying tests!')
  def test08_set_vm_lifetime_neg(self):
    """Negative test case for attempting to set TTL on VM instance with invalid credentials."""

    # Init
    lifetime = 25

    # Construct mock return object.
    json_body = '{"ok": false}'

    resp = _HttpResponse(200, json_body)

    # Patch
    with patch.object(service, '_make_request', return_value=resp) as mock_func:
      with self.assertRaises(RuntimeError) as cm:
        service.set_vm_lifetime(self.vmpooler_url, self.hostname, lifetime, self.auth_token)

        excep = cm.exception

        self.assertEqual(excep.msg, 'Invalid credentials provided!')
