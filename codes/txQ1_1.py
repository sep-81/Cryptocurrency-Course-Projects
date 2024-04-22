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

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key] 

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx)

def unspendable_script_PubKey():
    return [OP_RETURN]

def public_spentdable_script_PubKey():
    return [OP_TRUE]


def create_two_outputs_signed_transaction(txin, first_txout, second_txout,
                                  txin_scriptPubKey,txin_scriptSig):
    tx = CMutableTransaction([txin], [first_txout, second_txout])
    txin.scriptSig = CScript(txin_scriptSig)
    VerifyScript(txin.scriptSig, CScript(txin_scriptPubKey),tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx
def create_two_outputs_OP_CHECKSIG_signature(txin, first_txout,\
                                              second_txout, txin_scriptPubKey, seckey):
    tx = CMutableTransaction([txin], [first_txout, second_txout])
    sighash = SignatureHash(CScript(txin_scriptPubKey), tx,
                            0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    return sig
    
def scriptSig(txin, first_txout, second_txout, txin_scriptPubKey):
    signature = create_two_outputs_OP_CHECKSIG_signature(txin, first_txout,\
                         second_txout, txin_scriptPubKey, my_private_key)
    return [signature, my_public_key]

def gen_tx(first_amount_to_spend, second_amount_to_spend, txid_to_spend, utxo_index,
                                first_txout_scriptPubKey, second_txout_scriptPubKey):
    first_txout = create_txout(first_amount_to_spend, first_txout_scriptPubKey)
    second_txout = create_txout(second_amount_to_spend, second_txout_scriptPubKey)
    txin_scriptPubKey = P2PKH_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = scriptSig(txin, first_txout, second_txout, txin_scriptPubKey)

    new_tx = create_two_outputs_signed_transaction(txin, first_txout,
                                second_txout, txin_scriptPubKey,txin_scriptSig)
    return broadcast_transaction(new_tx)



if __name__ == '__main__':
    unspnt_amount = 0.00001 # Amount of BTC in the output you're splitting minus fee
    spendable_amount = 0.015
    txid_to_spend = ('f359191ee9cdeb2e9b17b13f420a5b9abc693305b2e4af735515684c54b85fea') # TxHash of UTXO
    utxo_index = 1

    print(my_address) # Prints your address in base58
    print(my_public_key.hex()) # Print your public key in hex
    print(my_private_key.hex()) # Print your private key in hex

    first_txout_scriptPubKey = unspendable_script_PubKey()
    second_txout_scriptPubKey = public_spentdable_script_PubKey()
    response = gen_tx(unspnt_amount, spendable_amount, txid_to_spend,
                       utxo_index, first_txout_scriptPubKey, second_txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text) # Report the hash of transaction which is printed in this section result


    # txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    # response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    # print(response.status_code, response.reason)
    # print(response.text) # Report the hash of transaction which is printed in this section result
