#!/usr/bin/python

class LoadVarDir(object):
    def __init__(self, module):
        self.module = module
        self.path = self.module.params["path"]
        self.fact = self.module.params["fact"]
        self.data_bag = self.module.params["databag"]
        self.extract_extra_keys = self.module.params["extract_extra_keys"]
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

    def parse_yaml(self, data, path_hint=None):
        ''' convert a yaml string to a data structure.  Also supports JSON, ssssssh!!!'''

        stripped_data = data.lstrip()
        loaded = None
        if stripped_data.startswith("{") or stripped_data.startswith("["):
            # since the line starts with { or [ we can infer this is a JSON document.
            try:
                loaded = json.loads(data)
            except ValueError as ve:
                if path_hint:
                    self.module.fail_json(msg=path_hint + ": " + str(ve))
                else:
                    self.module.fail_json(msg=str(ve))
        else:
            # else this is pretty sure to be a YAML document
            loaded = yaml.load(data, Loader=Loader)
        return loaded

    def parse_yaml_from_file(self, path, vault_password=None):
        ''' convert a yaml file to a data structure '''
        data = None
        try:
            data = open(path).read()
        except IOError:
            self.module.fail_json(msg="file could not read: %s" % path)

        try:
            return self.parse_yaml(data, path_hint=path)
        except yaml.YAMLError as exc:
            self.module.fail_json(msg="Syntax error in yaml file '%s'" % path)

    def main(self):
        self._check_variable()
        result = {"changed": False, "msg": "Hi", self.fact: self.file_data}
        self.module.exit_json(**result)

    def _read_from_file(self, file_path, databag):
        data = self.parse_yaml_from_file(file_path, vault_password="")
        if data and type(data) != dict:
            self.module.fail_json(msg="%s must be stored as a dictionary/hash".format(file_path))
        elif data is None:
            data = {}

        if databag:
            data = self.convert_chef_user_data_bag(data)
        return data

    def convert_chef_user_data_bag(self, data):
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

            if self.extract_extra_keys:
                for key, value in data.iteritems():
                    new_data.update({key: value})
            # Check for an action
            chef_action = new_data.get("state", False)
            if chef_action:
                if chef_action == "create":
                    new_data["state"] = "present"
                elif chef_action == "remove":
                    new_data["state"] = "absent"
            chef_groups = new_data.get("groups", False)
            primary_group = new_data.get("group", False)
            if primary_group in chef_groups:
                # Databag issue for smart-os Issue
                chef_groups = [group_item for group_item in chef_groups if group_item != primary_group]
            new_data["groups"] = ",".join(chef_groups)
            return {user_name: new_data}

    def _check_variable(self):
        for path_item in self.path:
            try:
                path = path_item.get("path")
                path = os.path.expanduser(path)
                base_path = path_item.get("base_path", None)
                databag = path_item.get("databag", self.data_bag)
                #print "all={} type={} path={} databag={}".format(path_item, type(path_item), path, databag)
            except Exception as E:
                self.module.fail_json(msg="Path is a list but is malformed could not get 'path' got '{}'. Error '{}'".
                                      format(path_item, E))
            self._follow_path(path, databag, base_path)

    def _load_files(self,actual_path, databag):
        if os.path.isdir(actual_path):
            for root, dirs, files in os.walk(actual_path, topdown=False):
                for filename in files:
                    self.file_data.update(self._read_from_file(actual_path + "/" + filename, databag))
        else:
            self.file_data.update(self._read_from_file(path, databag))

    def _follow_path(self, path, databag, base_path=None):
        cwd = os.getcwd()
        if base_path:
            base_path = os.path.abspath(base_path+ "/" + path)

        if os.path.exists(path):
            self._load_files(path,databag)
        elif base_path and os.path.exists(base_path):
            self._load_files(base_path,databag)
        else:
            self.module.fail_json(msg="Failed to find path '{}'.".format(path), cwd=cwd, base_path=base_path)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(default=None, aliases=["path"], required=True, type='list'),
            fact=dict(default="var_dir", required=False),
            databag=dict(default=False, type='bool'),
            extract_extra_keys=dict(default=True, required=False)
        ),
        supports_check_mode=False
    )

    if not yaml_found:
        module.fail_json(msg="Python YAML module can't be imported, Please install it or check your python lib path")

    LoadVarDir(module).main()


# import module snippets
from ansible.module_utils.basic import *

try:
    import yaml
except ImportError:
    yaml_found = False
else:
    yaml_found = True
    try:
        from yaml import CSafeLoader as Loader
    except ImportError:
        from yaml import SafeLoader as Loader

main()
