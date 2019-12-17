from setuptools import setup, find_packages
from os.path import join, dirname
import os
import BotCrypt
from BotCrypt.BotCrypt import super_main


setup(
    name='BotCrypt',
    author='botfg76',
    author_email='botfgbartenevfgzero76@gmail.com',
    license='Apache License Version 2.0',
    url='https://github.com/botfg/BotCrypt',
    description='crypt and decrypt file',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    version=BotCrypt.__version__,
    packages=find_packages(),
    install_requires=[
        'progress==1.5',
        'pyAesCrypt==0.4.3'],
    entry_points={
        'console_scripts':
            ['bc = BotCrypt.BotCrypt:super_main']
        },
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.6',
    
    
)