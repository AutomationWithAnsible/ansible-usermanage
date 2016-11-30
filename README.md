ansible-usermanage
===

[![Build Status](https://travis-ci.org/AutomationWithAnsible/ansible-usermanage.svg?branch=master)](https://travis-ci.org/AutomationWithAnsible/ansible-usermanage)

## What

This role was developed to manage users, groups, teams, extra user information and SSH keys in multi node environment.


## How
### Simple Mode

You define your user in a variable *usermanage_usersdb*. You can define that differnetly per host our group.

```yaml
usermanage_usersdb:
  daniels:
    comment: "Jack daniels"
    state: "present"
    keys:
      - key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDLql1khoXEH/pThpLSDwJNBIEHkjrBggjEvRCqCFYvE1Neavc6iuLSzjLdnj74LNrPEjY+xcjAcPmgwxo8+WKpLL7Iy8e9IGH3lwB05x9jfnw2H1ZRnZZxF+wV/ei/vfCmRyt2cqv+DLomg18RDTnyTk2pvSEvL0xkRn5QRbzxqbnB+9xmItTjdtq/ZDYRgFYn2ZPfokFyyr3KpwpK0gNcpFhCF94CvExKpu6SFPTv+ERnFvHEN9d8SlzwkyCP4yqrfOjFuVUuZf2FtAkDx0d4cXo0i7VUM/hOthUNFpmljZLhkxafPxwp50Q/xRe7MvDQMrEPGPZ/pubOwzqVmMWH"
      - key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxAqbTlltSFlRY+gQyAx3j0W+WDnahZYbECAXiwNqAHG7PP8GSEDVkfZTkJdlu9PoB/B3nW2R/Q3//IxUfzRsUnjUzl0WXbhz331n5bHtgJlg82MGqwbNjN0yMR/GB4pQKeExYOLKi/7jI/wkOAJ4X9Bv9skEK/mHAWWPrBf/5C5qWUOxVC1+he3iaU+LSbiL6uiNs8S49fiGno8tBkBFgth+9gqdCLRAFVe2dzJJK1nSQTffHCs12pJs2S3yBD9KkUQJO51tByP4qO3549iwLo8hQnqtFULMpL+NN5Muk1bFZ2jW+0Sri1bhVS58llZCuoENZsLf/+xejbfwJAk4h"
        key_options: no-port-forwarding
  gin:
    comment: "Gordons Gin"
    keys:
      - key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcoo+eU8+k7QYpKbZwOQwiMpeklQcmEyLTsJr0RLTeqsHkIh8rFWyMZURDZ5pgEGo3iXZD+dqM28agy2Pw68/V0wht/9n0PjmUVZgkWIas162w3vZrJENDi8wAo4ojQJf0lZf63K8AxoB12fF+QdR7jfTLrz2bCxv9XaHKm7nYGtRO0f8ETgvwpIS2jN0mPAD7qnCFvLtbaxd/UzsQS5M8Au42+9zdn78Atm7gtKY9uR5U1Jwrop8KipXf0wAtMo39Xc9P8hGbYGA1jkbcG2x1LI7G9L+PddxeZjpkW2Uv559YJDRjBJfJAfp6K4HGV5uXITSMVDY9KBYvepolrlul"
    shell: /bin/zsh
    uid: 2300
  vodaka:
    comment: "Savvy Vodka"
    state: "absent"
    keys:
      - key: "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC2Pq3M7AgeBjmNII6HGsKd2uaXFIfaljpNg1Rf6y3iGP84wC82bMfZTSIhnzJ4qwHj7Bzn8oiMmqtyeGcmEwLXm5f7mk3lj9NmxUEfbuWsPoSX4VHIney0F2cjrYRAHua8vZ50OrqYvRaBNttx+pCsub/Kw/t91PQvz7s5ML12DfhlfbE5f/g+ZrKHBxsn6Vw0VqN1Cx5cecaN+9NbdwTV25/RVsXC6v9TQlIqWR+znt4ZVxUSCTAbGc51tmauoleZee2XBkAO7xmJ7zPQEndhErq/zm0euZGx1xGIjQ7dVBK8t1ah2UdBS4pSHgjhDulo0hr4gIubQ0FSV+8cWCNN"
```

Basically **usermanage_usersdb** is a dictionary of users each user will accept all options defined in [user ansible module](http://docs.ansible.com/user_module.html)

A special argument **keys** which is a list of keys that will be created for that user, each key can accept all options defined in [authorized key module](http://docs.ansible.com/authorized_key_module.html)

### Group Management
To manage groups you can define **usermanage_groupsdb** as a **list**. You must define atleast the *name* of group and optional state,gid and system.

```yaml
usermanage_groupsdb  :
      - name         : "group1"
        state        : "present"
        gid          : "5000"
        system       : "true"

      - name         : "group2"
        state        : "present"
        gid          : "5001"
        system       : "false"

      - name         : "group3"

      - name         : "group4"
        state        : "absent"
```

Some *nix system does not support creating the primary group for each user with the same name. If you want to enable that functionality for systems that does not support it. just enable that flag.
```yaml
usermanage_create_per_user_group            : true
```

### Users DB Sources
** TODO **

### Advanced mode
ToDo document

### teams
ToDo document

## Extra information

## Check mode


### Private Key
ToDo document


### Contributors
* [Adham Helal](https://github.com/ahelal)
* [Till Klocke](https://github.com/dereulenspiegel)
* [Leon George](https://github.com/yogo1212)
* [Marc Abramowitz](https://github.com/msabramo)
* [Mohannad Ali](https://github.com/mandoz)
