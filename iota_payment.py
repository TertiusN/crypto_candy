'''
Dependancies
pyota - pip install pyota[ccurl,pow]
RPi.GPIO - pip install RPi.GPIO
'''

import os
from configparser import ConfigParser
from cryptography.fernet import Fernet
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

cipher_suite = Fernet(os.environ['FERNET_KEY'])

if len(config_files) == 0:
    #Generate random IOTA seed
    seed = ''
    seed = seed.encode('ascii')
    api = Iota(node, seed)

    iota_seed_e = cipher_suite.encrypt(str(api.seed))
    print(iota_seed_e)

    cfgfile = open("config.ini",'w')
    parser.add_section('wallet')
    parser.set('wallet', 'iotaSeed', iota_seed_e)
    parser.set('wallet', 'index', '0')

    parser.write(cfgfile)
    cfgfile.close()

else:
    print("Config file successfully loaded")
    index = int(parser.get('wallet', 'index'))
    iota_seed_e = parser.get('wallet', 'iotaSeed')
    iota_seed = cipher_suite.decrypt(iota_seed_e)
    print(iota_seed)

