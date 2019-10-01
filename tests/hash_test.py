# -*- coding:utf-8 -*-

from hashlib import blake2b
from hmac import compare_digest

h = blake2b(key=b'pseudorandom key', digest_size=16)
h.update(b'message data')
digest = h.hexdigest()
print(digest)

SECRET_KEY = b'pseudorandomly generated server secret key'
AUTH_SIZE = 16


def sign(cookie):
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(cookie)
    return h.hexdigest().encode('utf-8')



def verify(cookie, sig):
    good_sig = sign(cookie)
    return compare_digest(good_sig, sig)


cookie = b'user-alice'
sig = sign(cookie)
print("{0},{1}".format(cookie.decode('utf-8'), sig))
result = verify(cookie, sig)
print(result)

size = '0xffff'
a = int(size, 16)
print(a)
