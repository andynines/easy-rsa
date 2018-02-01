# Easy RSA
Easy RSA is a Python library and application for implementing simple RSA
cryptosystems. It has been written only for educational purposes; its security
is not guaranteed.
## License
The contents of this repository are made available under the MIT License.
## Import use
	>>> from easy_rsa import *
	>>> my_encryption = Cipher("Romeo Sierra Alfa") #creating a new encryption
	>>> my_encryption.m #the message's Unicode ordinals
	[82, 111, 109, 101, 111, 32, 83, 105, 101, 114, 114, 97, 32, 65, 108, 102, 97]
	>>> my_encryption.c #the message's encrypted ordinals
	[4597, 6070, 9824, 3158, 6070, 2811, 7995, 2601, 3158, 9380, 9380, 10573, 2811,
	3009, 5463, 991, 10573]
	>>> "".join([chr(ordinal) for ordinal in my_encryption.c]) #the encryption interpreted as Unicode
	'ᇵា♠ౖា\u0afbἻ\u0a29ౖ⒤⒤⥍\u0afbுᕗϟ⥍'
	>>> "".join([chr(ordinal) for ordinal in formula(my_encryption.c, my_encryption.d, my_encryption.n)]) #decrypting the message
	'Romeo Sierra Alfa'
## Application use
	Easy RSA loaded successfully
	Provide a message for encryption or type /e to exit

	>Romeo Sierra Alfa
	Unicode ordinals (m) 82, 111, 109, 101, 111, 32, 83, 105, 101, 114, 114, 97, 32, 65, 108, 102, 97
	First prime (p) 19
	Second prime (q) 37
	Modulus (n) 703
	Totient (phi(n)) 648
	Public key (e) 5
	Private key (d) 389
	Encrypted ordinals (c) 689, 555, 523, 233, 555, 242, 182, 364, 233, 95, 95, 526, 242, 373, 90, 410, 526
