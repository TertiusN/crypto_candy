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



node = 'https://nodes.thetangle.org:443' #Select your preferred node

parser = ConfigParser()
config_files = parser.read('wallet.ini')
cipher_suite = Fernet(os.environ['FERNET_KEY'])

if len(config_files) == 0:
    #Generate random IOTA seed
    seed = ''
    seed = seed.encode('utf-8')
    api = Iota(node, seed)
    iota_seed = api.seed

    iota_seed_e = cipher_suite.encrypt(bytes(iota_seed))

    cfgfile = open("wallet.ini",'w')
    parser.add_section('wallet')
    parser.add_section('addresses')
    parser.set('wallet', 'iotaSeed', iota_seed_e.decode('utf-8'))
    parser.set('wallet', 'index', '1')
    parser.set('wallet', 'activeAddress', 'blank')
    parser.set('wallet', 'balance', '0')

    parser.write(cfgfile)
    print("Config file write success")
    cfgfile.close()

else:
    print("Config file successfully loaded")
    index = int(parser.get('wallet', 'index'))
    iota_seed_e = parser.get('wallet', 'iotaSeed')
    iota_seed = cipher_suite.decrypt(iota_seed_e.encode('utf-8')).decode('utf-8')
    print(iota_seed)

    api = Iota(node, iota_seed)
    inputs = api.get_inputs()

    cfgfile = open("wallet.ini", 'w')

    addresses = inputs['inputs']
    parser.set('wallet', 'index', str(len(addresses)))
    for i, address in enumerate(addresses):
        parser.set('addresses', 'address'+str(i), str(address))


    inputs = api.get_inputs(start=index, stop=index+1)
    balance = inputs['totalBalance']
    address = inputs['inputs'][-1]

    parser.set('wallet', 'balance', str(balance))
    parser.set('wallet', 'activeAddress', str(address))

    parser.write(cfgfile)
    cfgfile.close()
    print(inputs)
    print(address)
    print(balance)










