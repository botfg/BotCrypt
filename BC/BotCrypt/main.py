# ==============================================================================
# Copyright 2020 Nikolai Bartenev. Contacts: botfgbartenevfgzero76@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import binascii
import getpass
import hashlib
import os
import os.path
import random
import sys
from hashlib import sha3_512

import pyAesCrypt
import pyDes
from progress.bar import IncrementalBar
from stegano import lsb


class color:
    OKBLUE = ('\033[94m')
    OKGREEN = ('\033[92m')
    WARNING = ('\033[93m')
    RED = ('\033[91m')
    END = ('\033[0m')


botdrPrompt = (color.OKGREEN + "BotCrypt ~# " + color.END)


botdrlogo = (color.OKGREEN + '''
    ____        __                           __ 
   / __ )____  / /_   ____________  ______  / /_
  / __  / __ \/ __/  / ___/ ___/ / / / __ \/ __/
 / /_/ / /_/ / /_   / /__/ /  / /_/ / /_/ / /_  
/_____/\____/\__/   \___/_/   \__, / .___/\__/  
                             /____/_/
''' + color.END)


def dec(string: str) -> str:
    length_string = (59 - len(string)) // 2  # 49
    decor = str((length_string * '-') + string + (length_string * '-') + '\n')
    return decor


def clearScr() -> None:
    os.system('clear')


def hash(string: str) -> str:
    signature = sha3_512(string.encode()).hexdigest()
    return signature


def sha1OfFile(filepath: str) -> str:
    sha = hashlib.sha3_512()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2 ** 10)
            if not block:
                break
            sha.update(block)
        return sha.hexdigest()


# args: 1)file path 2)password 3)password2 or file key path
# mods: 1pas; 2pas; fkey
def crypt_aes(*args: str, mod: str) -> None:
    buffer_size = 512 * 2048
    file2 = args[0][:-4] + '.bin'
    file = args[0]
    password = args[1]
    if mod == '1pas':
        pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size)
        os.remove(file)
    elif mod == '2pas':
        password2 = args[2]
        pyAesCrypt.encryptFile(file, file2, password, buffer_size)
        buffer_size2 = 512 * 2048
        pyAesCrypt.encryptFile(file2, str(file + '.aes'), password2, buffer_size)
        os.remove(file)
        os.remove(file2)
    elif mod == 'fkey':
        fileKey = args[2]
        pyAesCrypt.encryptFile(file, str(file + '.bin'), password, buffer_size)
        with open(fileKey, "rb") as in_file:
            in_file.seek(0)
            if len(in_file.read()) > 315:
                file_b = str(in_file.read(315)) + str(sha1OfFile(fileKey))
            elif len(in_file.read()) < 315:
                file_b = str(in_file.read()) + str(sha1OfFile(fileKey))
        in_file.close()
        pyAesCrypt.encryptFile(file2, str(file + '.aes'), file_b, buffer_size)
        os.remove(file)
        os.remove(file2)


# args: 1)dir path: str 2)password: str  optional: 3)password2: str
def walk_e_pass(*args: str) -> None:
    dir = args[0]
    password = args[1]
    if len(args) == 2:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                crypt_aes(path, password, mod='1pas')
                bar.next()
            else:
                walk_e_pass(path, password)
    elif len(args) == 3:
        password2 = args[2]
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                crypt_aes(path, password, password2, mod='2pas')
                bar.next()
            else:
                walk_e_pass(path, password, password2)


# args: 1)dir path: str 2)password: str  optional: 3)password2: str
def walk_d_pass(*args: str) -> None:
    dir = args[0]
    password = args[1]
    if len(args) == 2:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                try:
                    decrypt_aes(path, password, mod='1pas')
                    bar.next()
                except:
                    pass
            else:
                walk_d_pass(path, password)
    elif len(args) == 3:
        password2 = args[2]
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                try:
                    decrypt_aes(path, password, password2, mod='2pas')
                    bar.next()
                except:
                    pass
            else:
                walk_d_pass(path, password, password2)


