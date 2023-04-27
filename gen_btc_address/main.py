from ecdsa import SigningKey, SECP256k1
from hashlib import new, sha256
from binascii import unhexlify
from base58 import b58encode

def gen_btc_wallet(printa=False): 
    # gen ecdsa private key
    # ecdsa stands for Elliptic Curve Digital Signature Algorithm
    # https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
    ecdsaPrivateKey = SigningKey.generate(curve=SECP256k1)
    if printa: print("ECDSA Private Key: ", ecdsaPrivateKey.to_string().hex())

    # derive ecdsa pub key from the private key
    ecdsaPublicKey = '04' +  ecdsaPrivateKey.get_verifying_key().to_string().hex()
    if printa: print("ECDSA Public Key: ", ecdsaPublicKey)

    # ripemd160(sha256(ecdsa pub key)) 
    ridemp160FromHash256 = new('ripemd160', unhexlify(sha256(unhexlify(ecdsaPublicKey)).hexdigest()))
    if printa: print("RIDEMP160(SHA256(ECDSA Public Key)): ", ridemp160FromHash256.hexdigest())

    # prepend '00'
    prependNetworkByte = '00' + ridemp160FromHash256.hexdigest()
    hash = prependNetworkByte

    # get checksum of hash
    for x in range(1,3):
        hash = sha256(unhexlify(hash)).hexdigest()
        if printa: print("\t|___>SHA256 #", x, " : ", hash)
    cheksum = hash[:8]
    if printa: print("Checksum(first 4 bytes): ", cheksum)

    # encode in base58 to get btc address
    bitcoinAddress = b58encode(unhexlify(prependNetworkByte + cheksum))
    if printa: print("Bitcoin Address: ", bitcoinAddress.decode('utf8'))

    return ecdsaPrivateKey.to_string().hex(), bitcoinAddress.decode('utf8')

if __name__ == '__main__':
    private_key, btc_address = gen_btc_wallet()
    print(f'{private_key=}\n{btc_address=}')
    # to double check if address is valid
    # https://thomas.vanhoutte.be/tools/validate-bitcoin-address.php
