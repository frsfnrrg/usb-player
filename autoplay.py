#!/usr/bin/env python3

import os, sys, random, time,subprocess,pwd

"""
Need: mplayer, mpg123, alsa, usbmount for usb automounting

Note: aplay -L and aplay --list-devices help for config options

# Here follows the appropriate systemd unit file

[Unit]
Description=Automatically play music from an mp3

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/odroid/bin/autoplay.py /media/usb0

[Install]
WantedBy=multi-user.target

"""

target = sys.argv[1] if len(sys.argv) == 2 else "/media/usb0"


user = pwd.getpwuid(os.getuid()).pw_name
print(user)
curr = os.path.realpath(__file__)
if not curr.startswith("/home/"):
     print("Proper user could not be identified")
     quit()

realuser = list(filter(None,curr.split('/')))[1]
if user != realuser:
   os.system("sudo -u {} python3 {} {}".format(realuser, curr, target))
   quit()

endings = {'ogg','mp3','wav','m4a'}
mounted = os.listdir(target)
while True:
     print("Repeating the cycle!")
     choices = []
     for root, subdirs, files in os.walk(target):
         for file in files:
              pth = os.path.join(root, file)
              for end in endings:
                  # skip paths with a dollar sign in them
                  if pth.endswith(end) and not "$" in pth:
                        choices.append(pth)
     random.shuffle(choices)
     for c in choices:
         if not os.path.exists(c):
             continue
         print("Playing:",c)
         try:
              #opts = ['-ao','alsa:device=plughw=1.0']
              opts = []
              cmd = ["mplayer",'-novideo']+opts+[c]
              print(cmd)
              subprocess.call(cmd,stdin=subprocess.DEVNULL)
         except subprocess.SubprocessError:
              pass

     print("Done with cycle!")
     time.sleep(5)


