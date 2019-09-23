#==============================================================================
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
#==============================================================================
import pyAesCrypt
import os
import os.path
import sys
from progress.bar import IncrementalBar
from pyfiglet import Figlet
import getpass
import hashlib
from hashlib import sha3_512
import sqlite3

f = Figlet(font='slant')
print(f.renderText('Bot crypt'))

BLOCKSIZE = 65536

def crypt_bd(dir, password, password2):
    x = os.path.isfile(dir)
    if x == False:
        print('No such file or directory')
        main()
    buffer_size = 512 * 2048
    try:
        pyAesCrypt.encryptFile(str(dir), str(dir + '.bin'), password, buffer_size)
    except :
        print('Error')
        main()
    dir2 = dir + '.bin'
    try:
        pyAesCrypt.encryptFile(str(dir2), str(dir + '.aes'), password2, buffer_size)
    except :
        print('Error')
        main()
    os.remove(dir)
    os.remove(dir2)




def decrypt_bd(dir, password, password2):
    x = os.path.isfile(dir)
    if x is False:
        print('No such file or directory')
        main()
    buffer_size = 512 * 2048
    dir2 = dir[0:-4] + '.bin'
    try:
        pyAesCrypt.decryptFile(str(dir), str(dir2), password2, buffer_size)
    except:
        print('Error')
        main()
    try:
        pyAesCrypt.decryptFile(str(dir2), str(dir2[0:-4]), password, buffer_size)
    except:
        print('Error')
        main()
    os.remove(dir)
    os.remove(dir2)


x1 = os.path.isfile('.database.db')
x2 = os.path.isfile('.database.db.aes')
if x1 == False and x2 == True:
    password = getpass.getpass('pass 1: ')
    password2 = getpass.getpass('pass 2: ')
    decrypt_bd('.database.db.aes', password, password2)
    name_db = '.database.db'
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, name_db)
    conn = sqlite3.connect(path_db)
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()
else:
    name_db = '.database.db'
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, name_db)
    conn = sqlite3.connect(path_db)
    conn.row_factory = lambda cursor, row: row[0]
    cursor = conn.cursor()

def md5(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

def sha1OfFile(filepath):
    sha = hashlib.sha3_512()
    with open(filepath, 'rb') as f:
        while True:
            block = f.read(2**10)
            if not block: break
            sha.update(block)
        return sha.hexdigest()


def hash_s(string):
    signature = sha3_512(string.encode()).hexdigest()
    return signature




def decrypt(dir, password, password2):
    x = os.path.isfile(dir)
    if x is False:
        print('No such file or directory')
        main()
    print(proverka_aes(dir))
    buffer_size = 512 * 2048
    dir2 = dir[0:-4] + '.bin'
    try:
        pyAesCrypt.decryptFile(str(dir), str(dir2), password2, buffer_size)
    except:
        print('Error')
        main()
    dir3 = dir[0:-4]
    try:
        pyAesCrypt.decryptFile(str(dir2), str(dir3), password, buffer_size)
    except:
        print('Error')
        main()
    os.remove(dir)
    os.remove(dir2)



def decrypt_dir(dir, password, password2):
    x = os.path.isfile(dir)
    if x is False:
        print('No such file or directory')
        main()
    if proverka_aes(dir) == 'файл изменён ':
        print('file: ' + dir + ' изменён ')
        uc = input('извлечь? ')
        if uc == '-':
            main()
    buffer_size = 512 * 2048
    dir2 = dir[0:-4] + '.bin'
    try:
        pyAesCrypt.decryptFile(str(dir), str(dir2), password2, buffer_size)
    except:
        print('Error')
        main()
    dir3 = dir[0:-4]
    try:
        pyAesCrypt.decryptFile(str(dir2), str(dir3), password, buffer_size)
    except:
        print('Error')
        main()
    os.remove(dir)
    os.remove(dir2)


def add_aes_h(filename):
    try:
        x0 = hash_s(filename)
        x1 = md5(filename)
        x2 = sha1OfFile(filename)
        hash = [(x0,x1,x2)]
        cursor.executemany("INSERT INTO hash_aes VALUES (?,?,?)", hash)
        conn.commit()
    except:
        print('ошибка')


def proverka_aes(filename):
    cursor.execute('SELECT name FROM hash_aes')
    results = cursor.fetchall()
    x = list(results)
    if hash_s(filename) in x:
        p1 = md5(filename)
        p2 = sha1OfFile(filename)
        cursor.execute('SELECT md5 FROM hash_aes')
        results1 = cursor.fetchall()
        x1 = list(results1)
        if p1 in x1:
            cursor.execute('SELECT sha FROM hash_aes')
            results2 = cursor.fetchall()
            x2 = list(results2)  
            if p2 in x2:
                return 'файл не изменён '
            else:
                return 'файл изменён '
        else:
            return 'файл изменён '
    else:
        return 'файла нет в базе'




def crypt(dir, password, password2):
    x = os.path.isfile(dir)
    if x == False:
        print('No such file or directory')
        main()
    buffer_size = 512 * 2048
    dir2 = dir + '.bin'
    try:
        pyAesCrypt.encryptFile(str(dir), str(dir2), password, buffer_size)
    except :
        print('Error')
        main()
        os.remove(dir)
    dir3 = dir + '.aes'
    try:
        pyAesCrypt.encryptFile(str(dir2), str(dir3), password2, buffer_size)
    except  :
        print('Error')
        main()
    add_aes_h(dir3) 
    os.remove(dir)
    os.remove(dir2)


def walk_e(dir, password, password2):
    try:
        for name in os.listdir(dir):
            path = os.path.join(dir,name)
            if os.path.isfile(path):
                crypt(path, password, password2)
                bar.next()
            else: 
                walk_e(path, password, password2)
    except FileNotFoundError:
        print('not dir')
        main()


def walk_d(dir, password, password2):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):  
            try: 
                decrypt_dir(path, password, password2)
                bar.next()
            except: pass
        else: walk_d(path, password, password2)



