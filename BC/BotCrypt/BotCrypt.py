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
import getpass
import hashlib
import os
import os.path
import sys
from hashlib import sha3_512
import binascii
import random


import pyDes
import pyAesCrypt
from progress.bar import IncrementalBar


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
    length_string = (59 - len(string)) // 2     # 49
    decor = str((length_string * '-') + string + (length_string * '-') + '\n')
    return decor         


def clearScr() -> None:
    os.system('clear')


def hash(string) -> str:
    signature = sha3_512(string.encode()).hexdigest()
    return signature


def sha1OfFile(filepath) -> str:
    sha = hashlib.sha3_512()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10)
            if not block:
                break
            sha.update(block)
        return sha.hexdigest()


def crypt_2pass(file, password, password2) -> None:
    buffer_size1 = 512 * 2048
    file2 = file + '.bin'
    pyAesCrypt.encryptFile(file, file2, password, buffer_size1)
    buffer_size2 = 512 * 2048
    pyAesCrypt.encryptFile(file2, str(file + '.aes'), password2, buffer_size2)
    os.remove(file)
    os.remove(file2)

def crypt_1pass(file, password) -> None:
    buffer_size1 = 512 * 2048
    pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size1)
    os.remove(file)


def crypt_add_file(file, password, fileKey) -> None:
    buffer_size1 = 512 * 2048
    pyAesCrypt.encryptFile(file, str(file + '.bin'), password, buffer_size1)
    file2 = file + '.bin'
    buffer_size2 = 512 * 2048
    with open(fileKey, "rb") as in_file:
        in_file.seek(0)
        if len(in_file.read()) > 315:
            file_b = str(in_file.read(315)) + str(sha1OfFile(fileKey))
        elif len(in_file.read()) < 315:
            file_b = str(in_file.read()) + str(sha1OfFile(fileKey))
    pyAesCrypt.encryptFile(file2, str(file + '.aes'), file_b, buffer_size2)
    os.remove(file)
    os.remove(file2)


def walk_e_1pass(dir, password) -> None:
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            crypt_1pass(path, password)
            bar.next()
        else:
            walk_e_1pass(path, password)


def walk_d_1pass(dir, password) -> None:
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            try:
                decrypt_1pass(path, password)
                bar.next()
            except:
                pass
        else:
            walk_d_1pass(path, password)


def walk_e_2pass(dir, password, password2) -> None:
    for name in os.listdir(dir):
        path = os.path.join(dir,name)
        if os.path.isfile(path):
            crypt_2pass(path, password, password2)
            bar.next()
        else: 
            walk_e_2pass(path, password, password2)


def walk_d_2pass(dir, password, password2) -> None:
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):  
            try: 
                decrypt_2pass(path, password, password2)
                bar.next()
            except: pass
        else: walk_d_2pass(path, password, password2)


def decrypt_1pass(file, password) -> None:
    buffer_size1 = 512 * 2048
    file2 = file[0:-4] + '.bin'
    pyAesCrypt.decryptFile(file, str(file2[:-4]), password, buffer_size1)
    os.remove(file)


def decrypt_2pass(file, password, password2) -> None:
    buffer_size = 512 * 2048
    file2 = file[:-4] + '.bin'
    pyAesCrypt.decryptFile(file, file2, password2, buffer_size)
    pyAesCrypt.decryptFile(file2, str(file[:-4]), password, buffer_size)
    os.remove(file)
    os.remove(file2)


def decrypt_add_file(file, password, fileKey) -> None:
    buffer_size = 512 * 2048
    file2 = file[0:-4] + '.bin'
    with open(fileKey, "rb") as in_file:
        in_file.seek(0)
        if len(in_file.read()) > 315:
            file_b = str(in_file.read(315)) + str(sha1OfFile(fileKey))
        elif len(in_file.read()) < 315:
            file_b = str(in_file.read()) + str(sha1OfFile(fileKey))
    pyAesCrypt.decryptFile(file, file2, file_b, buffer_size)
    os.remove(file)
    pyAesCrypt.decryptFile(file2, str(file[0:-4]), password, buffer_size)
    os.remove(file2)


def main() -> None:
    global bar
    clearScr()
    print(botdrlogo)
    print(dec(color.RED + 'options' + color.END))
    print(color.RED + '1' + color.END + ')--' + color.OKBLUE + 'Encrypt_file' + color.END)
    print(color.RED + '2' + color.END + ')--' + color.OKBLUE + 'Decrypt_file' + color.END)
    print(color.RED + '3' + color.END + ')--' + color.OKBLUE + 'Encrypt_dir' + color.END)
    print(color.RED + '4' + color.END + ')--' + color.OKBLUE + 'Decrypt_dir' + color.END)
    print(color.RED + '5' + color.END + ')--' + color.OKBLUE + 'Encrypt_text' + color.END)
    print(color.RED + '6' + color.END + ')--' + color.OKBLUE + 'Decrypt_text' + color.END)
    print(color.RED + '7' + color.END + ')--' + color.OKBLUE + 'Password_generator' + color.END)
    print(color.RED + '8' + color.END + ')--' + color.OKBLUE + 'Exit\n' + color.END)
    user_comand = input(botdrPrompt)
    if user_comand == '1':
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
                        crypt_1pass(dir, password)
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
                        while True: # проверка 1 пароля
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
                        while True: # проверка второго пароля
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
                        crypt_2pass(dir, password, password2)
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
                crypt_add_file(dir, password, file)
                main()
            elif uc == 'Q':
                main()
            else:
                print('wrong command')
    elif user_comand == '2':
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
                                decrypt_1pass(dir, password)
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
                                decrypt_2pass(dir, password, password2)
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
                        decrypt_add_file(dir, password, file)
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
    elif user_comand == '3':
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
                walk_e_1pass(dir, password)
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
                walk_e_2pass(dir, password, password2)
                bar.finish()
                main()
            else:
                main()
    elif user_comand == '4':
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
                cpt = sum([len(files) for r, d, files in os.walk(dir)])
                bar = IncrementalBar('Processing', max=cpt)
                # проверка пароля
                while True:
                    password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                    try:
                        walk_d_1pass(dir, password)
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
                cpt = sum([len(files) for r, d, files in os.walk(dir)])
                bar = IncrementalBar('Processing', max=cpt)
                # проверка пароля
                while True:
                    password = getpass.getpass(color.OKBLUE + 'enter password 1: ' + color.END)
                    if password == 'Q':
                        main()
                    password2 = getpass.getpass(color.OKBLUE + 'enter password 2: ' + color.END)
                    if password2 == 'Q':
                        main()
                    try:
                        walk_d_2pass(dir, password, password2)
                        bar.finish()
                    except:
                        print(color.RED + 'invalid password' + color.END)
                    else:
                        break
                main()            
            else:
                main()
    elif user_comand == '5':
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
        print (color.OKBLUE + "Encrypted: " + color.END + str(d))
        while True:
            print(color.RED + '\nQ)--GO BACK\n' + color.END)
            uc = input(botdrPrompt)
            if uc == 'Q':
                main()
    elif user_comand == '6':
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
            print (color.OKBLUE + "Decrypted: " + color.END + out_text)
        while True:
            print(color.RED + '\nQ)--GO BACK\n' + color.END)
            uc = input(botdrPrompt)
            if uc == 'Q':
                main()   
    elif user_comand == '7':
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
        chars = ('+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
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
    elif user_comand == '8':
        clearScr()
        sys.exit()
    else:
        main()


def super_main() -> None:
    main()