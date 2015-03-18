#!/usr/bin/env python


class UsersDB(object):
    def __init__(self, module):
        self.module = module
        self.users_db = self.module.params["usersdb"]
        self.teams_db = self.module.params["teamsdb"]
        self.servers_db = self.module.params["serversdb"]
        # Databases
        self.lookup_key_db = {}  # used for quick lookup
        self.expanded_users_db = []  # Used in simple mode
        self.expanded_users_key_db = []  # Used in simple mode
        self.expanded_server_db = []  # Used in advanced mode for merged User + server
        self.expanded_server_key_db = []  # Used in advanced mode

    def _concat_keys(self, user_name, user_keys=None, server_keys=None):
        # Concat keys (if possible) and update username to keys
        new_user_keys = []
        if user_keys and server_keys:
            for user_key in user_keys:
                new_user_key = dict(user_key, **server_keys)
                new_user_key.pop("name", None)
                new_user_key.pop("user", None)
                new_user_keys.append(new_user_key)
        elif server_keys:
            # server key is dic
            server_keys.pop("name", None)
            #server_keys.update({"user": user_name})
            new_user_keys = [server_keys]
        elif user_keys:
            for user_key in user_keys:
                new_user_key = user_key
                new_user_key.pop("name", None)
                new_user_key.pop("user", None)
                new_user_keys.append(new_user_key)
        else:
            self.module.fail_json(msg="user '{}' list has no keys defined.".format(user_name))
        return new_user_keys

    def _merge_key(self, user_keys, sever_keys, user_name):
        # Rules ( no real merge happens )
        # 1- Default use the user key
        # 2- if server has defined keys then use those instead no merge here
        if sever_keys:
            merged_keys = []
            for server_key in sever_keys:
                if "user" in server_key:
                    account_key = self.lookup_key_db.get(server_key.pop("user"))
                    merged_keys += self._concat_keys(user_name, account_key, server_key)
                elif "team" in server_key:
                    pass
                elif "key" in server_key:
                    merged_keys += self._concat_keys(user_name, server_keys=server_key)
                else:
                    self.module.fail_json(msg="user '{}' list has no keys defined.".format(user_name))
            return merged_keys
        else:
            return self._concat_keys(user_name, user_keys=user_keys)

    @staticmethod
    def _merge_user(user_user_db, user_server_db):
        merged_user = dict(user_user_db.items() + user_server_db.items())
        return merged_user

    def expand_servers(self):
        # Advanced mode Merges users and servers data
        # Expand server will overwrite same attributes defined in user db except for state = "absent"
        for user_server in self.servers_db:

            user_server_keys = None
            # 1st lets get the user/team dictionary from the user db
            user_name = user_server.get("user") or user_server.get("name", False)

            user_definition = self.users_db.get(user_name)
            team_definition = user_server.get("team", False)
            if user_name:
                if user_definition.get("state", "present") in ("absent", "delete", "deleted", "remove", "removed"):
                    # Don't merge you will delete any way
                    pass
                else:
                    # Merge User and Server ( Server has precedence in this case )
                    user_server = self._merge_user(user_definition, user_server)
                    user_db_key = self.lookup_key_db.get(user_name, None)
                    user_server_keys = self._merge_key(user_db_key, user_server.get("keys", None), user_name)
            elif team_definition:
                # TODO: Should expand teams
                self.module.fail_json(msg="Team is not yet implemented")
            else:
                self.module.fail_json(msg="Your server definition has no user or team. Please check your data type. "
                                          "for '{}'".format(user_server))
            # Populate DBs
            user_server.pop("keys", None)  # Get rid of keys
            self.expanded_server_db.append(user_server)
            self.expanded_server_key_db.append({"user": user_name, "keys": user_server_keys})

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
            # 3- remove keys from userdb if exists
            user.pop("keys", None)
            # 4- Populate DBs
            self.expanded_users_db.append(user)  # Populate new list user db
            self.expanded_users_key_db.append({"user": username, "keys": keys})
            self.lookup_key_db.update({username: keys})  # Populate dict key db

    def main(self):
        self.expand_users()
        if self.servers_db and self.servers_db[0] != "False":
            # Advanced mode we have to do merges and stuff :D
            self.expand_servers()
            result = {"changed": False, "msg": "",
                      "users_db": self.expanded_server_db,
                      "key_db": self.expanded_server_key_db}
        else:
            # Simple mode no servers db
            result = {"changed": False, "msg": "",
                      "users_db": self.expanded_users_db,
                      "key_db": self.expanded_users_key_db}
        self.module.exit_json(**result)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            usersdb=dict(default=None, required=True, type="dict"),
            teamsdb=dict(default=None, required=False, type=None), # Should be dict but would break if value is false/none
            serversdb=dict(default=None, required=False, type="list"),
        ),
        supports_check_mode=False
    )
    UsersDB(module).main()

# import module snippets
from ansible.module_utils.basic import *
main()
