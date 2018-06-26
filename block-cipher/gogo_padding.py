#!/usr/bin/python -u

from Crypto.Cipher import AES
from Crypto import Random
from signal import alarm


class Scheme:
    def __init__(self,key):
        self.key = key
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS) 

    def unpad(self, raw):
        pad_checker = ord(raw[-1])
        if pad_checker == 0x00:
            return "No"

        for i in range(1, pad_checker+1):
            if ord(raw[-i]) != ord(raw[-1]):
                return "No"

        return raw[0:-ord(raw[-1])]


    def encrypt(self,raw):
        raw = self.pad(raw)

        iv = Random.new().read(self.BS)
        cipher = AES.new(self.key,AES.MODE_CBC,iv)

        return (iv + cipher.encrypt(raw)).encode("hex")

    def decrypt(self,enc):
        enc = enc.decode("hex")

        iv = enc[:self.BS]
        enc = enc[self.BS:]

        cipher = AES.new(self.key,AES.MODE_CBC,iv)
        blob = cipher.decrypt(enc)

        data = self.unpad(blob)

        if data == "No":
            print "Result: Padding error"
            return

        return True

key = Random.new().read(16)
scheme = Scheme(key)

flag = open("flag",'r').readline()
assert(len(flag) == 59)
alarm(300)

print "Welcome to theori encryption service!"
print scheme.encrypt(flag)
while True:
    data = raw_input().strip()
    result = scheme.decrypt(data)
    if result:
        print "Result: Check passed"
