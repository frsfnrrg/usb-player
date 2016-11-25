#!/usr/bin/env python3

import tornado.web
import tornado.websocket
import os
import sys
import random
import pwd
import multiprocessing
import signal
import autoplay


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(
            "ui.html",
            items=items,
            sel=selected,
            iidx=items.index(selected))

wslist = []


class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print("WebSocket", len(wslist), "opened")
        wslist.append(self)

    def on_message(self, message):
        global selected, proc
        print(wslist.index(self), "got", message)
        if selected != message:
            selected = message
            idx = items.index(selected)
            for w in wslist:
                w.write_message(str(idx))
            # proc.kill()
            #os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            os.kill(proc.pid, signal.SIGINT)
            # proc.terminate()
            proc = multiprocessing.Process(
                target=autoplay.runloop, args=(selected,))
            proc.start()

    def on_close(self):
        print("WebSocket", wslist.index(self), "closed")
        wslist.remove(self)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/selection", EchoWebSocket),
    ])

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

    items = sorted({x[0] for x in os.walk(target)})
    selected = items[random.randint(0, len(items))]
    proc = multiprocessing.Process(target=autoplay.runloop, args=(selected,))
    proc.start()

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
