#!/usr/bin/env python


class UsersDB(object):
    def __init__(self, module):
        self.module = module
        self.users_db = self.module.params["usersdb"]
        self.teams_db = self.module.params["teamsdb"]
        self.servers_db = self.module.params["serversdb"]
        self.compiled_list = []

    def expand_servers(self):
        # Expand server will overwrite same attributes defined in userdb except for state = "absent"
        for a_user in self.servers_db:
            # 1st lets get the user/team dictionary from the userdb

            #team_definition = self.users_db.get("team")
            if a_user.get("user"):
                user_definition = self.users_db.get(a_user.get("user"))
                if user_definition.get("state", None) == "absent":
                    pass
                    # dont merge you will delete any way
                else:
                    # merge do some magic
                    # TODO: How to merge Keys and key options 
                    a_user = dict(user_definition.items() + a_user.items())

            elif a_user.get("team"):
                pass
            else:
                self.module.fail_json(msg="Your server definition has no user or team. Please check your data type.")
            # Add the final merge
            self.compiled_list.append(a_user)

    def expand_users(self):
        for a_user, a_user_options in self.users_db.iteritems():
            a_user = {"name": a_user}  # create the account name
            a_user.update(a_user_options)  # update all other option
            # Get pubkey
            a_user_key = a_user_options.get("pubkey", [])
            if len(a_user_key) == 0:
                self.module.fail_json(msg="user '{}' has no key defined.".format(a_user))

            compiled_keys = []
            if not isinstance(a_user_key, list):
                a_user_key = [a_user_key]

            for key in a_user_key:
                user_key = {}
                if isinstance(key, dict):
                    if key.get("state", None):
                        user_key.update({"state": key.get("state")})
                    if key.get("key_options", None):
                        user_key.update({"key_options": key.get("key_options")})
                    if key.get("pubkey", None):
                        user_key.update({"pubkey": key.get("pubkey")})
                else:
                    # just key
                    user_key.update({"pubkey": key})

                compiled_keys.append(user_key)
                a_user.update({"keys": compiled_keys})
            self.compiled_list.append(a_user)


    def main(self):
        if self.servers_db:
            # Check if we are customizing per server subgroup
            self.expand_servers()
        else:
            # Simple just expand the user list
            self.expand_users()
        result = {"changed": False, "msg": "", "compiled_list": self.compiled_list}

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
