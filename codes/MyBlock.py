# L58ikTm6wWbCimikPFHwC3Q5mHJaJqnhJ5hkrkeeFHyqKXgLeyWu
# sid last 4 digits: (81019)9357

import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from bitcoin.core import Hash160, Hash, b2lx, b2x
from bitcoin.core.key import CPubKey
from utils import *
import codecs
import time
import struct
import secrets

bitcoin.SelectParams("mainnet") 
# Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret(
    "Kzi6GgXjYo8nGVBtdQE6emmgoEhVqjFhca94SWkuvBbLEDuMaCKf")
# Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
print(my_public_key)
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
print(my_address)
# 19tF26qNQMySYhDdZRuCbLJ9kN62BiDrgu

# destination_address = bitcoin.wallet.CBitcoinAddress('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
#  Destination address (recipient of the money)


MAGIC_NUMBER = 0xD9B4BEF9
BLOCK_REWARD = 6.25
TXID = 64 * '0'
VOUT = 'FFFFFFFF'
TX_CNT = b'\x01'
def get_txin_scriptPubKey():
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]

def create_transaction(sigScript_data: str):
    txout_scriptPubKey = get_txin_scriptPubKey()
    # 256 bit == 32 byte == 64 hex
    txid_to_spend = 64 * '0'

    txin = create_txin(txid_to_spend, int(VOUT, 16))
    txout = create_txout(BLOCK_REWARD, txout_scriptPubKey)

    data_hex = sigScript_data.encode('ascii').hex()
    scriptSig = [bytes.fromhex(data_hex)]
    txin.scriptSig = CScript(scriptSig)
    return CMutableTransaction([txin], [txout])

def cal_block_bytes(header, block_body):
    mgc_num_little = MAGIC_NUMBER.to_bytes(4, 'little')
    block_size = len(header) + len(TX_CNT) + len(block_body)
    return mgc_num_little + struct.pack('<L', block_size) + header + TX_CNT + block_body

def cal_target(bits):
    exp = int(bits[:2], 16)
    magnitude = int(bits[2:], 16)
    target = magnitude * (2 ** (8 * (exp - 3)))
    target = f'{target:x}'.zfill(64)
    return bytes.fromhex(target)

# print(cal_target('180696f4').hex())

def print_result(version, prev_block_hash, merkle_root,
             time_stamp, bits, nonce, hash_rate, hash, header, body):
  print('Version:', version)
  print('Previous Block Hash:', prev_block_hash)
  print('Merkle Root:', merkle_root)
  print('Time Stamp:', time_stamp)
  print('Bits:', bits)
  print('Nonce:', nonce)
  print('---')
  print(f'Hash Rate: {hash_rate:.2f} H/s')
  print('Block Hash:', b2lx(hash))
  print('Block Header:', header.hex())
  print('Block Hex:', b2x(cal_block_bytes(header, body)))
  print('Block Body:', body.hex())

def mine(prev_block_hash: str, coinbase_data: str):
    version = 1
    bits = '1f010000'

    transaction = create_transaction(coinbase_data)
    body = transaction.serialize()
    merkle_root = b2lx(Hash(body))

    time_stamp = int(time.time())
    block_header = struct.pack('<L', version)
    block_header += bytes.fromhex(prev_block_hash)[::-1]
    block_header += bytes.fromhex(merkle_root)[::-1]
    block_header += struct.pack('<LL', time_stamp, int(bits, 16))
    print('Block_header:', block_header.hex())
    
    start_time = time.time()
    nonce = 0
    target = cal_target(bits)
    print(target.hex())
    while nonce < 2 ** 32:
        header = block_header + struct.pack('<L', nonce)
        hash = Hash(header)
        if hash[::-1] < target:
            hash_rate = nonce / (time.time() - start_time)
            print_result(version, prev_block_hash, merkle_root,\
                          time_stamp, bits, nonce, hash_rate, hash, header, body)
            return
        nonce += 1


if __name__ == '__main__':
    prev_block_hash = '00000000b7c37ebcca8672e12da0dfaebbc6f8808ce57e5fff7123259d51d644'
    coinbase_data = '810199357SepehrAzardar'
    mine(prev_block_hash, coinbase_data)