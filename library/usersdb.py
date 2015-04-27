#!/usr/bin/python


class UsersDB(object):
    def __init__(self, module):
        self.module = module
        self.users_db = self.module.params["usersdb"]
        self.source_user_db = self.module.params["source_userdb"]
        # If we have to userdb and source db lets merge them if not
        if self.users_db and self.source_user_db:
            self.users_db.update(self.source_user_db)
        if self.source_user_db and not self.users_db:
            self.users_db = self.source_user_db
        if not self.users_db and not self.source_user_db:
            self.module.fail_json(msg="Missing argument. You must defined either 'usersdb' or 'source_userdb'.")

        self.teams_db = self.module.params["teamsdb"]
        self.servers_db = self.module.params["serversdb"]
        # Databases
        self.lookup_key_db = {}  # used for quick lookup
        self.expanded_users_db = []  # Used in simple mode
        self.expanded_users_key_db = []  # Used in simple mode
        self.expanded_server_db = []  # Used in advanced mode for merged User + server
        self.expanded_server_key_db = []  # Used in advanced mode

    def _concat_keys(self, user_name, user_keys=None, server_keys=None, user_status=False):
        # Concat keys (if possible) and update username to keys
        new_user_keys = []
        if user_keys and server_keys:
            for user_key in user_keys:
                new_user_key = dict(user_key, **server_keys)
                new_user_key.pop("name", None)
                new_user_key.pop("user", None)
                if user_status:
                    new_user_key.update({"state": "absent"})
                new_user_keys.append(new_user_key)
        elif server_keys:
            # server key is dic
            server_keys.pop("name", None)
            new_user_keys = [server_keys]
        elif user_keys:
            for user_key in user_keys:
                new_user_key = user_key
                new_user_key.pop("user", None)
                new_user_key.pop("name", None)
                if user_status:
                    new_user_key.update({"state": "absent"})
                new_user_keys.append(new_user_key)
        else:
            # TODO: Should work without keys
            # self.module.fail_json(msg="user '{}' list has no keys defined.".format(user_name))
            pass
        return new_user_keys

    def _merge_key(self, user_keys, sever_keys, user_name, user_status=False):
        # Rules ( no real merge happens )
        # 1- Default use the user key
        # 2- if server has defined keys then use those instead no merge here
        if sever_keys:
            merged_keys = []
            for server_key in sever_keys:
                if "user" in server_key:
                    user = server_key.pop("user", False)
                    account_key = self.lookup_key_db.get(user)
                    user_definition = self.users_db.get(user, {})
                    if user_definition.get("state", "present") in ("absent", "delete", "deleted", "remove", "removed"):
                        user_status = "absent"
                    merged_keys += self._concat_keys(user_name, account_key, server_key, user_status=user_status)
                elif "team" in server_key:
                    self.module.fail_json(msg="Team key is not yet implemented")
                elif "key" in server_key:
                    merged_keys += self._concat_keys(user_name, server_keys=server_key, user_status=user_status)
                else:
                    # TODO: Should work without keys
                    # self.module.fail_json(msg="user '{}' list has no keys defined.".format(user_name))
                    pass
            return merged_keys
        else:
            return self._concat_keys(user_name, user_keys=user_keys, user_status=user_status)

    def _merge_user(self, user_name, user_server):
        user_definition = self.users_db.get(user_name, False)

        if not user_definition:
            self.module.fail_json(msg="'%s' user has no definition" % user_name)

        if user_definition.get("state", "present") in ("absent", "delete", "deleted", "remove", "removed"):
            user_status = "absent"
        else:
            user_status = False

        # Merge User and Server ( Server has precedence in this case )
        merged_user = dict(user_definition.items() + user_server.items())

        if user_status:
            merged_user.update({"state": "absent"})
        user_server = merged_user
        user_db_key = self.lookup_key_db.get(user_name, None)
        user_server_keys = self._merge_key(user_db_key, user_server.get("keys", None), user_name, user_status)
        # In case of team user dict will not be defined so lets just define anyway
        user_server.update({"user": user_name})

        # Populate DBs
        user_server.pop("keys", None)  # Get rid of keys
        user_server.pop("team", None)  # Get rid of team if exists
        self.expanded_server_db.append(user_server)
        if len(user_server_keys) > 0:
            self.expanded_server_key_db.append({"user": user_name, "keys": user_server_keys})

    def expand_servers(self):
        # Advanced mode Merges users and servers data
        # Expand server will overwrite same attributes defined in user db except for state = "absent"
        for user_server in self.servers_db:
            team_name = user_server.get("team", False)
            user_name = user_server.get("user", False) or user_server.get("name", False)

            if user_name:
                self._merge_user(user_name, user_server)
            elif team_name:
                team_definition = self.teams_db.get(team_name, False)
                if not team_definition:
                    self.module.fail_json(msg="'%s' team has no definition" % team_name)
                for user_in_team in team_definition:
                    self._merge_user(user_in_team, user_server)
            else:
                self.module.fail_json(msg="Your server definition has no user or team. Please check your data type. "
                                          "for '{}'".format(user_server))

    def expand_keys(self, keys, user):
        # if len(keys) == 0:
        #     # TODO: Should work without keys
        #     self.module.fail_json(msg="user '{}' has no keys defined.".format(user))

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
                    # TODO: Should work without keys
                    # self.module.fail_json(msg="user '{}' list has no keys defined.".format(key.keys()))
                    pass
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
            if len(keys) > 0:
                self.lookup_key_db.update({username: keys})  # Populate dict key db

    def main(self):
        self.expand_users()

        if self.servers_db and len(self.servers_db) > 0:
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
            usersdb=dict(default=None, required=False, type="dict"),
            source_userdb=dict(default=None, required=False, type="dict"),
            teamsdb=dict(default=None, required=False),  # Should be dict but would break if value is false/none
            serversdb=dict(default=None, required=False),
        ),
        supports_check_mode=False
    )
    UsersDB(module).main()

# import module snippets
from ansible.module_utils.basic import *
main()
