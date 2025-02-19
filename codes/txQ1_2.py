import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") 
# Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("91gWQy7rGeTJZ2WGK35eisqs21xhk7WoJPtitPhGKQfjzeyoP9F")
 # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

# destination_address = bitcoin.wallet.CBitcoinAddress('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
#  Destination address (recipient of the money)

def P2PKH_scriptPubKey():
    return [ OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY , OP_CHECKSIG] 

def get_txin_scriptPubKey():
    return [OP_TRUE]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key] 

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = get_txin_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)

    # txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,[])

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_to_send = 0.001 # Amount of BTC in the output you're splitting minus fee
    txid_to_spend = ('9666c747c3d2f599fddd24355876d5587ba70c9b4810c6b0ca950e65172bc030') # TxHash of UTXO
    utxo_index = 1
    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = P2PKH_scriptPubKey()
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
