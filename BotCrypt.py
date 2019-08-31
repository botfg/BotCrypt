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
from hashlib import sha512



f = Figlet(font='slant')
print(f.renderText('Bot crypt'))




def hash(string):
    signature = sha512(string.encode()).hexdigest()
    return signature



def crypt(dir, password, password2):
    x = os.path.isfile(dir)
    if x == False:
        print('No such file or directory')
        main()
    lol = hash(dir)
    print(lol)
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



def walk_e(dir, password):
    for name in os.listdir(dir):
        path = os.path.join(dir,name)
        if os.path.isfile(path):
            crypt(path, password)
            bar.next()
        else: 
            walk_e(path, password)




def walk_d(dir, password):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):  
            try: 
                decrypt(path, password)
                bar.next()
            except: pass
        else: walk_d(path, password)



def decrypt(dir, password, password2):
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
    lol = hash(dir2[0:-4])
    print(lol)
    os.remove(dir)
    os.remove(dir2)


def main():
    global bar
    print('------------------------------------------------------------------------')
    print('| 1-encrypt_file  2-decrypt_file  3-encrypt_dir  4-decrypt_dir  5-exit |')
    print('------------------------------------------------------------------------')
    user_comand = input('chooise action: ')
    if user_comand == '1':
        dir = input('file: ')
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
        crypt(dir, password, password2)
        main()
    elif user_comand == '2':
        dir = input('file: ')
        password = getpass.getpass('введи пароль 1: ')
        password2 = getpass.getpass('введи пароль 2: ')
        decrypt(dir, password, password2)
        main()
    elif user_comand == '3':
        dir = input('dir: ')
        password1 = getpass.getpass('введи пароль: ')
        password2 = getpass.getpass('повтори пвроль: ')
        if str(password1) == str(password2):
            password = password2
        else:
            print('different password')
            main()
        cpt = sum([len(files) for r, d, files in os.walk(dir)])
        bar = IncrementalBar('Processing', max=cpt)
        walk_e(dir, password)
        bar.finish()
        main()
    elif user_comand == '4':
        dir = input('dir: ')
        password = hash(getpass.getpass('введи пароль: '))
        cpt = sum([len(files) for r, d, files in os.walk(dir)])
        bar = IncrementalBar('Processing', max=cpt)
        walk_d(dir, password)
        bar.finish()
        main()
    elif user_comand == '5':
        print('')
        sys.exit()
    else:
        print('not valibale action')
        main()

if(__name__ == '__main__'):
    main()