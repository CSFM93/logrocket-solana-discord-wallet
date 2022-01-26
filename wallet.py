from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer

import json

solana_client = Client("https://api.devnet.solana.com")


def create_account(sender_username):
    try:
        kp = Keypair.generate()
        public_key = str(kp.public_key)
        secret_key = kp.secret_key

        data = {
            'public_key': public_key,
            'secret_key': secret_key.decode("latin-1"),
        }

        file_name = '{}.txt'.format(sender_username)
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)

        return public_key

    except Exception as e:
        print('error:', e)
        return None


def load_wallet(sender_username):
    try:
        file_name = '{}.txt'.format(sender_username)
        with open(file_name) as json_file:
            account = json.load(json_file)
            account['secret_key'] = account['secret_key'].encode("latin-1")
            return account
            
    except Exception as e:
        print(e)
        return None


def fund_account(sender_username, amount):
    try:
        amount = int(1000000000 * amount)
        account = load_wallet(sender_username)
        resp = solana_client.request_airdrop(
            account['public_key'], amount)   
        print(resp)    
        
        transaction_id = resp['result']
        if transaction_id != None:
            return transaction_id
        else:
            return None

    except Exception as e:
        print('error:', e)
        return None


def get_balance(sender_username):
    try:
        account = load_wallet(sender_username)
        resp = solana_client.get_balance(account['public_key'])
        print(resp)
        balance = resp['result']['value'] / 1000000000
        data = {
            "publicKey": account['public_key'],
            "balance": str(balance),
        }
        return data
    except Exception as e:
        print('error:', e)
        return None


def send_sol(sender_username, amount, receiver):
    try:
        account = load_wallet(sender_username)
        sender = Keypair.from_secret_key(account['secret_key'])
        amount = int(1000000000 * amount)

        txn = Transaction().add(transfer(TransferParams(
            from_pubkey=sender.public_key, to_pubkey=PublicKey(receiver), lamports=amount)))
        resp = solana_client.send_transaction(txn, sender)
        print(resp)

        transaction_id = resp['result']
        if transaction_id != None:
            return transaction_id
        else:
            return None

    except Exception as e:
        print('error:', e)
        return None        