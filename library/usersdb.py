#!/usr/bin/env python


class UsersDB(object):
    def __init__(self, module):
        self.module = module
        self.users_db = self.module.params["usersdb"]
        self.keys_db = {}  # used for quick lookup
        self.teams_db = self.module.params["teamsdb"]
        self.servers_db = self.module.params["serversdb"]
        self.expanded_users_db = []
        # Our final compiled DB to use
        self.expanded_server_db = []

    @staticmethod
    def concat_keys(user_keys, server_keys):
        # Override all user_key
        new_user_keys = []
        for user_key in user_keys:
            new_user_keys.append(dict(user_key, **server_keys))
        return new_user_keys

    def merge_key(self, user_keys, sever_keys, user_name):
        # Rules ( no real merge happens )
        # 1- Default use the user key
        # 2- if server has defined keys then use those instead no merge here
        if sever_keys:
            merged_keys = []
            for server_key in sever_keys:
                if "account" in server_key:
                    account_key = self.keys_db.get(server_key.pop("account"))
                    merged_keys += self.concat_keys(account_key, server_key)
                elif "team" in server_key:
                    pass
                elif "key" in server_key:
                    merged_keys.append(server_key)
                else:
                    self.module.fail_json(msg="user '{}' list has no keys defined.".format(user_name))
            return merged_keys
        else:
            return user_keys

    def merge_user(self, user_user_db, user_server_db, user_name):
        user_db_key = self.keys_db.get(user_name, None)
        merged_key = self.merge_key(user_db_key, user_server_db.get("keys", None), "static name")
        merged_user = dict(user_user_db.items() + user_server_db.items())
        merged_user.update({"keys": merged_key})
        return merged_user

    def expand_servers(self):
        # Expand server will overwrite same attributes defined in userdb except for state = "absent"
        for user_server in self.servers_db:
            # 1st lets get the user/team dictionary from the userdb
            user_name = user_server.get("user") or user_server.get("name", False)
            user_definition = self.users_db.get(user_name)
            team_definition = user_server.get("team", False)
            if user_name:
                if user_definition.get("state", "present") in ("absent", "delete", "deleted", "remove", "removed"):
                    # Don't merge you will delete any way
                    pass
                else:
                    # Merge User and Server ( Server has precedence in this case
                    user_server = self.merge_user(user_definition, user_server, user_name)

            elif team_definition:
                # TODO: Should expand teams
                pass
            else:
                self.module.fail_json(msg="Your server definition has no user or team. Please check your data type.")
            # Add the final merge
            self.expanded_server_db.append(user_server)

    def expand_keys(self, keys, user):
        if len(keys) == 0:
            # TODO: Should work without keys maybe ?!?!?
            self.module.fail_json(msg="user '{}' has no keys defined.".format(user))

        user_keys = []
        # If key is not a list than its a raw key string
        if not isinstance(keys, list):
            user_keys.append({"key": keys})
        else:
            for key in keys:
                # Basic syntax check
                if isinstance(key, basestring) and "ssh-" in key:
                    user_keys.append({"key": key})
                elif "key" not in key and "name" not in key:
                    self.module.fail_json(msg="user '{}' list has no keys defined.".format(key.keys()))
                else:
                    # All is okay just add the dict
                    user_keys.append(key)
        return user_keys

    def expand_users(self):
        # Get User database which is a dic and create expendaded_user_db and key_db
        # Put keys in right dictionary format
        for username, user_options in self.users_db.iteritems():
            # 1- Convert dic to list (servers_db style)
            user = {"name": username}  # create the account name
            user.update(user_options)  # update all other option
            # 2- Compile key
            unformatted_keys = user_options.get("keys", [])
            keys = self.expand_keys(unformatted_keys, user)
            user.update({"keys": keys})
            # 3- Populate DB
            self.expanded_users_db.append(user)  # Populate  new user db
            self.keys_db.update({username: keys})  # Populate key db

    def main(self):
        self.expand_users()
        if self.servers_db:
            # Check if we are customizing per server subgroup
            self.expand_servers()
            result = {"changed": False, "msg": "", "expanded_users_db": self.expanded_server_db, "key_db": self.keys_db}
        else:
            result = {"changed": False, "msg": "", "expanded_users_db": self.expanded_users_db, "key_db": self.keys_db}
        self.module.exit_json(**result)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            usersdb=dict(default=None, required=True, type="dict"),
            teamsdb=dict(default=None, required=True, type="dict"),
            serversdb=dict(default=None, required=False, type="list"),
        ),
        supports_check_mode=False
    )
    UsersDB(module).main()

# import module snippets
from ansible.module_utils.basic import *
main()
