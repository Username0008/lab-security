import os
import requests
from typing import Any, Tuple, Dict

API_URL = "http://95.217.177.249/casino"


def to_signed_int32(n: int):
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))


def input_int(message) -> int:
    while True:
        try:
            i = int(input(message))
            if i == 0:
                os._exit(0)
            return i
        except:
            pass


def _send_request_createacc(id_account: int) -> Tuple[Dict, Any]:
    query = {"id": id_account}
    r = requests.get("{}/createacc".format(API_URL), params=query)
    print("\n[INFO] GET {}".format(r.url))
    print("[INFO] RESPONSE: {} {}".format(r.status_code, r.json()))
    return r.json(), r


def create_account() -> Dict:
    has_account = False
    account = {}
    while not has_account:
        id = input_int("\nPlease enter an integer as player ID (or 0 to exit): ")
        account, r = _send_request_createacc(id)
        has_account = r.ok and "id" in account
    return account


def make_bet(id_account: int, amount: int, number: int, mode: str = "Lcg", enable_logging: bool = True) -> Dict:
    query = {
        'id': id_account,
        'bet': amount,
        'number': number
    }    
    r = requests.get("{}/play{}".format(API_URL, mode), params=query)
    
    if enable_logging:
        print("\n[INFO] GET {}".format(r.url))
        print("[INFO] RESPONSE: {} {}".format(r.status_code, r.json()))
    
    return r.json()


class mersenne_rng(object):
    def __init__(self, seed=5489):
        self.state = [0]*624
        self.f = 1812433253
        self.m = 397
        self.u = 11
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.index = 624
        self.lower_mask = (1 << 31)-1
        self.upper_mask = 1 << 31

        # update state
        self.state[0] = seed
        for i in range(1, 624):
            self.state[i] = self.int_32(
                self.f*(self.state[i-1] ^ (self.state[i-1] >> 30)) + i)

    def twist(self):
        for i in range(624):
            temp = self.int_32(
                (self.state[i] & self.upper_mask)+(self.state[(i+1) % 624] & self.lower_mask))
            temp_shift = temp >> 1
            if temp % 2 != 0:
                temp_shift = temp_shift ^ 0x9908b0df
            self.state[i] = self.state[(i+self.m) % 624] ^ temp_shift
        self.index = 0

    def temper(self, in_value):
        y = in_value
        y = y ^ (y >> self.u)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        return y

    def get_random_number(self):
        if self.index >= 624:
            self.twist()
        out = self.temper(self.state[self.index])
        self.index += 1
        return self.int_32(out)

    def int_32(self, number):
        return int(0xFFFFFFFF & number)