# args: 1)file path 2)password 3)password2 or file key path
# mods: 1pas; 2pas; fkey
def decrypt_aes(*args: str, mod: str) -> None:
    buffer_size = 512 * 2048
    file2 = args[0][:-4] + '.bin'
    file = args[0]
    password = args[1]
    if mod == '1pas':
        pyAesCrypt.decryptFile(file, str(file2[:-4]), password, buffer_size)
        os.remove(file)
    elif mod == '2pas':
        password2 = args[2]
        pyAesCrypt.decryptFile(file, file2, password2, buffer_size)
        pyAesCrypt.decryptFile(file2, str(file[:-4]), password, buffer_size)
        os.remove(file)
        os.remove(file2)
    elif mod == 'fkey':
        fileKey = args[2]
        with open(fileKey, "rb") as in_file:
            in_file.seek(0)
            if len(in_file.read()) > 315:
                file_b = str(in_file.read(315)) + str(sha1OfFile(fileKey))
            elif len(in_file.read()) < 315:
                file_b = str(in_file.read()) + str(sha1OfFile(fileKey))
        in_file.close()
        pyAesCrypt.decryptFile(file, file2, file_b, buffer_size)
        os.remove(file)
        pyAesCrypt.decryptFile(file2, str(file[0:-4]), password, buffer_size)
        os.remove(file2)


def commands_Encrypt_file() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Encrypt file' + color.END))
    while True:
        print(color.OKBLUE + 'Use file as key? [Y/n]\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Q':
            main()
        elif uc == 'n':
            while True:
                clearScr()
                print(botdrlogo)
                print(dec(color.RED + 'Encrypt file' + color.END))
                print(color.OKBLUE + '1 pass or 2 pass\n' + color.END)
                uc = input(botdrPrompt)
                if uc == 'Q':
                    main()
                elif uc == '1':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'single password file encryption' + color.END))
                    # проверка введёного файла на сушествование
                    while True:
                        dir = input(color.OKBLUE + 'encrypted file: ' + color.END)
                        if dir == 'Q':
                            main()
                        x1 = os.path.isfile(dir)
                        if not x1:
                            print(color.RED + 'file not found' + color.END)
                        if x1:
                            break
                    while True:
                        password_1 = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                        if password_1 == 'Q':
                            main()
                        password_2 = getpass.getpass(color.OKBLUE + 'repeat password 1: ' + color.END)
                        if password_2 == 'Q':
                            main()
                        if str(password_1) == str(password_2):
                            password = str(password_2)
                            break
                        else:
                            print(color.RED + 'different password' + color.END)
                    crypt_aes(dir, password, mod='1pas')
                    main()
                elif uc == '2':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'file encryption with two passwords' + color.END))
                    # проверка введёного файла на сушествование
                    while True:
                        dir = input(color.OKBLUE + 'encrypted file: ' + color.END)
                        if dir == 'Q':
                            main()
                        x1 = os.path.isfile(dir)
                        if not x1:
                            print(color.RED + 'file not found' + color.END)
                        if x1:
                            break
                    while True:  # проверка 1 пароля
                        password_1 = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                        if password_1 == 'Q':
                            main()
                        password_2 = getpass.getpass(color.OKBLUE + 'repeat password 1: ' + color.END)
                        if password_2 == 'Q':
                            main()
                        if str(password_1) == str(password_2):
                            password = str(password_2)
                            break
                        else:
                            print(color.RED + 'different password' + color.END)
                    while True:  # проверка второго пароля
                        password_3 = getpass.getpass(color.OKBLUE + 'enter password 2: ' + color.END)
                        if password_3 == 'Q':
                            main()
                        password_4 = getpass.getpass(color.OKBLUE + 'repeat password 2: ' + color.END)
                        if password_4 == 'Q':
                            main()
                        if str(password_3) == str(password_4):
                            password2 = str(password_3)
                            break
                        else:
                            print(color.RED + 'different password' + color.END)
                    crypt_aes(dir, password, password2, mod='2pas')
                    main()
                else:
                    print('wrong command')
        elif uc == 'Y':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'file encryption with key_file' + color.END))
            # проверка введёного файла на сушествование
            while True:
                dir = input(color.OKBLUE + 'encrypted file: ' + color.END)
                if dir == 'Q':
                    main()
                x1 = os.path.isfile(dir)
                if not x1:
                    print(color.RED + 'file not found' + color.END)
                elif x1:
                    break
            password_1 = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
            password_2 = getpass.getpass(color.OKBLUE + 'repeat password 1: ' + color.END)
            if str(password_1) == str(password_2):
                password = str(password_2)
            else:
                print(color.RED + 'different password' + color.END)
                main()
            # проверка введёного файла на сушествование
            while True:
                file = input(color.OKBLUE + 'file key: ' + color.END)
                if file == 'Q':
                    main()
                x1 = os.path.isfile(file)
                if not x1:
                    print(color.RED + 'file not found' + color.END)
                if x1:
                    break
            crypt_aes(dir, password, file, mod='fkey')
            main()
        else:
            main()


