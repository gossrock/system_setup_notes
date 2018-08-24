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
