from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto import Random
import base64
import codecs

# 打开客户端私钥签名
with open('private_client.pem') as prifile:
    private_key = RSA.import_key(prifile.read())
print("private_key:",private_key)

# 打开客户端公钥验签
with open('public_client.pem') as pubfile:
    public_key = RSA.import_key(pubfile.read())
print("public_key:",public_key)

message = B'To be signed'



h = MD5.new(message)
print('-----------------')
signer = PKCS1_v1_5.new(private_key)
signature = signer.sign(h)
print(signature)
hexlify = codecs.getencoder('hex')
# m = hexlify(signature)[0]  # <--- I am sending this hex signature to JS.
# --------------Code below is to test the verify in python, n it works !
h = MD5.new(B'To be signed')


verifier = PKCS1_v1_5.new(public_key.publickey())
if verifier.verify(h, signature):
    print("The signature is authentic.")
else:
    print("The signature is not authentic.")

