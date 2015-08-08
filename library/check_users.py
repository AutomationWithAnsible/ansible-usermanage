#!/usr/bin/python

import pwd
import json
from ansible.module_utils.basic import *

NOOP_SHELL = [
  "/usr/sbin/nologin",
  '/bin/nologin',
  '/bin/false'
]

class CheckUsers(object):
  def __init__(self, module):
    self.module = module
    self.cusers = self.module.params["users_var"]
    self.fail_on_error = self.module["fail_on_error"]

  def main(self):
    users = pwd.getpwall()
    count = 0
    for user in users:
      name = user.pw_name
      shell = user.pw_shell
      uid = user.pw_uid
      home_dir = user.pw_dir

      if (uid > 999 and self.isValidShell(shell)):
        if not self.isUserNameInDb(name):
          self.exitWithResult("User {} not defined by ansible".format(name))
        else:
          self.checkUsersKeys(user)
      count = count + 1

    result = {"changed": False, "msg": "Checked {} user accounts".format(count)}
    self.module.exit_json(**result)

  def isUserNameInDb(self, name):

    for entry in self.cusers['users_db']:
      if entry['name'] == name:
        return True

    return False

  def isValidShell(self, shell):
    if shell in NOOP_SHELL:
      return False
    return True

  def checkUsersKeys(self, user):
    usersKeys = None

    for keys in self.cusers['key_db']:
      if keys['user'] == user.pw_name:
        usersKeys = keys
        break

    if usersKeys == None:
      self.exitWithResult("User {} has no ansible defined SSH keys".format(user.pw_name))

    installed_keys = self.loadInstalledAuthorizedKeys(user)
    configured_keys = []
    for key in usersKeys['keys']:
      configured_keys.append(key['key'])

    for key in installed_keys:
      if not key in configured_keys:
        self.exitWithResult("User {} has rogue ssh authorized keys".format(user.pw_name))


  def loadInstalledAuthorizedKeys(self, user):
    authorized_keys_file = os.path.join(user.pw_dir,'.ssh','authorized_keys')
    if not os.path.isfile(authorized_keys_file):
      self.exitWithResult("Can't load authorized keys from {} for user {}".format(authorized_keys_file, user.pw_name))
    with open(authorized_keys_file, 'r') as infile:
      data = infile.read()
    authorized_keys = data.splitlines()
    return authorized_keys

  def exitWithResult(self, message):
    if self.fail_on_error:
      self.module.fail_json(msg=message)
    else:
      self.module.exit_json(msg=message)
    

def main():
  module = AnsibleModule(
      argument_spec=dict(
          users_var=dict(default=None, required=True, type='dict')
          fail_on_error=dict(default=True, required=False, type='bool')
      ),
      supports_check_mode=False
  )
  CheckUsers(module).main()

if __name__ == '__main__':
    main()