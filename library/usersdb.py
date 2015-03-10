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

    def merge_key(self, user_keys, sever_keys, user_name):
        # Rules ( no real merge happens )
        # 1- Default use the user key
        # 2- if server has defined keys then use those instead no merge here
        print "user_keys", user_keys
        print "sever_keys", sever_keys
        if sever_keys:
            user_keys = []
            for key in sever_keys:
                # Basic syntax check
                if "account" in key:
                    account_key = key.get("account")
                    return account_key
                elif "team" in key:
                    pass
                elif "key" in key:
                    pass
                else:
                    self.module.fail_json(msg="user '{}' list has no keys defined.".format(user_name))
        else:
            return user_keys

    def merge_user(self, user_definition, user_items):
        # print "ALLLLLL____user_definition", user_definition
        # print "ALL_user_items", user_items
        merged_key = self.merge_key(user_definition.get("keys", None), user_items.get("keys", None), "static name")
        merged_user = dict(user_definition.items() + user_items.items())
        merged_user.update({"keys": merged_key})
        return merged_user

    def expand_servers(self):
        # Expand server will overwrite same attributes defined in userdb except for state = "absent"
        for a_user in self.servers_db:
            # 1st lets get the user/team dictionary from the userdb
            user_name = a_user.get("user") or a_user.get("name", False)
            user_definition = self.users_db.get(user_name)
            team_definition = a_user.get("team", False)
            if user_name:
                if user_definition.get("state", "present") in ("absent", "delete", "deleted", "remove", "removed"):
                    # Don't merge you will delete any way
                    pass
                else:
                    # merge do some magic
                    a_user = self.merge_user(user_definition, a_user)

            elif team_definition:
                # Should expand teams
                pass
            else:
                self.module.fail_json(msg="Your server definition has no user or team. Please check your data type.")
            # Add the final merge
            self.expanded_server_db.append(a_user)

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
        # Get User database which is a dic i.e.
        # daniels:
        #     comment : 'Jack daniels'
        #     keys     :

        for username, user_options in self.users_db.iteritems():
            # 1- Convert dic to list (servers_db style)
            user = {"name": username}  # create the account name
            user.update(user_options)  # update all other option
            # 2- Compile key
            keys = user_options.get("keys", [])
            keys = self.expand_keys(keys, user)
            user.update({"keys": keys})
            # 3- Populate DB
            self.expanded_users_db.append(user)  # Populate  new user db
            self.keys_db.update({username: keys})  # Populate key db

    def main(self):
        # Simple just expand the user list
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
