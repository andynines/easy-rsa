"""
easy_rsa.py
Copyright (c) 2017 andynines
MIT License
"""

#setup
from math import ceil, floor, sqrt
from random import SystemRandom
SR = SystemRandom()

class PublicKeyException(Exception):
    pass
class PrivateKeyException(Exception):
    pass
"""
Thrown if the calculation of the respective variable fails. When using the
Cipher class object, these errors are caught and a new set of variables is used.
"""
class MessageException(Exception):
    pass
"""
Thrown if a given message for a new Cipher object would break the calculation or
create an infinite loop.
"""

#prime number functions
def is_prime(number):
    """
    Returns true or false for whether the given number is prime. Primality is
    not defined mathematically for non-integers or values less than 2.
    """
    if number < 2:
        return False
    for factor in range(2, floor(sqrt(number)) + 1):
        if number % factor == 0:
            return False
    return True

def relatively_prime(a, b):
    """
    Returns true or false for whether the given numbers are relatively prime,
    having no common factors other than 1.
    """
    for number in range(2, min(a, b) + 1):
        if a % number == b % number == 0:
            return False
    return True

def sieve(limit):
    """
    Returns a list of prime numbers up to but not including the given number.
    """
    array = [True] * limit                          
    array[0] = array[1] = False
    primes = []
    for (number, prime) in enumerate(array):
        if prime:
            primes.append(number)
            for index in range(number * number, limit, number):
                array[index] = False
    return primes

def random_integer(minimum, maximum, prime=False, exclusions=[]):
    """
    Returns a cryptographically secure random integer in the interval [a, b).
    If prime is set to True, the result will be prime. The result will not be a
    value contained within the exclusions argument.
    """
    if prime:
        numbers = sieve(maximum)
    else:
        numbers = list(range(minimum, maximum))
    for number in numbers:
        if number in exclusions or number < minimum:
            numbers.remove(number)
    return SR.choice(numbers)

#rsa functions
formula = lambda text, key, modulus: [(character ** key) % modulus for character in text]
"""
Returns a list of the values of a[x]^b mod c for every element of a. This is the
format of RSA's encryption and decryption formulas m^e mod n and c^d mod n
respectively.
"""

totient = lambda a, b: (a - 1) * (b - 1)
"""
Returns an evaluation of Euler's totient function for two values a and b.
"""

def generate_public(phi):
    """
    Generates a public key in the interval [3, phi) raising a PublicKeyException
    if it fails.
    """
    for attempt in range(3, phi):
        if relatively_prime(attempt, phi):
            return attempt
    raise PublicKeyException("Could not generate e for given value of phi")

MAXIMUM_COEFFICIENT = 10

def generate_private(e, phi):
    """
    Generates a private key given the values of the public key and ϕn using
    brute force. If the calculation reaches MAXIMUM_COEFFICIENT before
    succeeding, a PrivateKeyException is raised. A higher MAXIMUM_COEFFICIENT
    value may result in OverflowError, as the private key will later be used
    as an exponent during the decryption process.
    """
    for coefficient in range(3, MAXIMUM_COEFFICIENT + 1):
        attempt = phi * coefficient + 1
        if attempt % e == 0:
            return int(attempt / e)
    raise PrivateKeyException("Private key calculation reached maximum phi coefficient before succeeding")

class Cipher(object):
    def __init__(self, m):
        """
        Creates an RSA cryptosystem for a given plaintext.
        """
        if not m:
            raise MessageException("Message is blank or uninterpretable")
        while True:
            try:
                self.m = [ord(character) for character in list(str(m))]
                largest_m = max(self.m)
                """
                The RSA algorithm works properly so long as the modulus n is
                greater than any ordinal that makes up the message m. To ensure
                this is always the case, the smallest possible modulus that
                could be generated would be the product of the largest m
                ordinal's square root if it is prime, and the next prime after
                that number, since p and q must be two distinct primes. In this
                way such an edge case is prevented entirely.
                """
                self.p = random_integer(ceil(sqrt(largest_m)), largest_m, prime=True)
                self.q = random_integer(ceil(sqrt(largest_m)), largest_m, prime=True, exclusions=[self.p])
                self.n = self.p * self.q
                self.phi = totient(self.p, self.q)
                self.e = generate_public(self.phi)
                self.d = generate_private(self.e, self.phi)
                self.c = formula(self.m, self.e, self.n)
                assert self.m != self.c
                break
            except (PublicKeyException, PrivateKeyException, AssertionError):
                continue

#demo
def main():
    """
    An I/O loop that takes messages and encrypts them for the user.
    """
    EXIT_COMMAND = "/e"

    print("Easy RSA loaded successfully")
    print("Provide a message for encryption or type {} to exit\n".format(EXIT_COMMAND))
    while True:
        message = input(">")
        if len(message) >= len(EXIT_COMMAND) and message[:len(EXIT_COMMAND)] == EXIT_COMMAND:
            break
        try:
            encryption = Cipher(message)
        except MessageException:
            print("An error occurred\n")
            continue
        print("Unicode ordinals (m) " + ", ".join([str(ordinal) for ordinal in encryption.m]),
              "First prime (p) " + str(encryption.p),
              "Second prime (q) " + str(encryption.q),
              "Modulus (n) " + str(encryption.n),
              "Totient (phi(n)) " + str(encryption.phi),
              "Public key (e) " + str(encryption.e),
              "Private key (d) " + str(encryption.d),
              "Encrypted ordinals (c) " + ", ".join([str(ordinal) for ordinal in encryption.c]) + "\n",
              sep="\n")

if __name__ == "__main__":
    main()