def commands_Decrypt_file() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Decrypt file' + color.END))
    while True:
        print(color.OKBLUE + "use file as key? [Y/n]\n" + color.END)
        uc = input(botdrPrompt)
        if uc == 'n':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Decrypt file' + color.END))
            while True:
                print(color.OKBLUE + '1 pass or 2 pass\n' + color.END)
                uc = input(botdrPrompt)
                if uc == '1':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'decryption file with one password' + color.END))
                    while True:
                        dir = input(color.OKBLUE + 'encrypted file: ' + color.END)
                        if dir == 'Q':
                            main()
                        x1 = os.path.isfile(dir)
                        if not x1:
                            print(color.RED + 'file not found' + color.END)
                        if x1:
                            break
                    while True:
                        password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                        if password == 'Q':
                            main()
                        try:
                            decrypt_aes(dir, password, mod='1pas')
                        except:
                            print(color.RED + 'Invalid password' + color.END)
                        else:
                            break
                    main()
                elif uc == '2':
                    clearScr()
                    print(botdrlogo)
                    print(dec(color.RED + 'decryption file with two passwords' + color.END))
                    while True:
                        dir = input(color.OKBLUE + 'encrypted file: ' + color.END)
                        if dir == 'Q':
                            main()
                        x1 = os.path.isfile(dir)
                        if not x1:
                            print(color.RED + 'file not found' + color.END)
                        if x1:
                            break
                    while True:
                        password = getpass.getpass(color.OKBLUE + 'entr password 1: ' + color.END)
                        if password == 'Q':
                            main()
                        password2 = getpass.getpass(color.OKBLUE + 'enter password 2: ' + color.END)
                        if password2 == 'Q':
                            main()
                        try:
                            decrypt_aes(dir, password, password2, mod='2pas')
                        except:
                            print(color.RED + 'Invalid password' + color.END)
                        else:
                            break
                    main()
                elif uc == 'Q':
                    main()
                else:
                    main()
        elif uc == 'Q':
            main()
        elif uc == 'Y':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'decryption file with file_key' + color.END))
            # проверка введёного файла на сушествование
            while True:
                dir = input(color.OKBLUE + 'encrypted file: ' + color.END)
                if dir == 'Q':
                    main()
                x1 = os.path.isfile(dir)
                if not x1:
                    print(color.RED + 'file not found' + color.END)
                if x1:
                    break
            password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
            if password == 'Q':
                main()
            # проверка введёного файла-ключа на сушествование
            while True:
                file = input(color.OKBLUE + 'file key: ' + color.END)
                if file == 'Q':
                    main()
                x1 = os.path.isfile(file)
                if not x1:
                    print(color.RED + 'file not found' + color.END)
                if x1:
                    break
            while True:
                try:
                    decrypt_aes(dir, password, file, mod='fkey')
                except:
                    print(color.RED + 'wrong password or file_key' + color.END)
                    password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                    if password == 'Q':
                        main()
                    # проверка введёного файла-ключа на сушествование
                    while True:
                        file = input(color.OKBLUE + 'file key: ' + color.END)
                        if file == 'Q':
                            main()
                        x1 = os.path.isfile(file)
                        if not x1:
                            print(color.RED + 'file not found' + color.END)
                        if x1:
                            break
                else:
                    break
            main()
        else:
            main()


