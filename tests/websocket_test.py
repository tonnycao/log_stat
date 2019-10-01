import websocket
from threading import Thread
import time
import sys


def on_message(ws, message):
    print(message)


def parse_recv_data(msg):
    en_bytes = b''
    cn_bytes = []
    if len(msg) < 6:
        return ''
    v = msg[1] & 0x7f
    if v == 0x7e:
        p = 4
    elif v == 0x7f:
        p = 10
    else:
        p = 2
    mask = msg[p:p + 4]
    data = msg[p + 4:]
    for k, v in enumerate(data):
        nv = chr(v ^ mask[k % 4])
        nv_bytes = nv.encode()
        nv_len = len(nv_bytes)
        if nv_len == 1:
            en_bytes += nv_bytes
        else:
            en_bytes += b'%s'
            cn_bytes.append(ord(nv_bytes.decode()))
    if len(cn_bytes) > 2:
        # 字节数组转汉字
        cn_str = ''
        clen = len(cn_bytes)
        count = int(clen / 3)
        for x in range(0, count):
            i = x * 3
            b = bytes([cn_bytes[i], cn_bytes[i + 1], cn_bytes[i + 2]])
            cn_str += b.decode()
        new = en_bytes.replace(b'%s%s%s', b'%s')
        new = new.decode()
        res = (new % tuple(list(cn_str)))
    else:
        res = en_bytes.decode()
    return res


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(100):
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            ws.send("{'mobile':'18691495616','code':2,'data':'Hello %d'}"% i)
            time.sleep(1)

        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(False)
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImIyMzllMmI5MWI3N2E4ZmQxZGM2YTYyYzczMDI4N2U5NWZkZDRlMjA5NzcxMzIzZWQ4ZGIyOTVlYmJhNGQ1ZGQ3OTI4YzZjZDk1MjdjMmNhIn0.eyJhdWQiOiIyIiwianRpIjoiYjIzOWUyYjkxYjc3YThmZDFkYzZhNjJjNzMwMjg3ZTk1ZmRkNGUyMDk3NzEzMjNlZDhkYjI5NWViYmE0ZDVkZDc5MjhjNmNkOTUyN2MyY2EiLCJpYXQiOjE1NjA4NDU4ODQsIm5iZiI6MTU2MDg0NTg4NCwiZXhwIjoxNTYyMTQxODg0LCJzdWIiOiIxNDgiLCJzY29wZXMiOlsiKiJdfQ.nDIeUb52rf-MRch3fxANrWnZoiOW5NHer16NPbp8b7233fHJ4XIMx4X7naVgjzBq0mFkb2fwR332r4cIv6bzHoqE0xoU3N0lXk8dMPabjhumf9YQiRJasg1SFdYgo3IuIo5MO6fT0Kuq1_FDoipYomo9DyhNlyeJBPpQdcKgBG8u10_Qagvt8oIKrxTUPkLvrfshgR3uH-1Z-DyyJDqRTW_MhBXfjj5Ub7FFuPlsC9HEx8E2pprukk5kK3ToO-e2SmQfh9B7EJSB65L4EN2ds66ZqXolEv4PI5qqehobVkmisk9jH4ojFDw87I3huLxcwCtOFcc2tb6uVBX5uScC9g8FZOVjTpjTj-GbNZlhAlou7s-dTbjTfTXqHLD1uW2g3ZzzOxFp5XVwwcYAS_FxYrmfsknRYYQHdMBgwyfb5QVILy7w7CyLEf-MJ6ljJ7LnkXR4-ArL7x1lxlCci1V-_XipjfBp_pLlS_bxfHkUjXJds9jT7Ibpxpsb3WNaACgFb7--IfqkA-R7E80jvynmc9Kz5wY-CvCEmBFbESoOZmX4z7SjoBUtK7R5aCMGYcCVPXUiPiJ8uOSpGyniOfGdKKpO8yTFoJXT77a6FKl1Q4_ekr2l02ZVfwcc0cQCOnEF8-Tu91iAHu4Jd4DqcG8ObEQT6J1a02v2xPONqObt-fU'
    host = "ws://192.168.8.62:9509?token="+token
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()