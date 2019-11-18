# ==============================================================================
# Copyright 2019 Nikolai Bartenev. Contacts: botfgbartenevfgzero76@gmail.com
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

import pyAesCrypt
from pyfiglet import Figlet
from progress.bar import IncrementalBar

f = Figlet(font='slant')
print(f.renderText('Bot crypt'))


def hash(string):
    signature = sha3_512(string.encode()).hexdigest()
    return signature


def sha1OfFile(filepath):
    sha = hashlib.sha3_512()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10)
            if not block:
                break
            sha.update(block)
        return sha.hexdigest()


def crypt_2pass(file, password, password2):
    buffer_size1 = 512 * 2048
    file2 = file + '.bin'
    pyAesCrypt.encryptFile(file, file2, password, buffer_size1)
    buffer_size2 = 512 * 2048
    pyAesCrypt.encryptFile(file2, str(file + '.aes'), password2, buffer_size2)
    os.remove(file)
    os.remove(file2)

def crypt_1pass(file, password):
    buffer_size1 = 512 * 2048
    pyAesCrypt.encryptFile(file, str(file + '.aes'), password, buffer_size1)
    os.remove(file)


def crypt_add_file(file, password, fileKey):
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


def walk_e_1pass(dir, password):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            crypt_1pass(path, password)
            bar.next()
        else:
            walk_e_1pass(path, password)


def walk_d_1pass(dir, password):
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


def walk_e_2pass(dir, password, password2):
    for name in os.listdir(dir):
        path = os.path.join(dir,name)
        if os.path.isfile(path):
            crypt_2pass(path, password, password2)
            bar.next()
        else: 
            walk_e_2pass(path, password, password2)


def walk_d_2pass(dir, password, password2):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):  
            try: 
                decrypt_2pass(path, password, password2)
                bar.next()
            except: pass
        else: walk_d_2pass(path, password, password2)


def decrypt_1pass(file, password):
    buffer_size1 = 512 * 2048
    file2 = file[0:-4] + '.bin'
    pyAesCrypt.decryptFile(file, str(file2[:-4]), password, buffer_size1)
    os.remove(file)


def decrypt_2pass(file, password, password2):
    buffer_size = 512 * 2048
    file2 = file[:-4] + '.bin'
    pyAesCrypt.decryptFile(file, file2, password2, buffer_size)
    pyAesCrypt.decryptFile(file2, str(file[:-4]), password, buffer_size)
    os.remove(file)
    os.remove(file2)


def decrypt_add_file(file, password, fileKey):
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


