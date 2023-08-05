import _libhsmd


print(dir(_libhsmd))
print(_libhsmd.__file__)

msg = '000b0488b21e0488ade46fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d61900000000000000000000'
#import pdb;pdb.set_trace()

response = _libhsmd.init('00'*32, "bitcoin")
print(response)


# Try to sign a message:

req = (
    '0017'  # type 23
    '000B'  # len = 11
    '48656c6c6f20776f726c64'  # "Hello world" in hex
)

for i in range(1):
    response = _libhsmd.handle(1024, 0, None, req)
print(response)

assert response.startswith('007b')
assert len(response) / 2 == 67
