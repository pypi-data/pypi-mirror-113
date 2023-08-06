from hashlib import sha256
from random import SystemRandom
import pyperclip as pc
from pyqrcode import create
from dzh.hasher import Hasher


NONCE_MIN = 1000000
NONCE_MAX = 9999999


def get_sha256(raw_string):
    return sha256(raw_string.encode("utf-8")).hexdigest()


def get_prng():
    prng = SystemRandom()
    prn = prng.randint(NONCE_MIN, NONCE_MAX)
    print("Nonce: ", prn)
    return prn


def get_clipboard():
    try:
        return pc.paste()
    except RuntimeError:
        print("Error: xclip needed. Run “sudo apt install xclip”")
        return


class UI:
    def __init__(self):
        self.nonce = 0
        self.password = ""
        self.salt = ""
        self.secret = ""

    def create_secret(self):
        self.secret = Hasher(self.password, self.salt).generate()

    def check(self, password_confirm, salt_confirm):
        if self.password != password_confirm or self.salt != salt_confirm:
            return False
        return True

    def set_clipboard(self):
        try:
            pc.copy(self.secret)
        except RuntimeError:
            print("Error: xclip needed. Run “sudo apt install xclip”")
            return False
        return True

    def get_qrcode(self):
        qr = create(self.secret)
        qr.show()

