#easy_rsa.py

"""
MIT License

Copyright AardvarkNines (c) 2017 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from math import ceil, floor, sqrt
from random import SystemRandom
SR = SystemRandom()

class PublicKeyException(Exception):
    pass
class PrivateKeyException(Exception):
    pass

#prime numbers
def is_prime(number):
    if number < 2:
        return False
    for factor in range(2, floor(sqrt(number)) + 1):
        if number % factor == 0:
            return False
    return True

def relatively_prime(a, b):
    for number in range(2, min(a, b) + 1):
        if a % number == b % number == 0:
            return False
    return True

def sieve(limit):
    array = [True] * limit                          
    array[0] = array[1] = False
    for (number, primality) in enumerate(array):
        if primality:
            yield number
            for index in range(number * number, limit, number):
                array[index] = False

random_integer = lambda minimum, maximum: SR.randint(minimum, maximum)

def random_prime(minimum, maximum, exclusions = []):
    primes = [prime for prime in sieve(maximum)]
    for prime in primes:
        if prime in exclusions:
            primes.remove(prime)
    return SR.choice(primes)

#rsa procedure
formula = lambda text, key, modulus: [(character ** key) % modulus for character in text]

totient = lambda a, b: (a - 1) * (b - 1)

def generate_public(phi):
    for attempt in range(3, phi):
        if relatively_prime(attempt, phi):
            return attempt
    raise PublicKeyException("Could not generate e for given value of phi")

MAXIMUM_COEFFICIENT = 100

def generate_private(e, phi):
    for coefficient in range(3, MAXIMUM_COEFFICIENT + 1):
        attempt = (phi * coefficient + 1) / e
        if attempt == int(attempt):
            return int(attempt)
    raise PrivateKeyException("Private key calculation reached maximum phi coefficient before succeeding")

class Cipher(object):
    def __init__(self, m):
        self.m = [ord(character) for character in list(str(m))]
        largest_m = max(self.m)
        self.p = random_prime(ceil(sqrt(largest_m)), largest_m)
        self.q = random_prime(ceil(sqrt(largest_m)), largest_m, exclusions = [self.p])
        self.n = self.p * self.q
        self.phi = totient(self.p, self.q)
        self.e = generate_public(self.phi)
        self.d = generate_private(self.e, self.phi)
        self.c = formula(self.m, self.e, self.n)
