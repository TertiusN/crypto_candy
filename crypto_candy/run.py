from crypto_candy.crypto_payments import iota_payment
from crypto_candy.device import run_motor
import time, os


def initialise(node, wallet=None):
    candy_iota = iota_payment.cryptoWallet(os.environ['FERNET_KEY'], node)
    if wallet is None:
        print("No wallet Found")
        wallet = candy_iota.initialise_wallet()
        api, inputs = candy_iota.load_wallet(wallet)
    else:
        api, inputs = candy_iota.load_wallet(wallet)

    last_balance, active_address = candy_iota.update_balance(wallet, len(inputs))
    summary = "Wallet Initialised:\n\nActive Address: {0}\nAddress Balance: {1}".format(active_address, last_balance)
    print(summary)

    while True:
        balance, active_address = candy_iota.active_address_balance(api, len(inputs))
        if balance > last_balance:
            payment = balance - last_balance
            print("Payment Received! {} iota".format(payment))
            print("Dispensing...")
            run_motor.dispense(3)
            print("Enjoy your candy")

            last_balance, active_address = candy_iota.update_balance(wallet, len(inputs))

        print(balance)
        time.sleep(3)