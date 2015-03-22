#!/usr/bin/python


class LoadVarDir(object):
    def __init__(self, module):
        self.module = module
        self.path = self.module.params["path"]
        self.fact = self.module.params["fact"]
        self.data_bag = self.module.params["databag"]
        if self.data_bag:
            # Chef => Ansible mapping
            self.mapping = {"comment": "comment",
                            "force": "force",
                            "gid": "group",
                            "groups": "groups",
                            "home": "home",
                            "manage_home": "move_home",
                            "non_unique": "non_unique",
                            "password": "password",
                            "shell": "shell",
                            "action": "state",
                            "system": "system",
                            "uid": "uid",
                            "ssh_keys":  "keys"
                            }
        self.file_data = {}

    def main(self):
        self._read_path()
        result = {"changed": False, "msg": "Hi", self.fact: self.file_data}
        self.module.exit_json(**result)

    def _read_from_file(self, file_path):
        data = parse_yaml_from_file(file_path, vault_password="")
        if data and type(data) != dict:
            self.module.fail_json(msg="%s must be stored as a dictionary/hash".format(self.path))
        elif data is None:
            data = {}

        if self.data_bag:
            data = self.convert_chef_user_data_bag(data)
        return data

    def convert_chef_user_data_bag(self,data):
        if len(data) == 0:
            return data
        else:
            new_data = {}
            user_name = data.pop("id")  # Should fail if no id
            # Loop and only pick item in our map and translate it to ansible ignore the rest
            for mapping_key in self.mapping:
                data_bag_item_value = data.pop(mapping_key, None)
                if data_bag_item_value:
                    ansible_key = self.mapping.get(mapping_key)
                    new_data.update({ansible_key: data_bag_item_value})
            # Check for an action
            chef_action = new_data.get("state", False)
            if chef_action:
                if chef_action == "create":
                    new_data["state"] = "present"
                elif chef_action == "remove":
                    new_data["state"] = "absent"

            return {user_name: new_data}

    def _read_path(self):
        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                for root, dirs, files in os.walk(self.path, topdown=False):
                    for filename in files:
                        self.file_data.update(self._read_from_file(self.path + "/" + filename))
            else:
                self.file_data.update(self._read_from_file(self.path))
        else:
            self.module.fail_json(msg="Failed to find path '{}'.".format(self.path))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(default=None, required=True),
            fact=dict(default="var_dir", required=False),
            databag=dict(default=False, type='bool')
        ),
        supports_check_mode=False
    )
    if not ansible_client_found:
        module.fail_json(msg="Ansible is not installed or ansible python library is not in path")
    LoadVarDir(module).main()


# import module snippets
from ansible.module_utils.basic import *

try:
    from ansible.utils import parse_yaml_from_file
except ImportError:
    ansible_client_found = False
else:
    ansible_client_found = True

main()
