import operator
import random
from unittest import TestCase

from src.ip_calc import Octet, IPv4


class TestOctet(TestCase):
    def test_count(self):
        temp = '0', '1',
        for _ in range(2 ** 8):
            string = ''.join(random.choices(temp, k=8))
            self.assertEqual(Octet(int(string, 2)).count(0), string.count('0'))
            self.assertEqual(Octet(int(string, 2)).count(1), string.count('1'))

    def test_add(self):
        for _ in range(255):
            x, y = random.randint(0, 255), random.randint(0, 255)
            if x + y > 255:
                self.assertRaises(ValueError, lambda: operator.add(Octet(x), Octet(y)))
            else:
                self.assertEqual(Octet(x) + Octet(y), Octet(x + y))

    def test_sub(self):
        for _ in range(255):
            x, y = random.randint(0, 255), random.randint(0, 255)
            if x - y < 0:
                self.assertRaises(ValueError, lambda: operator.sub(Octet(x), Octet(y)))
            else:
                self.assertEqual(Octet(x) - Octet(y), Octet(x - y))

    def test_invert(self):
        for _ in range(255):
            x = random.randint(0, 255)
            self.assertEqual(~Octet(x), Octet(~x & ((1 << 8) - 1)))

    def test_and(self):
        for _ in range(255):
            x, y = random.randint(0, 255), random.randint(0, 255)
            self.assertEqual(Octet(x) & Octet(y), Octet(x & y))


class TestIPv4(TestCase):
    def test_from_cidr(self):
        for _ in range(32):
            x = random.randint(0, 32)
            self.assertEqual(IPv4.from_cidr(x).count(1), x)
            self.assertEqual(IPv4.from_cidr(x).count(0), 32 - x)

    def test_from_int(self):
        self.assertEqual(IPv4.from_int(0b11111111_00000000_00000000_00000001), IPv4(255, 0, 0, 1))

    def test_from_string(self):
        self.assertEqual(IPv4.from_string('192.168.0.1'), IPv4(192, 168, 0, 1))

    def test_count(self):
        for i in range(32):
            self.assertEqual(IPv4.from_cidr(i).count(1), i)

    def test_add(self):
        self.assertEqual(IPv4(192, 168, 1, 0) + IPv4(0, 0, 0, 1), IPv4(192,168, 1, 1))

    def test_sub(self):
        self.assertEqual(IPv4(192, 168, 1, 255) - IPv4(0, 0, 0, 1), IPv4(192, 168, 1, 254))

    def test_invert(self):
        self.assertEqual(~IPv4.from_cidr(30), IPv4.from_int(3))

    def test_and(self):
        self.assertEqual(IPv4(192, 168, 0, 1) & IPv4.from_cidr(8), IPv4(192, 0, 0, 0))