def commands_Encrypt_dir() -> None:
    global bar
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Encrypt_dir' + color.END))
    while True:
        print(color.OKBLUE + '1 pass or 2 pass\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Q':
            main()
        elif uc == '1':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'one-password directory encryption' + color.END))
            # проверка введёного файла на сушествование
            while True:
                dir = input(color.OKBLUE + 'dir: ' + color.END)
                if dir == 'Q':
                    main()
                x1 = os.path.isdir(dir)
                if not x1:
                    print(color.RED + 'dir not found' + color.END)
                if x1:
                    break
            while True:
                password_1 = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                if password_1 == 'Q':
                    main()
                password_2 = getpass.getpass(color.OKBLUE + 'repeat password 1: ' + color.END)
                if password_2 == 'Q':
                    main()
                if str(password_1) == str(password_2):
                    password = password_2
                    break
                else:
                    print(color.RED + 'different password' + color.END)
            cpt = sum([len(files) for r, d, files in os.walk(dir)])
            bar = IncrementalBar('Processing', max=cpt)
            walk_e_pass(dir, password)
            bar.finish()
            main()
        elif uc == '2':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'encryption directory with two passwords' + color.END))
            # проверка введёного файла на сушествование
            while True:
                dir = input(color.OKBLUE + 'dir: ' + color.END)
                if dir == 'Q':
                    main()
                x1 = os.path.isdir(dir)
                if not x1:
                    print(color.RED + 'dir not found' + color.END)
                if x1:
                    break
            while True:
                password_1 = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                if password_1 == 'Q':
                    main()
                password_2 = getpass.getpass(color.OKBLUE + 'repeat password 1: ' + color.END)
                if password_2 == 'Q':
                    main()
                if str(password_1) == str(password_2):
                    password = password_2
                    break
                else:
                    print(color.RED + 'different password' + color.END)
            while True:
                password_3 = getpass.getpass(color.OKBLUE + 'enter password 2: ' + color.END)
                if password_3 == 'Q':
                    main()
                password_4 = getpass.getpass(color.OKBLUE + 'repeate password 2: ' + color.END)
                if password_4 == 'Q':
                    main()
                if str(password_3) == str(password_4):
                    password2 = password_3
                    break
                else:
                    print(color.RED + 'different password' + color.END)
            cpt = sum([len(files) for r, d, files in os.walk(dir)])
            bar = IncrementalBar('Processing', max=cpt)
            walk_e_pass(dir, password, password2)
            bar.finish()
            main()
        else:
            main()


def commands_Decrypt_dir() -> None:
    global bar
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Decrypt_dir' + color.END))
    while True:
        print(color.OKBLUE + '1 pass or 2 pass\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Q':
            main()
        elif uc == '1':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'decryption directory with one password' + color.END))
            # проверка введёного файла на сушествование
            while True:
                dir = input(color.OKBLUE + 'dir: ' + color.END)
                if dir == 'Q':
                    main()
                x1 = os.path.isdir(dir)
                if not x1:
                    print(color.RED + 'dir not found' + color.END)
                if x1:
                    break
            # проверка пароля
            while True:
                password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                try:
                    cpt = sum([len(files) for r, d, files in os.walk(dir)])
                    bar = IncrementalBar('Processing', max=cpt)
                    walk_d_pass(dir, password)
                    bar.finish()
                except:
                    print(color.RED + 'invalid password' + color.END)
                else:
                    break
            main()
        elif uc == '2':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'decryption directory with two passwords' + color.END))
            # проверка введёного файла на сушествование
            while True:
                dir = input(color.OKBLUE + 'dir: ' + color.END)
                if dir == 'Q':
                    main()
                x1 = os.path.isdir(dir)
                if not x1:
                    print(color.RED + 'dir not found' + color.END)
                if x1:
                    break
            # проверка пароля
            while True:
                password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                if password == 'Q':
                    main()
                password2 = getpass.getpass(color.OKBLUE + 'enter password 2: ' + color.END)
                if password2 == 'Q':
                    main()
                try:
                    cpt = sum([len(files) for r, d, files in os.walk(dir)])
                    bar = IncrementalBar('Processing', max=cpt)
                    walk_d_pass(dir, password, password2)
                    bar.finish()
                except:
                    print(color.RED + 'invalid password' + color.END)
                else:
                    break
            main()
        else:
            main()


