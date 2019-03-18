### create new admin user
1. log-in.

    username: `pi`
    
    password: `raspberry`
    
1. add user

    (replace [username] with the name that you want your new admin user to be)

    `sudo adduser [newusername]`

    *(follow prompts)*

1. make the new user an admin user (i.e add the user to the `sudo` group)

    `sudo adduser [newusername] sudo`
    
### Delete the pi user 

   *(highly recommended)*

1. if you are loged in as the `pi` userlog-out

1. remove the pi user

    `sudo deluser pi`
    
 ### or Change password 
 
 *(highly recommended if you didn't delete the `pi` user)*

1.  log in as the `pi` user

1. change the password 

    `passwd`
    
    *(follow prompts)*

### require password for sudo actions 

*(more secure, less convenient)*

   move (or delete if your really serious) /etc/sudoers.d/010_pi-nopasswd
   
   `mv /etc/sudoers.d/010_pi-nopasswd ~`
   
   *(this command moves the flie to your home directory [`/home/username/`])*