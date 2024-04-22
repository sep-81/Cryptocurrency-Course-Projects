import hashlib
import base58
import codecs
import ecdsa
import secrets

test_net_prk_version = b"\xef"
test_net_pbk_version = b"\x6f"

def convert_str_to_hex(str:str):
  return codecs.encode(str.encode(),'hex').decode("utf-8")

def random_gen():
  return secrets.token_hex(32)
  
def check_sum(inp:bytes):
  return hashlib.sha256(hashlib.sha256(inp).digest()).digest()[0:4]

def wif_converter(prk:str, is_compressed=b""):
  """prk is hex encoded string"""
  hashed = test_net_prk_version+codecs.decode(prk, 'hex')
  return base58.b58encode(hashed + is_compressed + check_sum(hashed)).decode('utf-8')

def uncomp_public_key_generator(prk:str):
  """prk is hex encoded string"""
  prk_bytes = codecs.decode(prk, 'hex')
  pbk_raw = ecdsa.SigningKey.from_string(prk_bytes, curve=ecdsa.SECP256k1).verifying_key
  pbk_bytes = pbk_raw.to_string()
  # bytes to hex encoded string
  return pbk_bytes.hex()

def to_compressed(uncomp_pbk:str):
  '''hex encoded string and without 04 at beginning'''
  bytes_val = codecs.decode(uncomp_pbk[-2:], 'hex')
  int_val = int.from_bytes(bytes_val,'big')
  compress_prefix=0
  if int_val % 2 == 0 :
    compress_prefix = '02'
  else :
    compress_prefix = '03'
  return compress_prefix + uncomp_pbk[:64]

def convert_pbk_to_addr(pbk:str):
  """pbk is hex encoded string"""
  if(pbk.__len__() == 128):
    pbk = '04' + pbk
  sha_dige = hashlib.sha256(codecs.decode(pbk,'hex')).digest()
  rip = hashlib.new('ripemd160')
  rip.update(sha_dige)
  hashed = rip.hexdigest()  
  hashed = test_net_pbk_version.hex() + hashed
  # addr is bytes
  addr = codecs.decode(hashed, 'hex') + check_sum(codecs.decode(hashed, 'hex'))
  return base58.b58encode(addr).decode('utf-8')


def addr_gen(prk:str):
  print("private key: ", wif_converter(prk)) 
  pbk = uncomp_public_key_generator(prk)
  print("uncompressed public key: ", pbk)
  print("compressed public key: ", to_compressed(pbk))
  addr = convert_pbk_to_addr(pbk)
  print("addr: ", addr)
  return addr

def vanity_generator(prefix:str):
  while True:
    prk = random_gen()
    pbk = uncomp_public_key_generator(prk)
    addr = convert_pbk_to_addr(pbk)
    print("addr: ", addr)
    if addr[1:1+prefix.__len__()] == prefix:
      print("vanity prk: ", prk)
      print("prk wif: " + wif_converter(prk))
      return addr     


# print(wif_converter('a22a031135fb9bb416ba65d0bdf706337eafbb4739f0c4ff375aeaf7d189301a'))


if __name__ == '__main__':
    # random = random_gen()
    random = '4772d0115f7f0c4b812583432969ff32840c2c7e59a47a2ef0de1c01e3cb1b46'
    print((random))
    print("your wallet addr is: ", addr_gen(random))
    print('vanity addr for sp: ' + vanity_generator('sp'))

'''
vanity prk:  7f60d9e49f3ee3829687c85e1c935d674c52c6a061f97991f5daaf1bec72f7c0
prk base58(wif): 92Z1sW9bbsUrANc1ZYAFSaVLiL7qsDJYtrokz8Zw99bZen592PL
vanity addr for sp: msepu7tvnB1fqq4k4cd73X8jsuADVx87vL
addr: msepu7tvnB1fqq4k4cd73X8jsuADVx87vL
pubk: 04d32efb2a388ad01c5208a3445eb710689e9c74941521c4c7788dcf9071cee537aecb5281c459db9896df5c0e3c32c96a25e3abbe389ec453f1e4362ab5d402fa
prk: 7f60d9e49f3ee3829687c85e1c935d674c52c6a061f97991f5daaf1bec72f7c0
'''

'''
vanity prk:  a22a031135fb9bb416ba65d0bdf706337eafbb4739f0c4ff375aeaf7d189301a
prk wif: 92pLRm8cK9FLAzLRnQxGTyCBwFiri5f65vmnCzYWMvJdCzt8tvC
vanity addr for sp: msepTuQpcFh93KffFp6bUfRcvcgPDu61zy

'''

'''
third one:
vanity prk:  06c85f016e260273cd8361f41e0660ab37e3c83219efd2c5979f5e8a6aeeeb16
prk wif: 91duRCxLRu36WSb5UG9bL9MPuJVmz4BChv8ebVMaBz6dgpxHRyW
vanity addr for sp: mspmzEYcoSrZXzvXWwkE3gcyNHUPC9UqFq

'''

'''
mian one:
vanity prk:  0cb1a9189abc27f06f09dd9dad5ffab769d16cd252f5078c838d361db549acea
prk wif: 91gWQy7rGeTJZ2WGK35eisqs21xhk7WoJPtitPhGKQfjzeyoP9F
vanity addr for sp: mspyV97GWXj2ZgbiCmtAAhq1aKQukB43f2

'''
'''
wif: 92tyjesFurdTjfzeJu4mZSGrKxVhEuZL1tu92HZCcoeTugDchhY
pbk: mspBonaqNwnZ7dwcn8Pe1WYVCgGwXtHakj
'''

'''
vanity prk:  5582245916e067cb3f4b40fc2da0f7a061c96e2234776ff1eeebd96e84053667
prk wif: 92EaMpD3ZCKs917dbxyXWFo42pesAfqL3HTZm9EqXYGnCefMSjq
vanity addr for sp: mspG86PFVaT1zLeeJYStBLNxC1SZUwUHB4

'''

'''
vanity prk:  8240f80f50cb9af74e529250a9db97d351d0fa87b836c3df47bbb0178f13d855
prk wif: 92aHKbBxhGp9iXuvZFRdZhUHxDYgEwrWuUM2HYTvDdrPyPKNFzb
vanity addr for sp: mspKRoDjG2avwMUjAYsG1z1tUSjAvz7Qtf
'''

'''
vanity prk:  94d0b3b6f49eb393672d2881fe1da86d3d6e792bd7167ecb06c36c9f28839d21
prk wif: 92iTSz8mrm1LEBjtDpUXhJXFRDhhPHXeyZK6Y9pbT6XbBUiLJvd
vanity addr for sp: mspgmvMnYGEEwfkYRTuDMuHjySwn5ZBxm2

'''