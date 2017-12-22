# Setting up a Raspberry Pi Zero Server

## INSTALL RASPIAN ON SD CARD

### Get Latest raspian lite

```wget --trust-server-names https://downloads.raspberrypi.org/raspbian_lite_latest```

### Extract .zip
```unzip 2017-11-29-raspbian-stretch-lite.zip ```

*[replace name of file with the file that actually comes to you.]*

### Write the image to the SD Card
Connect your micro-sd card to your computer somehow. (I insert it into a full size adapter and then into a full sized SD card reader on my laptop.)

1. Find the SD card:

    ``` df -h ```

    The SD card should be near the bottom.

    *[if your not sure run ```df -h``` with the card out and then in and see what's different]*

1. unmount all mounted partitions

    `sudo umount /dev/mmcblk0p5`

    *[in my current case I only have 1, but previously I have seen 2.]*
1. write the image to the sd card.

    `sudo ddrescue -D --force ./2017-11-29-raspbian-stretch-lite.img /dev/mmcblk0`


### boot the pi
* put SD card in rasberry pi
* connect monitor
* connect keyboard
* connect power
* optional: connect Wired ethernet
* boot device
* log-in. *[username: pi password: raspberry]*

### initial setup

#### (Optional) Configure keyboard for Dvorak input
*[I'm weird]*

```sudo dpkg-reconfigure keyboard-configuration```

* choose "Generic 105-key (Intel) PC" [Default]
* then choose "Other" [because all are English (UK)]
* then choose "English (US)"
* then choose "English (US) - English (Dvorak)"
* then for "AltGr" choose "The default fro the keyboard layout"
* then for "Compose key" choose "No compose key"
* restart:

    `sudo shutdown -r now`

#### (optional) create new user and disable the default user
1. add user

    `sudo adduser newusername`

    *[follow prompts]*

1. make the new user a super user  

    `sudo adduser newusername sudo`

1. remove the pi user

    `sudo deluser pi`

#### Change password (!!!Absolutely required!!! if you didn't delete the pi user)
`passwd`

#### reqire password for sudo actions
   move (or delete if your really serious) /etc/sudoers.d/010_pi-nopasswd

   ```mv /etc/sudoers.d/010_pi-nopasswd ~```

#### Setup wifi networking

1. get hash of psk

    ```wpa_passphrase "<SSID>" "<psk>" > pass```

1. edit pass to contain only the psk value
   ```nano pass```

1. edit interfaces file

    ```sudo nano /etc/network/interfaces```

1. add the following lines

    ```
    auto wlan0
    allow-hotplug wlan0
    iface wlan0 inet dhcp
        wpa-ssid "<SSID>"
        wpa-psk 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    ```

    *[^R lets you insert a file at the curser position, do this with the psk saved in pass]*

1. if you have an usb wired NIC include the following

    ```
    auto eth0
    allow-hotplug eth0
    iface eth0 inet dhcp
    ```


1. restart pi zero

    ```sudo shutdown -r now```


### Update system

```
sudo apt update
sudo apt upgrade
```

### Install ssh

```
sudo apt install ssh
sudo update-rc.d ssh defaults
sudo update-rc.d ssh enable
```

restart pi zero

```sudo shutdown -r now```

connect to raspberry pi via ssh

```ssh username@192.0.2.100```



## Todo:

- [ ] much of this is likely to be ablet to be automated 
