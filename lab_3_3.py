import sys
from random import randrange
from z3 import BitVec, BitVecVal, LShR, Solver

from lab_3_base import create_account, make_bet, mersenne_rng


def untemper(out):
    """
    This is the untemper function, i.e., the inverse of temper. This
    is solved automatically using the SMT solver Z3.
    """
    y1 = BitVec('y1', 32)
    y2 = BitVec('y2', 32)
    y3 = BitVec('y3', 32)
    y4 = BitVec('y4', 32)
    y = BitVecVal(out, 32)
    s = Solver()
    equations = [
        y2 == y1 ^ (LShR(y1, 11)),
        y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
        y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
        y == y4 ^ (LShR(y4, 18))
    ]
    s.add(equations)
    s.check()
    return s.model()[y1].as_long()


def recover_state_mt(numbers):
    """
    This function recovers the internal state of MT19937 given a
    sequence of outputs.
    """
    state = []
    for n in numbers[0:624]:
        state.append(untemper(n))
    return state


def main():
    account = create_account()

    numbers = []
    amount = account.get("money", 0)
    print("Retrieving real numbers from API. Please wait...")
    for i in range(624):
        play = make_bet(account["id"], 1, randrange(10000000), mode="BetterMt",
                        enable_logging=False)
        amount = play["account"]["money"]
        numbers.append(int(play["realNumber"]))
        sys.stdout.write("\r%d%% (%d of %d)" % ((100 * (i + 1) / 624), i + 1, 624))
        sys.stdout.flush()
    
    print("\nCloning MT19937 generator. Please wait...")
    recovered_state = recover_state_mt(numbers)
    cloned_rng = mersenne_rng()
    cloned_rng.state = recovered_state
    
    print("\nNow we can play with \"magic\" numbers :)")
    while amount < 1000000:
        winner_number = cloned_rng.get_random_number()
        play = make_bet(account["id"], amount, winner_number, mode="BetterMt")
        amount = play["account"]["money"]
    
    print("\nCongratulations! You won ${:,.2f}".format(amount))


if __name__ == '__main__':
    main()
