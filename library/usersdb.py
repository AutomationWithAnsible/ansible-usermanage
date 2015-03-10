#!/usr/bin/env python


class UsersDB(object):
    def __init__(self, module):
        self.module = module
        self.users_db = self.module.params["usersdb"]
        self.teams_db = self.module.params["teamsdb"]
        self.servers_db = self.module.params["serversdb"]
        self.expanded_users_db = []

    @staticmethod
    def merge_user(user_definition, user_items):
        print user_definition
        print user_items
        return dict(user_definition.items() + user_items.items())

    def expand_servers(self):
        # Expand server will overwrite same attributes defined in userdb except for state = "absent"
        for a_user in self.servers_db:
            # 1st lets get the user/team dictionary from the userdb
            user_definition = a_user.get("user") or a_user.get("name", False)
            team_definition = a_user.get("team", False)
            if user_definition:
                if user_definition.get("state", None) in ("absent", "delete", "deleted", "remove", "removed"):
                    # Don't merge you will delete any way
                    pass
                else:
                    # merge do some magic
                    a_user = self.merge_user(user_definition.items(), a_user.items())

            elif team_definition:
                # Should expand teams
                pass
            else:
                self.module.fail_json(msg="Your server definition has no user or team. Please check your data type.")
            # Add the final merge
            self.expanded_users_db.append(a_user)

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

        for a_user, a_user_options in self.users_db.iteritems():
            # 1- Convert dic to list (servers_db style)
            a_user = {"name": a_user}  # create the account name
            a_user.update(a_user_options)  # update all other option
            # 2- Compile key
            a_keys = a_user_options.get("keys", [])
            a_user.update({"keys": self.expand_keys(a_keys, a_user)})
            self.expanded_users_db.append(a_user)

    def main(self):
        if self.servers_db:
            # Check if we are customizing per server subgroup
            self.expand_servers()
        else:
            # Simple just expand the user list
            self.expand_users()
        result = {"changed": False, "msg": "", "expanded_users_db": self.expanded_users_db}

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