def commands_Encrypt_text() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Encrypt_text' + color.END))
    data = input(color.OKBLUE + 'text: ' + color.END)
    if data == 'Q':
        main()
    data = data.encode()
    while True:
        key = input(color.OKBLUE + 'enter 24 character password: ' + color.END)
        if key == 'Q':
            main()
        key = key.encode()
        if len(key) != 24:
            print(color.RED + 'not 24 characters' + color.END)
        elif len(key) == 24:
            break
    k = pyDes.triple_des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data).hex()
    print(color.OKBLUE + "Encrypted: " + color.END + str(d))
    while True:
        print(color.RED + '\nQ)--GO BACK\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Q':
            main()


def commands_Decrypt_text() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Decrypt_text' + color.END))
    while True:
        try:
            text = input(color.OKBLUE + 'text: ' + color.END)
            if text == 'Q':
                main()
            data = binascii.unhexlify(text)
        except:
            print(color.RED + 'invalid input' + color.END)
            continue
        else:
            break
    while True:
        key = input(color.OKBLUE + 'enter 24 character password: ' + color.END)
        if key == 'Q':
            main()
        key = key.encode()
        if len(key) != 24:
            print(color.RED + 'not 24 characters' + color.END)
        elif len(key) == 24:
            break
    k = pyDes.triple_des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    out_text = str(k.decrypt(data).decode('utf-8'))
    if len(out_text) == 0:
        print(color.RED + 'invalid password' + color.END)
    else:
        print(color.OKBLUE + "Decrypted: " + color.END + out_text)
    while True:
        print(color.RED + '\nQ)--GO BACK\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Q':
            main()


def commands_Password_generator() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'Password generator' + color.END))
    while True:
        len_pass = input(color.OKBLUE + 'len password: ' + color.END)
        if len_pass == 'Q':
            main()
        x1 = (len_pass).isnumeric()
        if x1:
            if int(len_pass) >= 1:
                break
        if not x1:
            print(color.RED + 'invalid input' + color.END)
    while True:
        num_pass = input(color.OKBLUE + 'Number of passwords: ' + color.END)
        if num_pass == 'Q':
            main()
        x1 = (num_pass).isnumeric()
        if x1:
            if int(num_pass) >= 1:
                break
        if not x1:
            print(color.RED + 'invalid input' + color.END)
    chars = ('+-/*!&$#()_?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    print('')
    for n in range(int(num_pass)):
        password = ('')
        for i in range(int(len_pass)):
            password += random.choice(chars)
        print(password + '\n')
    while True:
        print(color.RED + 'Q)--GO BACK\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Q':
            main()


def commands_Encrypt_img() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'PNG hide' + color.END))
    while True:
        print(color.OKBLUE + 'Encrypt text? [Y/n]\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Y':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Hide encrypted text in PNG' + color.END))
            data = input(color.OKBLUE + 'text: ' + color.END)
            if data == 'Q':
                main()
            data = data.encode()
            while True:
                key = input(color.OKBLUE + 'enter 24 character password: ' + color.END)
                if key == 'Q':
                    main()
                key = key.encode()
                if len(key) != 24:
                    print(color.RED + 'not 24 characters' + color.END)
                elif len(key) == 24:
                    break
            k = pyDes.triple_des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
            d = k.encrypt(data).hex()
            while True:
                img = input(color.OKBLUE + 'picture for text injection: ' + color.END)
                if img == 'Q':
                    main()
                x1 = os.path.isfile(img)
                if x1:
                    filename, file_extension = os.path.splitext(img)
                    if file_extension == 'png' or 'PNG':
                        break
                    else:
                        print(color.RED + 'not png file' + color.END)
                        continue
                if not x1:
                    print(color.RED + 'file not found' + color.END)
            secret = lsb.hide(img, d)
            img_save = input(color.OKBLUE + 'path to a new picture with a new name: ' + color.END)
            secret.save(img_save)
            main()
        elif uc == 'n':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'PNG hide' + color.END))
            data = input(color.OKBLUE + 'text: ' + color.END)
            if data == 'Q':
                main()
            while True:
                img = input(color.OKBLUE + 'picture for text injection: ' + color.END)
                if img == 'Q':
                    main()
                x1 = os.path.isfile(img)
                if x1:
                    filename, file_extension = os.path.splitext(img)
                    if file_extension == 'png' or 'PNG':
                        break
                    else:
                        print(color.RED + 'not png file' + color.END)
                        continue
                if not x1:
                    print(color.RED + 'file not found' + color.END)
            secret = lsb.hide(img, data)
            img_save = input(color.OKBLUE + 'path to a new picture with a new name: ' + color.END)
            secret.save(img_save)
            main()
        elif uc == 'Q':
            main()


