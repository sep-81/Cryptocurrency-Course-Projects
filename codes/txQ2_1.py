import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") 
# Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("92tyjesFurdTjfzeJu4mZSGrKxVhEuZL1tu92HZCcoeTugDchhY")
prk1 = bitcoin.wallet.CBitcoinSecret("92Z1sW9bbsUrANc1ZYAFSaVLiL7qsDJYtrokz8Zw99bZen592PL")
prk2 = bitcoin.wallet.CBitcoinSecret("92pLRm8cK9FLAzLRnQxGTyCBwFiri5f65vmnCzYWMvJdCzt8tvC")
prk3 = bitcoin.wallet.CBitcoinSecret("91duRCxLRu36WSb5UG9bL9MPuJVmz4BChv8ebVMaBz6dgpxHRyW")
my_public_key = my_private_key.pub
pbk1 = prk1.pub
pbk2 = prk2.pub
pbk3 = prk3.pub


my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)

# destination_address = bitcoin.wallet.CBitcoinAddress('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
#  Destination address (recipient of the money)

def P2PKH_scriptPubKey():
    return [ OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY , OP_CHECKSIG] 


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key] 


def multiSig_output_script():
    return [OP_2, pbk1, pbk2, pbk3, OP_3, OP_CHECKMULTISIG]




def create_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)
    return broadcast_transaction(new_tx)

if __name__ == '__main__':
    amount_to_send = 0.01 # Amount of BTC in the output you're splitting minus fee
    txid_to_spend = ('796fb508ae77a6caa92b003b0e8c9af809b40fe2022b81f284f2dd1534e252c6') # TxHash of UTXO
    utxo_index = 0
    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex
    txout_scriptPubKey = multiSig_output_script()
    response = create_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result
