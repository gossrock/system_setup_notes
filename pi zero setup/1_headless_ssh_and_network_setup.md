# Headless Setup of a Raspberry Pi Zero W

adapted from https://medium.com/@aallan/setting-up-a-headless-raspberry-pi-zero-3ded0b83f274

 https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address/37921#37921

 and

 https://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks


* ## Install Raspian Light image on SD card (see `pi zero setup/0_install_raspbian_on_sd_card_ubuntu.md`)

* ## insert the SD card (if it isn't already there)
* ## Enabling ssh
  * by default ssh is disabled
  * add an empty file called 'ssh' to the partition labeled 'boot'
    * navigate to the directory:
      * `cd /media/username/boot`
    * create the file:
      `touch ssh`
* ## Setup wireless for your network
  * navigate to the SD cards `boot` partition
    * `cd /media/username/boot`
  * create a file named `wpa_supplicant.conf` with the following information adjusted for your network:
    * `nano wpa_supplicant.conf`
      * variant 1 (basics):
        ```
        country=US
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1

        network={
         ssid="SSID"
         psk="PASSWORD"
         key_mgmt=WPA-PSK
        }
      ```
      * variant 2 (hashed psk):
        * if you don't want the password to be here in plain text you can do the following:
        * `wpa_passphrase "SSID" "PASSWORD"` (making the appropriate changes)
          * output:
            ```
            network={
            	ssid="SSID"
            	#psk="PASSWORD"
            	psk=c2161655c6ba444d8df94cbbf4e9c5c4c61fc37702b9c66ed37aee1545a5a333
            }
            ```
        * then edit the files in the boot partition (`nano wpa_supplicant.conf`):
          ```
          country=US
          ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
          update_config=1

          network={
           ssid="SSID"
           psk=c2161655c6ba444d8df94cbbf4e9c5c4c61fc37702b9c66ed37aee1545a5a333
           key_mgmt=WPA-PSK
          }
          ```
      * variant 3 (multiple SSIDs):
        * you can combine this one with variant 2
        * edit the wpa_supplicant.conf file on the boot partition like this:
          ```
          country=US
          ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
          update_config=1

          network={
                 ssid="SSID_1"
                 psk="PASSWORD_1"
                 key_mgmt=WPA-PSK
                 id_str="uniqueid1"
              }

          network={
                  ssid="SSID_2"
                  psk="PASSWORD_2"
                  key_mgmt=WPA-PSK
                  id_str="uniqueid2"
              }

          ```
      * variant 4 (multiple static ip and dhcp):
        * do valiant 3
        * then on the `rootfs` partition edit `/etc/network/inerfaces` file:
          ```
          auto lo
          iface lo inet loopback

          allow-hotplug wlan0
          iface wlan0 inet manual
          wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf

          iface uniqueid1 inet static
            address 192.168.0.100
            gateway 192.168.0.1
            netmask 255.255.255.0

          iface uniqueid2 inet dhcp
          ```
        * make sure that the uniqueid1 and uniqueid2 match the `wpa_supplicant.conf` file
        *
* ## USB-OTG / usb network setup
  * you will need to modify 2 files in the boot partition on the SD card
    * in the `config.txt` file add the line `dtoverlay=dwc2`
    * in the `cmdline.txt` file add `modules-load=dwc2,g_ether` just after `rootwait` (insure 1 space before and after)
  * to connect with USB-OTG on Ubuntu-Mate you will need to
    1. create an ethernet connection with 'IPv4' set to 'Shared to other computers'
    2. plug the USB cable into the USB port labeled 'USB' (Not the one labeled 'PWR')
    3. to obtain the ip address of the raspberry pi 0 run the command `avahi-resolve-host-name raspberrypi.local`
        * it may take a bit to report an IPv4 address instead of an IPv6 address
    4. after you see an IPv4 address you can now connect with 'ssh pi@raspberrypi.local' (you did put the empty 'ssh' 
    file in the boot partition didn't you)
  
  
 ## additional customizations
 
 #### change host name of raspberry pi 0
 
 1. change the host name `raspberrypi` in `/etc/hostname` (on raspberry pi 0) to what you want it to be:
    
    ```sudo nano hostname```
 
 2. change the hostname to mach in `/etc/hosts` (on raspberry pi 0):
 
    ``` sudo nano hosts```
    
 #### set usb ip address to be static
 1. edit '/etc/dhcpcd.conf' (on raspberry pi 0):
 
    ```sudo nano /etc/dhcpcd.conf``` 
 
 1. add the following lines to `/etc/dhcpcd.conf` (or similar):

    ```
        ###### connection via usb ######
        interface usb0
        static ip_address=10.42.0.103 # 103 can be your choice in range 2-254
        static routers=10.42.0.1

    ```
    
  #### connect more conveniently to raspberry pi 0 (on ubuntu)
  
  1. set your username for ssh to the raspberry pi and remove the need for '.local' when using ssh
  
     1. edit `~/.ssh/config` (on your ubuntu host)
     
        `nano ~/.ssh/config`
        
     2. add the following lines to that file (changing the '[]' info to the appropriate info)
     
        ```
            Host [raspberry pi host name]
            HostName [raspberry pi host name].local
            User [your user name on the raspberry pi]
        ```
  1. copy your ssh authorization key to pi so you no longer need to type your password 
  from your ubuntu host:
  
     1. `ssh-copy-id [your user name on the raspberry pi]@[raspberry pi host name]`
  
  1. additionally you may want to add a line in your '/etc/hosts' (on your ubuntu host) 
  so you can ping the host name or use the host name in your browser without '.local'
  
     1. `sudo nano /etc/hosts`
     2. add the following line `10.42.0.103     [raspberry pi host name]`
      