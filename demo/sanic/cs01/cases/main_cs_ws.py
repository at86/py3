# websocket-client
# https://github.com/websocket-client/websocket-client

# from websocket import create_connection
# ws = create_connection("ws://127.0.0.1:8000/wsreq")
# print("Sending 'Hello, World'...")
# ws.send("Hello, World")
# print("Sent")
# print("Receiving...")
# result =  ws.recv()
# print("Received '%s'" % result)
# ws.close()


import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(0.2)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def runWs():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/wsreq",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                )
    ws.on_open = on_open
    ws.run_forever()

import threading

tlist = []
for i in range(3):
    x = threading.Thread(target=runWs, args=())
    x.start()
    tlist.append(x)
for x in tlist:
    x.join()
