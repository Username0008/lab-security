import binascii
import re
import sys
from typing import List

from colorama import init


LINES = [
    "280dc9e47f3352c307f6d894ee8d534313429a79c1d8a6021f8a8eabca919cfb685a0d468973625e757490daa981ea6b",
    "3a0a9cab782b4f8603eac28aadde1151005fd46a859df21d12c38eaa858596bf2548000e883d72117466c5c3a580f66b",
    "3a0adee4783a538403b9c29eaac958550242d3778ed9a61918959bf4ca849afa68450f5edc6e311a7f7ed1d7ec",
    "3a0adee461354e8c1cfcc39bef8d5e40525fdc6bc0dee359578290bcca849afa685a1e5c897362",
    "3a0adab0282b5c9719fcc38caac054541b449a62cf9df21d509690af858286f731091a4890786252",
    "390adeaa283358c318f0c08befc157061f59dd65dd9dee1c04c38fad839586ea3b0903489078",
    "390bcfac283a1d8111ebc8d8e8c2554d1b5e852dfed5e955008c8bb48ed094fe3a4d0b45883d731b7b609c",
    "3a0d9ba37a2e539750f8c39caade464313449a78c7d9e3075782deaf8f9180e66845074f9e31",
    "2c17cfe47c335c9750edc59daac9434313549a62cf9df51a1a868ab0839e95bf294f1a4c893d751b7b66d882",
    "3a0adee47d35598a03fac28eefdf54011610d962dcd3f2070ecfdebe989f9fbf3f41015a9e3d73116f60de",
    "200d9bb07a3a4b861cf5c88aaadf54520742d47e859df6000d9992bd99d086f72d09194097713d",
    "2f0cdfe4653a568603b9d88baadf50521a55c82dcbd8e707579796b79995d2f624451d098c7831167b64d5",
    "3a0adaaa283d519a50edc2d8e5d9594300439a79c1dcf2550086deb3849f85bf26461a09947b2e",
    "3a0aceb72838528d03fac49de4ce5406165fce6589d0e71e12c39db79d9180fb3b09014fdb68625e7b7edc82",
    "2f0cdfe47c33489050edc59daac350521b46df2dc1c8e3551885deaa8f839df33d5d074695",
    "27119bb76138568f19fcc9d8e58a54545247d379c19df21d12c38eb98695d2fc295a1a09947b310a727dc5c9a898a3",
    "2f0cdfe46d35498602e9df91f9c842061d569a6adbd8e701579397ac82d093f12c09034696787f0a",
    "390bcfac282f558a03b9df9dedcc43425244d268c0cfa61602918cbd848481bf3c5c1c47db7c660c63",
    "2f0cdfe464344e8650edc59daac3504b1710d56b89dce5011e8c90f6"
]
SPACE = ord(' ')
FREQUENT_WORDS = ["the", "and", "with", "of", "to"]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def is_space(rows: List[bytes], current: int, column: int) -> bool:
    for row in rows:
        result = row[column] ^ current
        if not (chr(result).isalpha() or result == 0):
            return False
    return True


def one_xor_two(one: bytes, two: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(one, two))


def colored_text(text: str) -> str:
    if re.match("^[a-zA-Z?.!,' ]+$", text):
        return f"{bcolors.BOLD}{bcolors.OKGREEN}{text}{bcolors.ENDC}"
    else:
        return f"{bcolors.BOLD}{bcolors.WARNING}{text}{bcolors.ENDC}"


def query_yes_no(question: str, default: str = "yes") -> bool:
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def decrypt(ciphertexts: List[bytes], clear_texts: List[bytearray], input_key: str) -> None:
    key = binascii.unhexlify(input_key.rstrip())
    for i in range(len(ciphertexts)):
        for j in range(len(ciphertexts[i])):
            clear_texts[i][j] = ciphertexts[i][j] ^ key[j % len(key)]
        print(clear_texts[i].decode('utf-8'))


def attack(ciphertexts: List[bytes], clear_texts: List[bytearray], is_print: bool = True) -> List[bytearray]:
    max_length = max(len(line) for line in ciphertexts)
    for j in range(max_length):
        pending_ciphers = [line for line in ciphertexts if len(line) > j]
        for cipher in pending_ciphers:
            if is_space(pending_ciphers, cipher[j], j):
                i = 0
                for clear_row in range(len(clear_texts)):
                    if len(clear_texts[clear_row]) != 0 and j < len(clear_texts[clear_row]):
                        result = cipher[j] ^ pending_ciphers[i][j]
                        if result == 0:
                            clear_texts[clear_row][j] = SPACE
                        elif chr(result).isupper():
                            clear_texts[clear_row][j] = ord(chr(result).lower())
                        elif chr(result).islower():
                            clear_texts[clear_row][j] = ord(chr(result).upper())
                        i += 1
                break
    if is_print:
        print('\n'.join("{0:<2}: {1}".format(i + 1, line.decode('utf-8')) for i, line in enumerate(clear_texts)))
    return clear_texts


def manual_attack(ciphertexts: List[bytes], clear_texts: List[bytearray],
                  substring: str, padding: int = 0) -> None:
    print("\n================= MANUAL ATTACK =================")
    print("{}Guess substring: \"{}\"{}".format(bcolors.OKGREEN, substring, bcolors.ENDC))
    print('-' * 20)
    for i in range(len(ciphertexts)):
        for j in range(len(ciphertexts)):
            one = ciphertexts[i][padding:]
            two = ciphertexts[j][padding:]
            xor_lines = one_xor_two(one, two)

            substring_bytes = bytes(substring, "utf-8")
            decrypted_text = one_xor_two(xor_lines, substring_bytes).decode("utf-8")
            clear_text = clear_texts[j].decode("utf-8")
            print(
                '{0:<9}: {1}'.format(
                    "{} xor {}".format(i + 1, j + 1),
                    clear_text[:padding] + colored_text(decrypted_text) + clear_text[len(substring):]
                )
            )
        print('-' * 20)


def main():
    ciphertexts = [binascii.unhexlify(line.rstrip()) for line in LINES]
    clear_texts = [bytearray(b'_' * len(line)) for line in ciphertexts]

    # key = "6e62bbc4085b3de37099adf88aad31267230ba0da9bd867577e3fed8eaf0f29f48296e29fb1d117e1a12b0aec0ec8f4b"
    key = None
    if key:
        decrypt(ciphertexts, clear_texts, key)
    else:
        clear_texts = attack(ciphertexts, clear_texts)
        if query_yes_no("\nDo you want to run the manual attack?"):
            manual_attack(ciphertexts, clear_texts, FREQUENT_WORDS[0])


if __name__ == '__main__':
    init()
    main()