def main():
    global bar
    print('------------------------------------------------------------------------')
    print('| 1-encrypt_file  2-decrypt_file  3-encrypt_dir  4-decrypt_dir  5-exit |')
    print('------------------------------------------------------------------------')
    user_comand = input('chooise action: ')
    if user_comand == '1':
        dir = input('file: ')
        password_1 = hash(getpass.getpass('введи пароль 1: '))
        password_2 = hash(getpass.getpass('повтори пвроль 1: '))
        if str(password_1) == str(password_2):
            password = str(password_2)
        else:
            print('different password')
            main()
        password_3 = getpass.getpass('введи пароль 2(strong): ')
        password_4 = getpass.getpass('повтори пвроль 2: ')
        if str(password_3) == str(password_4):
            password2 = password_4
        else:
            print('different password')
            main()
        crypt(dir, password, password2)
        main()
    elif user_comand == '2':
        dir = input('file: ')
        password = str(hash(getpass.getpass('введи пароль 1: ')))
        password2 = getpass.getpass('введи пароль 2: ')
        decrypt(dir, password, password2)
        main()
    elif user_comand == '3':
        dir = input('dir: ')
        password_1 = getpass.getpass('введи пароль 1: ')
        password_2 = getpass.getpass('повтори пвроль 1: ')
        if str(password_1) == str(password_2):
            password = password_2
        else:
            print('different password')
            main()
        password_3 = getpass.getpass('введи пароль 2: ')
        password_4 = getpass.getpass('повтори пвроль 2: ')
        if str(password_3) == str(password_4):
            password2 = password_4
        else:
            print('different password')
            main()
        cpt = sum([len(files) for r, d, files in os.walk(dir)])
        bar = IncrementalBar('Processing', max=cpt)
        walk_e(dir, password, password2)
        bar.finish()
        main()
    elif user_comand == '4':
        dir = input('dir: ')
        password = getpass.getpass('введи пароль 1: ')
        password2 = getpass.getpass('введи пароль 2: ')
        cpt = sum([len(files) for r, d, files in os.walk(dir)])
        bar = IncrementalBar('Processing', max=cpt)
        walk_d(dir, password, password2)
        bar.finish()
        main()
    elif user_comand == '5':
        pass1 = getpass.getpass('pass 1: ')
        pass2 = getpass.getpass('pass 2: ')
        crypt_bd(path_db,pass1,pass2)
        sys.exit()
    else:
        print('not valibale action')
        main()




try:
    # Создание таблицы
    cursor.execute("""CREATE TABLE hash_aes
                (name text, md5 text, sha text)
                    """)
    # Сохраняем изменения
    conn.commit()
except:
    main()

main()



