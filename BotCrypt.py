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


f = Figlet(font='slant')
print(f.renderText('Bot crypt'))






def crypt(dir, password):
    x = os.path.isfile(dir)
    if x == False:
        print('No such file or directory')
        main()
    buffer_size = 512 * 2048
    try:
        pyAesCrypt.encryptFile(str(dir), str(dir) + '.aes', password, buffer_size)
    except :
        print('Eror')
        main()
    os.remove(dir)


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



def decrypt(dir, password):
    x = os.path.isfile(dir)
    if x is False:
        print('No such file or directory')
        main()
    buffer_size = 512 * 2048
    try:
        pyAesCrypt.decryptFile(str(dir), str(dir[0:-4]), password, buffer_size)
    except:
        print('Eror')
        main()
    os.remove(dir)


def main():
    global bar
    print('------------------------------------------------------------------------')
    print('| 1-encrypt_file  2-decrypt_file  3-encrypt_dir  4-decrypt_dir  5-exit |')
    print('------------------------------------------------------------------------')
    user_comand = input('chooise action: ')
    if user_comand == '1':
        dir = input('file: ')
        password1 = input('password: ')
        password2 = input('repeat password: ')
        if str(password1) == str(password2):
            password = password2
        else:
            print('different password')
            main()
        crypt(dir, password)
        main()
    elif user_comand == '2':
        dir = input('file ')
        password = input('password: ')
        decrypt(dir, password)
        main()
    elif user_comand == '3':
        dir = input('dir: ')
        password1 = input('password: ')
        password2 = input('repeat password: ')
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
        password = input('password: ')
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