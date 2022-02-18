import csv
import hashlib
import sys
from datetime import datetime

from lab_4_dict import d


USE_TOP100_ONLY = True
FILE_WITH_MOST_COMMON_PASSWORDS = 'lab_4_most_common.txt'

FILE_WITH_HASHES = 'data/hashes_1.csv'
# FILE_WITH_HASHES = 'data/hashes_2.csv'
CSV_SPLITTER = ';'

# FILE_WITH_HASHES = 'data/lab_4_hashes_2.csv'
# CSV_SPLITTER = ','


def get_md5(password: str) -> str:
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def get_md5_with_salt(password: str, salt: str) -> str:
    return hashlib.md5((password.strip() + salt.strip()).encode('utf-8')).hexdigest()


def get_sha1_with_salt(password: str, salt: str) -> str:
    return hashlib.sha1((password.strip() + salt.strip()).encode('utf-8')).hexdigest()


def get_sha256_with_salt(password: str, salt: str) -> str:
    return hashlib.sha256((password.strip() + salt.strip()).encode('utf-8')).hexdigest()


def get_sha512_with_salt(password: str, salt: str) -> str:
    return hashlib.sha512((password.strip() + salt.strip()).encode('utf-8')).hexdigest()


def main():
    print('[{}] The task is started.'.format(datetime.now().time().strftime("%H:%M:%S")))
    
    with open(FILE_WITH_HASHES) as fh:
        hashes_lines = fh.readlines()
        hashes_count = len(hashes_lines)
        
        if USE_TOP100_ONLY:
            print("Use TOP-100 passwords. Please wait...")
            common_passwords = d[100]
        else:
            print("Use 10K most common passwords. Please wait...")
            with open(FILE_WITH_MOST_COMMON_PASSWORDS) as f:
                common_passwords = f.readlines()

        try:
            k = 0
            recover_passwords = []
            for i in range(hashes_count):
                orig_hash, salt = hashes_lines[i].split(CSV_SPLITTER)
                sys.stdout.write("\rProcessed %d%% (%d of %d rows)" % ((100 * (i + 1) / hashes_count), i + 1, hashes_count))
                sys.stdout.flush()
                for password in common_passwords:
                    result_hashes = []

                    password_hash = get_md5_with_salt(password, salt)
                    result_hashes.append(password_hash)

                    password_hash = get_sha1_with_salt(password, salt)
                    result_hashes.append(password_hash)

                    # password_hash = get_sha256_with_salt(password, salt)
                    # result_hashes.append(password_hash)

                    # password_hash = get_sha512_with_salt(password, salt)
                    # result_hashes.append(password_hash)

                    if orig_hash in result_hashes:
                        # print('row # {0:<6}: \"{1}\"'.format(i, password.strip()))
                        recover_passwords.append((i, password.strip()))
                        k += 1
                        break
        except KeyboardInterrupt:
            print("\n[{}] The task is interrupted.".format(datetime.now().time().strftime("%H:%M:%S")))
        else:
            print("\n[{}] The task is finished.".format(datetime.now().time().strftime("%H:%M:%S")))
        finally:
            print("Managed to recover {} of {} passwords.".format(k, i))
            # write results to csv
            headers = ['row_no', 'password']
            with open('lab_4_recover_passwords.csv', 'w') as fr:
                f_csv = csv.writer(fr)
                f_csv.writerow(headers)
                f_csv.writerows(recover_passwords)
            print('\nResults are saved in csv file:\nlab_4_recover_passwords.csv')


if __name__ == '__main__':
    main()
