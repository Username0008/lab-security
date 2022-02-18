import csv
import hashlib
import random
import secrets
import string
from typing import Dict, Tuple

from lab_4_dict import d

PASSWORD_LENGTH = 10
SALT_LENGTH = 10
NUMBER_OF_PASSWORDS = 200000
PART_A = 0.1   # 10%
PART_B = 0.6   # 60%
PART_C = 0.05  # 5%
PART_D = 1 - (PART_A + PART_B + PART_C)


def get_random_word(dict_words: Dict, length: int) -> str:
    return random.choice(dict_words[length])


def transform_word(word: str) -> str:
    return word[::-1].upper()


def get_random_number(length: int) -> str:
    return ''.join(random.choice(string.digits) for i in range(length))


def get_md5(password: str) -> Tuple:
    return hashlib.md5(password.encode('utf-8')).hexdigest(),


def get_sha1_with_salt(password: str, salt: str) -> Tuple:
    return hashlib.sha1((password + salt).encode('utf-8')).hexdigest(), salt


def main():
    print('The password generator is started. Please wait...')
    
    rows_schema_one = []
    rows_schema_two = []

    # a. top 100
    for i in range(int(PART_A * NUMBER_OF_PASSWORDS)):
        password = '{}'.format(get_random_word(d, 100))
        salt = secrets.token_hex(SALT_LENGTH)
        rows_schema_one.append(get_md5(password))
        rows_schema_two.append(get_sha1_with_salt(password, salt))
    
    # b. most common passwords
    with open('lab_4_most_common.txt') as f:
        lines = f.readlines()
        for i in range(int(PART_B * NUMBER_OF_PASSWORDS)):
            password = str(secrets.choice(lines)).rstrip()
            salt = secrets.token_hex(SALT_LENGTH)
            rows_schema_one.append(get_md5(password))
            rows_schema_two.append(get_sha1_with_salt(password, salt))

    # c. complicated variant
    alphabet = string.ascii_letters + string.digits
    for i in range(int(PART_C * NUMBER_OF_PASSWORDS)):
        password = ''.join(secrets.choice(alphabet) for i in range(PASSWORD_LENGTH))
        salt = secrets.token_hex(SALT_LENGTH)
        rows_schema_one.append(get_md5(password))
        rows_schema_two.append(get_sha1_with_salt(password, salt))

    # d. general variant
    for i in range(int(PART_D * NUMBER_OF_PASSWORDS)):
        password = '{}{}{}'.format(
            get_random_word(d, 4).title(),
            transform_word(get_random_word(d, 5)),
            get_random_number(3)
        )
        salt = secrets.token_hex(SALT_LENGTH)
        rows_schema_one.append(get_md5(password))
        rows_schema_two.append(get_sha1_with_salt(password, salt))

    print("The task is completed.")

    # Write hashes to csv

    # schema # 1 (md5)
    headers = ['hash']
    with open('lab_4_hashes_1.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows_schema_one)
    
    # schema # 2 (sha1 + salt)
    headers = ['hash', 'salt']
    with open('lab_4_hashes_2.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows_schema_two)

    print('\nHashes are saved in csv files:\nlab_4_hashes_1.csv\nlab_4_hashes_2.csv')


if __name__ == '__main__':
    main()
