# Install Raspbian on SD card from Ubuntu

*(borrowed mostly from the instructions at http://ubuntu-mate.org/raspberry-pi/)*

* ## download image from raspbian download page
  * https://www.raspberrypi.org/downloads/raspbian/
    * (I use raspbian lite for the most part)
    * ### Method 1: Direct download
      * use browser
        * will download a file with a name similar to `2018-06-27-raspbian-stretch-lite.zip`
      * can be done from the command line as `wget https://downloads.raspberrypi.org/raspbian_lite_latest`
        * this will redirect and download the same file but the name will be `raspbian_lite_latest`
          * it is a zip file despite not having the '.zip' extension
    * ### Method 2: Torrent download
      * latest torrent url is: `https://downloads.raspberrypi.org/raspbian_lite_latest.torrent`
        * like the direct download this redirects to the current file and can be downloaded from the browser or with wget
          * it will have a date specific name if done from browser like `2018-06-27-raspbian-stretch-lite.zip.torrent`
          * it will be named the same as the original link if downloaded with wget: `raspbian_lite_latest.torrent`
      * open torrent file in `transmission` (default on ubuntu-mate) or other torrent downloader

* ## Extract zip file
  * You will have a zip file from the above
    * it may look something like: ```2018-06-27-raspbian-stretch-lite.zip```
    * if you used `wget` to direct download it may look like `raspbian_lite_latest`
  * ### Method 1: from file browser
    * right click and choose `extract here` or `extract to ...`
  * ### Method 2: from terminal
    * `unzip 2018-06-27-raspbian-stretch-lite.zip`
    * or (for the direct `wget` case) `unzip raspbian_late_latest`
  * in either method you will get a file like: `2018-06-27-raspbian-stretch-lite.img`

  * ## Figure out what your system calls your SD card
    * first `lsblk | grep disk` without the SD card to see what all your drives are called
      * you should see something like this:
    ```
    username@hostname$ lsblk | grep disk
    sda                                           8:0    0 931.5G  0 disk  
    sdb                                           8:16   0 232.9G  0 disk
    ```
    * next insert your SD card and `lsblk | grep disk` again to see what is new
      * you should see something new at the bottom like this:
    ```
    username@hostname$ lsblk | grep disk
    sda                                           8:0    0 931.5G  0 disk  
    sdb                                           8:16   0 232.9G  0 disk  
    mmcblk0                                     179:0    0   7.3G  0 disk
    ```
    * (you may only have one partition, but this is what it looks like after having installed it once)
    * you are looking for the "device name" of the SD card which in this case is `mmcblk0`
    *


* ## Write the image to the SD card
  * at the command line navigate to the directory where your image file is (if you are not there already)
  * modify the following command to match the information you have
    * `sudo ddrescue -D --force {raspbian image file name} /dev/{sdcard device name}`
    * example: `sudo ddrescue -D --force 2018-06-27-raspbian-stretch-lite.img /dev/mmcblk0`

* ## You are now ready to put the SD card into the raspberry pi for first boot


## Review by example

```
username@hostname$ cd ~/Downloads
username@hostname$ wget https://downloads.raspberrypi.org/raspbian_lite_latest
username@hostname$ unzip raspbian_lite_latest
username@hostname$ ls *raspbian*
2018-06-27-raspbian-stretch-lite.img
username@hostname$ lsblk | grep disk
sda                                           8:0    0 931.5G  0 disk  
sdb                                           8:16   0 232.9G  0 disk  

((( insert SD card )))

username@hostname$ lsblk | grep disk
sda                                           8:0    0 931.5G  0 disk  
sdb                                           8:16   0 232.9G  0 disk  
mmcblk0                                     179:0    0   7.3G  0 disk

username@hostname$ sudo ddrescue -D --force 2018-06-27-raspbian-stretch-lite.img /dev/mmcblk0
[sudo] password for username:
GNU ddrescue 1.22
     ipos:    1862 MB, non-trimmed:        0 B,  current rate:   4784 kB/s
     opos:    1862 MB, non-scraped:        0 B,  average rate:   7274 kB/s
non-tried:        0 B,  bad-sector:        0 B,    error rate:       0 B/s
  rescued:    1862 MB,   bad areas:        0,        run time:      4m 15s
pct rescued:  100.00%, read errors:        0,  remaining time:         n/a
                              time since last successful read:         n/a
Finished
```
