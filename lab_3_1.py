from random import randrange
from typing import Generator, Tuple

from lab_3_base import create_account, make_bet, to_signed_int32

MODULUS = 4294967296  # 2^32


def lcg(seed: int, a: int, c: int, m: int = MODULUS) -> Generator[int, None, None]:
    last = seed
    while True:
        last = (a * last + c) % m
        yield last


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def modinv(b: int, n: int) -> int:
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def find_increment(states, multiplier: int, modulus: int = MODULUS) -> Tuple[int, int, int]:
    increment = (states[1] - states[0] * multiplier) % modulus
    return modulus, multiplier, increment


def find_multiplier(states, modulus: int = MODULUS) -> Tuple[int, int, int]:
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return find_increment(states, multiplier, modulus)


def main():
    account = create_account()

    states = []
    amount = account.get("money", 0)
    is_hacked = False
    a = c = None
    while not is_hacked:
        play = make_bet(account["id"], 1, randrange(10000000))
        amount = play["account"]["money"]
        states.append(int(play["realNumber"]))

        # crack the casino
        if len(states) >= 3:
            try:
                _, a, c = find_multiplier(states[-3:])
                print("\nCasino is hacked: a={} c={}".format(a, c))
            except:
                print("\nHacking failure...")
            else:
                is_hacked = True

    # now we can play with all our money :)
    gen = lcg(states[-1], a, c)
    while amount < 1000000:
        winner_number = next(gen)
        play = make_bet(account["id"], amount, to_signed_int32(winner_number))
        amount = play["account"]["money"]

    print("\nCongratulations! You won ${:,.2f}".format(amount))
    print("a={} c={}".format(a, c))


if __name__ == '__main__':
    main()
