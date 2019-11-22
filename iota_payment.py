'''
Dependancies
pyota - pip install pyota[ccurl,pow]
RPi.GPIO - pip install RPi.GPIO
'''

import os
from configparser import ConfigParser
from iota import (
  __version__,
  Address,
  Iota,
  ProposedTransaction,
  Tag,
  TryteString,
  transaction
)

node = 'https://tuna.iotasalad.org:14265' #Select your preferred node

parser = ConfigParser()
config_files = parser.read('config.ini')

if len(config_files) == 0:
    #Generate random IOTA seed
    seed = ''
    seed = seed.encode('ascii')
    api = Iota(node, seed)
    iota_seed = str(api.seed)

    cfgfile = open("config.ini",'w')
    parser.add_section('wallet')
    parser.set('wallet', 'iotaSeed', iota_seed)
    parser.set('wallet', 'index', '0')

    parser.write(cfgfile)
    cfgfile.close()

else:
    print("Config file successfully loaded")
    index = int(parser.get('wallet', 'index'))
    iota_seed = parser.get('wallet', 'iotaSeed')

from cryptography.fernet import Fernet
key = Fernet.generate_key() #this is your "password
print(key)
print(os.environ['FERNET_KEY'])
cipher_suite = Fernet(key)
print(cipher_suite)
encoded_text = cipher_suite.encrypt(b"Hello stackoverflow!")
print(encoded_text)
decoded_text = cipher_suite.decrypt(encoded_text)
print(decoded_text)