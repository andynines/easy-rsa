readme.txt

About
---
Easy RSA is a Python library for implementing simple RSA cryptosystems. This
was written only for educational purposes; its security is not guaranteed.

Contents
---
-PublicKeyException and PrivateKeyException: for if their respective
calculations happen to fail.
-is_prime(number): returns true or false for whether the given number is prime.
-relatively_prime(a, b): returns true or false for whether the given numbers
are relatively prime, having no common factors other than 1.
-sieve(limit): yields primes up to but not including the given number. Must be
iterated through to make use of; my_primes = [prime for prime in sieve(100)]
-random_integer(a, b): returns a cryptographically secure random integer in the
interval [a, b] inclusively.
-random_prime(a, b, exclusions = [x, y, ...]): returns a cryptographically
secure random prime in the interval [a, b] inclusively.
-formula(a, b, c): returns the value of a^b mod c. This is the format of RSA's
encryption and decryption formulas m^e mod n and c^d mod n respectively.
-totient(a, b): returns the value of (a - 1) * (b - 1) according to Euler's
totient function.
-generate_public(phi): generates a public key in the interval [3, phi), raising
a PublicKeyException if it fails.
-generate_private(e, phi): generates a private key given the values of the
public key and ϕn using brute force. If the calculation reaches
MAXIMUM_COEFFICIENT before succeeding, a PrivateKeyException is raised.
-Cipher(message): Creates an RSA cryptosystem for a given plaintext.

Use
---
>>> import easy_rsa
>>> my_encryption = Cipher("Romeo Sierra Alfa") #creating a new encryption
>>> my_encryption.m #the message's Unicode ordinals
[82, 111, 109, 101, 111, 32, 83, 105, 101, 114, 114, 97, 32, 65, 108, 102, 97]
>>> my_encryption.c #the message's encrypted ordinals
[4597, 6070, 9824, 3158, 6070, 2811, 7995, 2601, 3158, 9380, 9380, 10573, 2811,
3009, 5463, 991, 10573]
>>> "".join([chr(ordinal) for ordinal in my_encryption.c]) #the encryption
interpreted as Unicode
'ᇵា♠ౖា\u0afbἻ\u0a29ౖ⒤⒤⥍\u0afbுᕗϟ⥍'
>>> "".join([chr(ordinal) for ordinal in formula(my_encryption.c,
my_encryption.d, my_encryption.n)]) #decrypting the message
'Romeo Sierra Alfa'