# How to setup Raspberry Pi for usage (and development)

## Connect to shared folder for development

Create mounting point:
'''
mkdir ~/wall-b
'''

Mount shared folder:
'''
sudo mount -t cifs //192.168.1.145/wall-b ~/wall-b -o username=wallb,password=Donno1999,uid=$(id -u wallb),gid=$(id -g wallb)
'''

Create permanent mount:

Install cifs-utils:
'''
sudo apt update
sudo apt install cifs-utils
'''

Add the following to fstab ('sudo nano /etc/fstab'):
'''
//192.168.1.145/wall-b /home/wallb/wall-b cifs username=wallb,password=Donno1999,uid=1000,gid=1000,iocharset=utf8 0 0
'''

## Get Coral working
- [https://www.youtube.com/watch?v=JF_P130v3AM](https://www.youtube.com/watch?v=JF_P130v3AM)