def main():
    global bar
    print('------------------------------------------------------------------------')
    print('| 1-encrypt_file  2-decrypt_file  3-encrypt_dir  4-decrypt_dir  5-exit |')
    print('------------------------------------------------------------------------')
    user_comand = input('chooise action: ')
    if user_comand == '1':
        print('Encrypt file')
        while True:
            uc = input('use file as key? +y -n: ')
            if uc == 'q':
                break
            elif uc == '-':
                while True:
                    uc = input('1 pass or 2 pass: ')
                    if uc == '1':
                        # проверка введёного файла на сушествование
                        while True:
                            dir = input('encrypted file: ')
                            if dir == 'q':
                                main()
                            x1 = os.path.isfile(dir)
                            if not x1:
                                print('нет файла')
                            if x1:
                                break
                        while True:
                            password_1 = getpass.getpass('введи пароль 1: ')
                            if password_1 == 'q':
                                main()
                            password_2 = getpass.getpass('повтори пвроль 1: ')
                            if password_2 == 'q':
                                main()
                            if str(password_1) == str(password_2):
                                password = str(password_2)
                                break
                            else:
                                print('different password')
                        crypt_1pass(dir, password)
                        main()
                    elif uc == '2':
                        # проверка введёного файла на сушествование
                        while True:
                            dir = input('encrypted file: ')
                            if dir == 'q':
                                main()
                            x1 = os.path.isfile(dir)
                            if not x1:
                                print('нет файла')
                            if x1:
                                break
                        while True: # проверка 1 пароля
                            password_1 = getpass.getpass('введи пароль 1: ')
                            if password_1 == 'q':
                                main()
                            password_2 = getpass.getpass('повтори пвроль 1: ')
                            if password_2 == 'q':
                                main()
                            if str(password_1) == str(password_2):
                                password = str(password_2)
                                break
                            else:
                                print('different password')
                        while True: # проверка второго пароля
                            password_3 = getpass.getpass('введи пароль 2: ')
                            if password_3 == 'q':
                                main()
                            password_4 = getpass.getpass('повтори пвроль 2: ')
                            if password_4 == 'q':
                                main()
                            if str(password_3) == str(password_4):
                                password2 = str(password_3)
                                break
                            else:
                                print('different password')
                        crypt_2pass(dir, password, password2)
                        main()
                    else:
                        print('wrong command')
            elif uc == '+':
                dir = input('encrypted file: ')
                # проверка введёного файла на сушествование
                while True:
                    x1 = os.path.isfile(dir)
                    if not x1:
                        print('нет файла')
                        dir = input('encrypted file: ')
                    if x1:
                        break
                password_1 = getpass.getpass('введи пароль 1: ')
                password_2 = getpass.getpass('повтори пвроль 1: ')
                if str(password_1) == str(password_2):
                    password = str(password_2)
                else:
                    print('different password')
                    main()
                file = input('file key: ')
                # проверка введёного файла на сушествование
                while True:
                    x1 = os.path.isfile(file)
                    if not x1:
                        print('нет файла')
                        file = input('file key: ')
                    if x1:
                        break
                crypt_add_file(dir, password, file)
                main()
            elif uc == 'q':
                main()
            else:
                print('wrong command')
    elif user_comand == '2':
        print('Decrypt file')
        while True:
            uc = input("use file as key? +y -n: ")
            if uc == '-':
                while True:
                    uc = input('1 pass or 2 pass: ')
                    if uc == '1':
                        while True:
                            dir = input('encrypted file: ')
                            if dir == 'q':
                                main()
                            x1 = os.path.isfile(dir)
                            if not x1:
                                print('файл не найден')
                            if x1:
                                break
                        while True:
                            password = getpass.getpass('введи пароль 1: ')
                            if password == 'q':
                                main()
                            try:
                                decrypt_1pass(dir, password)
                            except:
                                print('невепный пароль')
                            else:
                                break
                        main()
                    elif uc == '2':
                        while True:
                            dir = input('encrypted file: ')
                            if dir == 'q':
                                main()
                            x1 = os.path.isfile(dir)
                            if not x1:
                                print('файл не найден')
                            if x1:
                                break 
                        while True:
                            password = getpass.getpass('введи пароль 1: ')
                            if password == 'q':
                                main()
                            password2 = getpass.getpass('введи пароль 2: ')
                            if password2 == 'q':
                                main()
                            try:
                                decrypt_2pass(dir, password, password2)
                            except:
                                print('невепный пароль')
                            else:
                                break   
                        main()  
                    elif uc == 'q':
                        main()
                    else:
                        print('wrong command')  
            elif uc == 'q':
                main()    
            elif uc == '+':
                # проверка введёного файла на сушествование
                while True:
                    dir = input('encrypted file: ')
                    if dir == 'q':
                        main()
                    x1 = os.path.isfile(dir)
                    if not x1:
                        print('нет файла')
                    if x1:
                        break
                password = getpass.getpass('введи пароль 1: ')
                if password == 'q':
                    main()
                # проверка введёного файла-ключа на сушествование
                while True:
                    file = input('file key: ')
                    if file == 'q':
                        main()
                    x1 = os.path.isfile(file)
                    if not x1:
                        print('нет файла')
                    if x1:
                        break
                while True:
                    try:
                        decrypt_add_file(dir, password, file)
                    except:
                        print('неправильный пароль или ключ файл')
                        password = getpass.getpass('введи пароль 1: ')
                        if password == 'q':
                            main()
                        # проверка введёного файла-ключа на сушествование
                        while True:
                            file = input('file key: ')
                            if file == 'q':
                                main()
                            x1 = os.path.isfile(file)
                            if not x1:
                                print('нет файла')
                            if x1:
                                break                    
                    else:
                        break
                main()
            else:
                print('wrong command')
    elif user_comand == '3':
        while True:
            uc = input('1 pass or 2 pass: ')
            if uc == 'q':
                main()
            elif uc == '1':
                # проверка введёного файла на сушествование
                while True:
                    dir = input('dir: ')
                    if dir == 'q':
                        main()
                    x1 = os.path.isdir(dir)
                    if not x1:
                        print('нет папки')
                    if x1:
                        break
                while True:
                    password_1 = getpass.getpass('введи пароль 1: ')
                    if password_1 == 'q':
                        main()
                    password_2 = getpass.getpass('повтори пвроль 1: ')
                    if password_2 == 'q':
                        main()
                    if str(password_1) == str(password_2):
                        password = password_2
                        break
                    else:
                        print('different password')
                cpt = sum([len(files) for r, d, files in os.walk(dir)])
                bar = IncrementalBar('Processing', max=cpt)
                walk_e_1pass(dir, password)
                bar.finish()
                main()
            elif uc == '2':
                # проверка введёного файла на сушествование
                while True:
                    dir = input('dir: ')
                    if dir == 'q':
                        main()
                    x1 = os.path.isdir(dir)
                    if not x1:
                        print('нет папки')
                    if x1:
                        break
                while True:
                    password_1 = getpass.getpass('введи пароль 1: ')
                    if password_1 == 'q':
                        main()
                    password_2 = getpass.getpass('повтори пвроль 1: ')
                    if password_2 == 'q':
                        main()
                    if str(password_1) == str(password_2):
                        password = password_2
                        break
                    else:
                        print('different password')
                while True:
                    password_3 = getpass.getpass('введи пароль 2: ')
                    if password_3 == 'q':
                        main()
                    password_4 = getpass.getpass('повтори пвроль 2: ')
                    if password_4 == 'q':
                        main()
                    if str(password_3) == str(password_4):
                        password2 = password_3
                        break
                    else:
                        print('different password')
                cpt = sum([len(files) for r, d, files in os.walk(dir)])
                bar = IncrementalBar('Processing', max=cpt)
                walk_e_2pass(dir, password, password2)
                bar.finish()
                main()
            else:
                print('нет команды')
    elif user_comand == '4':
        while True:
            uc = input('1 pass or 2 pass: ')
            if uc == 'q':
                main()
            elif uc == '1':
                # проверка введёного файла на сушествование
                while True:
                    dir = input('dir: ')
                    if dir == 'q':
                        main()
                    x1 = os.path.isdir(dir)
                    if not x1:
                        print('нет папки')
                    if x1:
                        break
                cpt = sum([len(files) for r, d, files in os.walk(dir)])
                bar = IncrementalBar('Processing', max=cpt)
                # проверка пароля
                while True:
                    password = getpass.getpass('введи пароль 1: ')
                    try:
                        walk_d_1pass(dir, password)
                        bar.finish()
                    except:
                        print('неверный пароль ')
                    else:
                        break
                main()
            elif uc == '2':
                # проверка введёного файла на сушествование
                while True:
                    dir = input('dir: ')
                    if dir == 'q':
                        main()
                    x1 = os.path.isdir(dir)
                    if not x1:
                        print('нет папки')
                    if x1:
                        break
                cpt = sum([len(files) for r, d, files in os.walk(dir)])
                bar = IncrementalBar('Processing', max=cpt)
                # проверка пароля
                while True:
                    password = getpass.getpass('введи пароль 1: ')
                    password2 = getpass.getpass('введи пароль 2: ')
                    try:
                        walk_d_2pass(dir, password, password2)
                        bar.finish()
                    except:
                        print('неверный пароль ')
                    else:
                        break
                main()            
            else:
                print('нет команды')
    elif user_comand == '5':
        sys.exit()
    else:
        print('not valibale action')
        main()


if(__name__ == '__main__'):
    main()