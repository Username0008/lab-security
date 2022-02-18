from datetime import datetime
from lab_3_base import create_account, make_bet, mersenne_rng


def main():
    account = create_account()
    amount = account.get("money", 0)

    rng = mersenne_rng(seed=int(datetime.now().timestamp()))

    while amount <= 1000000 and amount != 0:
        winner_number = rng.get_random_number()
        play = make_bet(account["id"], amount, winner_number, mode="Mt")
        amount = play["account"]["money"]
    
    if amount != 0:
        print("\nCongratulations! You won ${:,.2f}".format(amount))
    else:
        print("\nGame over!")


if __name__ == '__main__':
    main()
