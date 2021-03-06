#!/usr/bin/env python3

import os
import sys
import random
import time
import subprocess
import pwd

endings = {'ogg', 'mp3', 'wav', 'm4a'}


def runloop(directory):
    while True:
        print("Repeating the cycle!")
        choices = []
        for root, subdirs, files in os.walk(directory):
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
            try:
                # May need to swap between options if audio doesn't work               

                #opts = ['-ao','alsa:device=plughw=1.0']
                opts = []
                cmd = ["mplayer", '-novideo'] + opts + [c]
                print(cmd)
                subprocess.call(cmd, stdin=subprocess.DEVNULL,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            except subprocess.SubprocessError as e:
                print(e)
                pass

        print("Done with cycle!")
        time.sleep(5)

if __name__ == "__main__":
    user = pwd.getpwuid(os.getuid()).pw_name
    print(user)
    curr = os.path.realpath(__file__)
    if not curr.startswith("/home/"):
        print("Proper user could not be identified")
        quit()

    target = sys.argv[1] if len(sys.argv) == 2 else "/media/usb0"
    realuser = list(filter(None, curr.split('/')))[1]
    if user != realuser:
        os.system("sudo -u {} python3 {} {}".format(realuser, curr, target))
        quit()
    runloop(target)
