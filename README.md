ansible-usermanage
===

#NOTE:
*Major rewrite is going on so please hold on :) or use stable release* 

# TODO
Currently the playbook serves my needs, but I it lacks some features

* Finish rewrite of library
* Write test
* Support multiple user files and chef databag
* Support DB can be in get
* Syntax checks

#Why?

This playbook was developed to manage users and SSH keys in multi node environment. it does not and will not support passwords based authentication 
The idea is you define a user database in a YAML file, then define access in your host/group variable. This keeps things organized and easily add/change/remove mass users.

# Instruction
##Usersdb
This serves as our user database that holds global information about users. Here is an example 

```
LinuxUsers:
    daniels:
        fullname : 'Jack daniels'
        pubkey   : 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCootXD63hexEQnbCmKGC7DjFSWxkqJ2neaC5S6POEdgwo7jQ60JWy0VCm5JS5d2ZNDQh+vi1wZ2cTr6n9X9bAkYhQ/eACmzYBjf8I8AXcqaigAOjRMLADU2qQfZmnRGyOLaGDI/EH52yBjeZHbgQdJOGrB07qgAu2facA2bd6kvI8eLwCx5yjqA+mInYEewRYrr5tUduGFdPhmyoKSGpaEeWWkLhafTj9eGRMSB3unBcMtux+LxXH4TfWgVBmWNVbr2Mcv+M6tYxix/iKniBLBUH/AfM/dTHlk38y2mjemUMUc/HBW+HmH3NXMwOks8po6Iohh8JNhywUlLKN9MvB7'
       delete   : 
```
 * *daniels:* this is the unix account name  
 * *fullname:* Description name
 * *SSH key:* ssh key
 * *delete:* if defined will delete in all occurrence 

##Servers
The state of user(s) is defined per host or group variable. below is an example 
```
ServerAccess:
      #Simplest form (create testuser and push the testuser key defined in the userdb)
      - account     : "testuser"
        userkeys    :
             - user        : 'testuser'

      - account     : "ops"
        groups      : ""
        state       : "present"
        userkeys    :
             - user : 'ops'
               state: 'present'
               key_options : ''

             - user : 'stewart'
               state: 'present'
               key_options : ''

      - account     : "daniels"
        groups      : 'ops,lpadmin'
        state       : 'absent'
        shell       : '/bin/false' 
        remove      : 'no' 
        userkeys    :
             - user        : 'daniels'
               state       : 'present'
               key_options : 'no-port-forwarding'

      - account     : "stewart"
        groups      : ""
        state       : "present"
        userkeys    :
             - user        : 'stewart'
               state       : 'present'

             - user        : 'daniels'
               state       : 'present'
               key_options : '' 
```


