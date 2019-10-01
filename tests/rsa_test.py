import base64
import rsa

with open('private_key.pem', mode='rb') as privatefile:
    keydata = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(keydata)


s = 'YNBfpTpib1iC+shXDrXwxsO3GkSwQ8jES7ZYjRKrnkqFIDSWaFnxsGJpKMEvL4IgSTFNx4sUTWwpmlTEqlMgOQcHrLIlNY9ZTZbeevwCKpf82C3XvzFOv4Am1ybUKp1Ri5BjlngNo/RmzcdAGUfwuc/jN/LiLMnV+6ryWh86vvU='
t = 'V0b0ioCQgQGpJgwMkV7sjvJRynATvycq2Bb4AOgA0EuHjGeACctMhfTfdFvirRRuv96mVmoaarR+hC3rxM2vnjGQwyuzYhn60vL4f46rTsWxhWeF14OiTocehGGy77kGZNP5sd59feNxh3z3dZVyG4uHzJkyD3pUCZJcwvp4RY0='
b = 'TdjdfzXkljh9tNfz730oBjIyqrSuEfEqIj5vBhif6jft0QGSkayEDAqGVicy/ytk3beTOt4hvC7xkRl16EQAIF6/FakT+iUhmJ0vUclYMDTPJMRLLpWaLun+Uv0b3yBAlICQZk0w1GeAdYHHID1amAhC3qT8nia1lTXtXL/IHI8='
a = 'C0nMzOOKwjrJ4x9bULJSsBfJ3mqPG8WXydCKtxLEycOBEfLwgkz7+5Jwu5iTTE8Yw0nVVjft/z/kgmudq0uvsYuRhP+LIZzhq6HBHVtYbNBcMuC68PZJubQyCIbOfdnPHk0YZEzZZsCOolWhkzbhYwnHpLvepe/Ui8hlmLFns4U='
c = 'G95K6K39asmSheUFVzuh3HyJRxdCZZPl9Tere9w40IF5GPxUnLlT4bOJV90S6KD6KPYq5bkD3pKyLMEG4xugndTLt96HR9noeicWWXh0jjdSXfvQEvmVnk9ONl2kOMHm0xRUxOrlh3fw0Wrp8Ssmirs11qzseZ92xhvFXmMoZC4='
d = 'JWIgz5gBDfzDAfX116SxOyN6ePs9VmZ40A7Ak1ViOmsMLri2N6kVmvvjH5UiIcVb0zDqwjmeV0JKoKpaqM8SjGOuA4zAtYA6bj5g/ssGPK9Vt6YL8URIv2t5JZkrZYLYRSnFPPU1t9KKKAy3MrdhZEk+imhAA5zbZ2pL+sfI63w='
e = 'ImcJk5jPbwwV65tAPkOwU5bkOLavONMNOXtawOcazeqmxpKlGUnRzXcbW0Bmf98/Nw1EkDmCB6GZas6Q5exIhPtJVTtdzhr7gq1F4rozyy+USV/pjGjxjsrcrNW/BqBp/CjSB4dO3W8iHOGkDlcI7SlL2DKqk390hYbPVUulzmI='
g = 'WmVDMZ1hPrU71EA9ZzE72BtQipMK78U6TvQDTM72UTtx4fC2mVBYkaS79oL0A0GIo31cXDUZWDf9WFwLriYaY6MKF/6NAdqEMbq5/guVQ4IJyP6jo+tS/5gac25NkikD+XJeAsA7y04tu2E4fvmeIK+V7HO57WLDw6MlKv5NToA='
f = 'bBhAiJz09qFb/vf3lR9RzpFzFcwvHsz927Z9Kt7l0q3UI4RAkspBdsAC53zUo6vn5vJ7R1fh7ryRZI+EcIfOnZCg1m1xZ07MMV4QEFpttkOQjmNqs8YXaFmW3IwR8ccUWaRni93L+jUESFNBzNUAl4Tldj8SD/SSFZxrr5U56T4='
h = 'Dth0cGzVT7qOcW60ZydApc80qlH6W2P0OPHlqU9OD77FCZW+odNPcmSFDRKx9/+AAJbPcfkrHLJmWnxpvOoPYMnfMQuelm3z7Q+gOxjW8+tewTMxgGZlR6wilV7o4pqjNIKxT/Bt4s2zRKw0KxyLcPjg2zpdxwoV05kZ8tgcn6w='
i = 'a+vswV9ETBlyjmcMMW3BY83nd7O6dj2MJL00dCb7+SL92iTbj7P/x4JakO0po0wxq8uv5uaL5zQQMv/mSsRDyu3cped3r6LUsrgB7uEnf6vwGri8m6vJGavwT7WXioK7UAILsgVhWGL/H4DzIV2NoIXGucCk/PfqXFYg74JxU1cFn8dlOgse6jSrhEXE+kKNjENv0Cjyh/DclTdCS6voKga2cW6KHGugYavLpcWRjGl8cemvHzri2scB9eWemcvF6ZrKHVy5VYhpKilUhGJY2iXXSRCnGxW/7HLrVHRUuZ7mAaI4Cf8bo0lrXlsXpPHYsPB5+sADTGpvlcBfm3ELuA=='
raw_str = base64.b64decode(i)
decrypt_str = str(rsa.decrypt(raw_str, privkey), encoding='utf-8')
print(decrypt_str)

with open('public.pem', mode='rb') as publicfile:
    data = publicfile.read()
    publikey = rsa.PublicKey.load_pkcs1(data)

print(publikey)
exit(0)
message = 'hello cj'.encode('utf-8')
crypto = rsa.encrypt(message, publikey)
base64_str = base64.b64encode(crypto)
print(str(base64_str))

# crypto = 'YNBfpTpib1iC+shXDrXwxsO3GkSwQ8jES7ZYjRKrnkqFIDSWaFnxsGJpKMEvL4IgSTFNx4sUTWwpmlTEqlMgOQcHrLIlNY9ZTZbeevwCKpf82C3XvzFOv4Am1ybUKp1Ri5BjlngNo' \
#          '/RmzcdAGUfwuc/jN/LiLMnV+6ryWh86vvU='.encode('utf-8')
# message = rsa.decrypt(crypto, privkey)
# print(message.decode('utf8'))

# (bob_pub, bob_priv) = rsa.newkeys(1024)
#
# priv = open('private.pem', mode='wb+')
# priv.write(bob_priv.save_pkcs1())
#
# pub = open('public.pem', mode='wb+')
# pub.write(bob_pub.save_pkcs1())

# message = 'https://www.v2ex.com/t/580970'.encode('utf8')
# crypto = rsa.encrypt(message, bob_pub)
# bs64 = base64.b64encode(crypto)
# print(bs64)
# data = base64.b64decode(bs64)
# message = rsa.decrypt(data, bob_priv)
# print(message.decode('utf8'))