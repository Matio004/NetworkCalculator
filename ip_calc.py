from typing import Union


class Octet:
    def __init__(self, octet: Union[int, list], base: int = 10):
        self.__octet = octet
        self.__base = base

        self.__max10 = 255

        self.check_for_errors()

    def __repr__(self):
        return str(self.__octet) if self.__base == 10 else ''.join(map(str, self.__octet))

    @property
    def octet(self):
        return self.__octet

    @property
    def base(self):
        return self.__base

    def check_for_errors(self):
        self.to_decimal()

        if self.__octet > self.__max10:
            raise ValueError('Octet should be a decimal number 0-255')

    def to_binary(self):
        if self.__base != 2:
            self.__octet = list(map(int, bin(self.__octet)[2:]))
            self.__octet = [0] * (8 - len(self.__octet)) + self.__octet
            self.__base = 2

            return self

    def to_decimal(self):
        if self.__base != 10:
            self.__octet = int(''.join(map(str, self.__octet)), self.__base)
            self.__base = 10

            return self

    def __add__(self, other):
        self.to_decimal()

        return Octet(self.__octet+other.octet)

    def __sub__(self, other):
        self.to_decimal()

        return Octet(self.__octet-other.octet)

    def __invert__(self):
        self.to_binary()

        new = []

        for bit in range(len(self.__octet)):
            new.append(int(not int(self.__octet[bit])))
        self.to_decimal()

        return Octet(new, 2)

    def __and__(self, other):
        self.to_decimal()

        return Octet(self.__octet & other.octet)

    def __len__(self):
        self.to_binary()
        temp = len(self.__octet)
        self.to_decimal()
        return temp

    def count(self, x: int):
        self.to_binary()

        x = self.__octet.count(x)

        self.to_decimal()
        return x


class IPv4:
    def __init__(self, ipv4: str, base: int = 10):
        self.__ipv4 = [Octet(int(i) if base == 10 else list(map(int, list(i))), base) for i in ipv4.split('.')]
        self.__base = base

        self.check_for_errors()

    @classmethod
    def from_cidr(cls, cidr: int):
        if cidr <= 32:
            iterable = '1' * cidr + '0' * (32 - cidr)
            instance = cls('.'.join([iterable[i:i + 8] for i in range(0, len(iterable), 8)]), 2)
            return instance.to_decimal()
        raise ValueError("Cidr can't be higher than 32")

    @property
    def ipv4(self):
        return self.__ipv4

    def __repr__(self):
        return '.'.join(map(str, self.__ipv4))

    def check_for_errors(self):
        [octet.check_for_errors() for octet in self.__ipv4]

        if len(self.__ipv4) != 4:
            raise ValueError('IPv4 contains 4 octets. Octet value should be 0-255')

    def to_binary(self):
        for octet in self.__ipv4:
            if octet.base != 2:
                octet.to_binary()
        return self

    def to_decimal(self):
        for octet in self.__ipv4:
            if octet.base != 10:
                octet.to_decimal()
        return self

    def __add__(self, other):
        new = []
        for octet in range(len(self.__ipv4)):
            new.append(str(self.__ipv4[octet] + other.ipv4[octet]))
        return IPv4('.'.join(new))

    def __sub__(self, other):
        new = []
        for octet in range(len(self.__ipv4)):
            new.append(str(self.__ipv4[octet] - other.ipv4[octet]))
        return IPv4('.'.join(new))

    def __invert__(self):
        new = []

        for octet in range(len(self.__ipv4)):
            new.append(str(~self.__ipv4[octet]))
        return IPv4('.'.join(new))

    def __and__(self, other):
        new = []
        for octet in range(len(self.__ipv4)):
            new.append(str(self.__ipv4[octet] & other.ipv4[octet]))
        return IPv4('.'.join(new))

    def count(self, x: int):
        count_ = 0
        for octet in range(len(self.__ipv4)):
            count_ += self.__ipv4[octet].count(x)
        return count_


class Network:
    def __init__(self, ip: str, mask: str = None):
        if mask is None:
            self.__mask = IPv4.from_cidr(int(ip.split('/')[-1]))
            self.ip = IPv4(ip.split('/')[0])
        else:
            self.ip = IPv4(ip)
            self.__mask = IPv4(mask)

    def __repr__(self):
        return f'IP: {self.ip}\nMask: {self.__mask}'

    @property
    def network_address(self):
        return self.ip & self.__mask

    @property
    def broadcast_address(self):
        return self.network_address + ~self.__mask

    @property
    def host0(self):
        return self.network_address + IPv4('0.0.0.1')

    @property
    def host_1(self):
        return self.broadcast_address - IPv4('0.0.0.1')

    @property
    def max_hosts(self):
        return 2 ** self.__mask.count(0) - 2


if __name__ == '__main__':
    while True:
        try:
            net = Network(input('Podaj adres ip i skrócony zapis maski: '))

            print(f'\nAdres sieci: {net.network_address}\n'
                  f'Adres rozgłoszeniowy: {net.broadcast_address}\n'
                  f'Adres pierwszego hosta: {net.host0}\n'
                  f'Adres ostatniego hosta: {net.host_1}\n'
                  f'Liczba hostów do zaadresowania: {net.max_hosts}\n')

        except ValueError:
            print('Wprowadź dane ponownie...')

        except KeyboardInterrupt:
            print('Koniec')
            break
