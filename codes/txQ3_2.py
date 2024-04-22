# 585881
# 579613
import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") 
# Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("92iTSz8mrm1LEBjtDpUXhJXFRDhhPHXeyZK6Y9pbT6XbBUiLJvd")
 # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

# destination_address = bitcoin.wallet.CBitcoinAddress('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
#  Destination address (recipient of the money)

def my_locking_script(sum_byte, sub_byte):
    return [OP_2DUP, OP_ADD, OP_HASH160, Hash160(sum_byte),
             OP_EQUALVERIFY,OP_SUB, OP_HASH160, Hash160(sub_byte), OP_EQUAL]

def my_unlocking_script(p1,p2):
    return [p1,p2]


def get_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]


def run(amount_to_send, txid_to_spend, utxo_index):
  prime_num1 = 9851
  prime_num2 = 7789
  sum_prm = prime_num1 + prime_num2
  sub_prm = prime_num1 - prime_num2
  sum_bytes = sum_prm.to_bytes(2,'little')
  sub_bytes = sub_prm.to_bytes(2,'little')

  
  txout_scriptPubKey = get_txin_scriptPubKey()
  txout = create_txout(amount_to_send, txout_scriptPubKey)
  txin_scriptPubKey = my_locking_script(sum_bytes, sub_bytes)

  txin = create_txin(txid_to_spend, utxo_index)

  txin_scriptSig = my_unlocking_script(prime_num1.to_bytes(2,'little'), prime_num2.to_bytes(2,'little'))
  new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)
  response =  broadcast_transaction(new_tx)
  
  print(response.status_code, response.reason)
  print(response.text)

if __name__ == '__main__':
  amount_to_send = 0.001 # Amount of BTC in the output you're splitting minus fee
  txid_to_spend = ('9b6b4628fa4958c8ff6f16661f8478539c6d0b717952fed1a4f6f5e305284992') # TxHash of UTXO
  utxo_index = 0
  print(my_address) # Prints your address in base58
  print(my_public_key.hex()) # Print your public key in hex
  print(my_private_key.hex()) # Print your private key in hex
  run(amount_to_send, txid_to_spend, utxo_index)
