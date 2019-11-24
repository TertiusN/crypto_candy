'''
Dependancies
pyota - pip install pyota[ccurl,pow]
RPi.GPIO - pip install RPi.GPIO
'''

import os, time
import configparser
from cryptography.fernet import Fernet
from iota import (
  __version__,
  Address,
  Iota,
)


class cryptoWallet:
    def __init__(self, key, node):
        self.key_f = Fernet(key)
        self.node = node

    def gen_seed(self):
        api = Iota(self.node, ''.encode('utf-8'))
        iota_seed_e = self.key_f.encrypt(bytes(api.seed)).decode('utf-8')

        return iota_seed_e

    def initialise_wallet(self):
        config = configparser.ConfigParser()
        config['wallet'] = {'iotaSeed': str(cryptoWallet.gen_seed(self)),
                            'index': '1',
                            'activeAddress': '9999',
                            'activeBalance': '0',
                            'totalBalance':'0'}
        config['addresses'] = {}
        filename = "Wallet_{}".format(int(time.time()))

        with open(filename, 'w') as configfile:
            config.write(configfile)
            configfile.close()

        return filename

    def load_wallet(self, wallet):
        config = configparser.ConfigParser()
        config.read(wallet)
        iota_seed_e = config['wallet']['iotaSeed']
        iota_seed = self.key_f.decrypt(iota_seed_e.encode('utf-8')).decode('utf-8')

        api = Iota(self.node, iota_seed)
        inputs = api.get_inputs()

        addresses = inputs['inputs']
        config['wallet']['index'] = str(len(addresses))

        if len(addresses) == 0:
            print("No address found. Generating...")
            gna_result = api.get_new_addresses(count=1)
            addresses = gna_result['addresses']

        config['wallet']['activeAddress'] = str(addresses[-1])
        config['wallet']['totalBalance'] = str(inputs['totalBalance'])

        for i, address in enumerate(addresses):
            config['addresses']['Address ' + str(i)] = str(address)

        with open(wallet, 'w') as configfile:
            config.write(configfile)

        return api, inputs

    def active_address_balance(self, api, index):
        inputs = api.get_inputs(start=index - 1, stop=index)
        balance = inputs['totalBalance']
        active_address = inputs['inputs'][0]

        return balance, active_address

    def update_balance(self, wallet, index):
        config = configparser.ConfigParser()
        config.read(wallet)
        iota_seed_e = config['wallet']['iotaSeed']
        iota_seed = self.key_f.decrypt(iota_seed_e.encode('utf-8')).decode('utf-8')

        api = Iota(self.node, iota_seed)
        inputs = api.get_inputs(start=index - 1, stop=index)
        balance = inputs['totalBalance']
        config['wallet']['activeBalance'] = str(balance)
        active_address = inputs['inputs'][0]

        with open(wallet, 'w') as configfile:
            config.write(configfile)

        return balance, active_address