def commands_Decrypt_img() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'PNG unhide' + color.END))
    while True:
        print(color.OKBLUE + 'Encrypt text? [Y/n]\n' + color.END)
        uc = input(botdrPrompt)
        if uc == 'Y':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Unhide encrypted text in PNG' + color.END))
            while True:
                img = input(color.OKBLUE + 'picture: ' + color.END)
                if img == 'Q':
                    main()
                x1 = os.path.isfile(img)
                if x1:
                    filename, file_extension = os.path.splitext(img)
                    if file_extension == 'png' or 'PNG':
                        break
                    else:
                        print(color.RED + 'not png file' + color.END)
                        continue
                if not x1:
                    print(color.RED + 'file not found' + color.END)
            des_message = lsb.reveal(img)
            data = binascii.unhexlify(des_message)
            while True:
                key = input(color.OKBLUE + 'enter 24 character password: ' + color.END)
                if key == 'Q':
                    main()
                key = key.encode()
                if len(key) != 24:
                    print(color.RED + 'not 24 characters' + color.END)
                elif len(key) == 24:
                    break
            k = pyDes.triple_des(key, pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
            out_text = str(k.decrypt(data).decode('utf-8'))
            if len(out_text) == 0:
                print(color.RED + 'invalid password' + color.END)
            else:
                print(color.OKBLUE + "Decrypted text: " + color.END + out_text)
            while True:
                print(color.RED + '\nQ)--GO BACK\n' + color.END)
                uc = input(botdrPrompt)
                if uc == 'Q':
                    main()
        elif uc == 'n':
            clearScr()
            print(botdrlogo)
            print(dec(color.RED + 'Unhide text in PNG' + color.END))
            while True:
                img = input(color.OKBLUE + 'picture: ' + color.END)
                if img == 'Q':
                    main()
                x1 = os.path.isfile(img)
                if x1:
                    filename, file_extension = os.path.splitext(img)
                    if file_extension == 'png' or 'PNG':
                        break
                    else:
                        print(color.RED + 'not png file' + color.END)
                        continue
                if not x1:
                    print(color.RED + 'file not found' + color.END)
            clear_message = lsb.reveal(img)
            print(color.OKBLUE + 'text: ' + color.END + clear_message)
            while True:
                print(color.RED + '\nQ)--GO BACK\n' + color.END)
                uc = input(botdrPrompt)
                if uc == 'Q':
                    main()
        elif uc == 'Q':
            main()


def main() -> None:
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'options' + color.END))
    print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'File' + color.END)
    print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Dir' + color.END)
    print(color.RED + '3' + color.END + ')--' + color.OKBLUE + 'Text' + color.END)
    print(color.RED + '4' + color.END + ')--' + color.OKBLUE + 'PNG' + color.END)
    print(color.RED + '5' + color.END + ')--' + color.OKBLUE + 'Password_generator' + color.END)
    print(color.RED + '6' + color.END + ')--' + color.OKBLUE + 'Exit\n' + color.END)
    user_command = input(botdrPrompt)
    if user_command == '1':
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'File' + color.END))
        print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Encrypt' + color.END)
        print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Decrypt\n' + color.END)
        while True:
            uc = input(botdrPrompt)
            if uc == '1':
                commands_Encrypt_file()
                break
            elif uc == '2':
                commands_Decrypt_file()
                break
            elif uc == 'Q':
                main()
                break
        main()
    elif user_command == '2':
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Dir' + color.END))
        print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Encrypt' + color.END)
        print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Decrypt\n' + color.END)
        while True:
            uc = input(botdrPrompt)
            if uc == '1':
                commands_Encrypt_dir()
                break
            elif uc == '2':
                commands_Decrypt_dir()
                break
            elif uc == 'Q':
                main()
                break
        main()
    elif user_command == '3':
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Text' + color.END))
        print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Encrypt' + color.END)
        print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Decrypt\n' + color.END)
        while True:
            uc = input(botdrPrompt)
            if uc == '1':
                commands_Encrypt_text()
                break
            elif uc == '2':
                commands_Decrypt_text()
                break
            elif uc == 'Q':
                main()
                break
        main()
    elif user_command == '4':
        clearScr()
        print(botdrlogo)
        print(dec(color.RED + 'Img' + color.END))
        print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Encrypt' + color.END)
        print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Decrypt\n' + color.END)
        while True:
            uc = input(botdrPrompt)
            if uc == '1':
                commands_Encrypt_img()
                break
            elif uc == '2':
                commands_Decrypt_img()
                break
            elif uc == 'Q':
                main()
                break
        main()
    elif user_command == '5':
        commands_Password_generator()
        main()
    elif user_command == '6':
        clearScr()
        sys.exit()
    else:
        main()