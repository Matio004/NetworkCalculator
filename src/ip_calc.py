from typing import Union, Optional


class Octet:
    __octet: int

    def __init__(self, octet):
        if isinstance(octet, int):
            self.__octet = octet
        else:
            self.__octet = octet.__octet

        self.check_for_errors()

    def __repr__(self):
        return f'Octet({self.__octet})'

    def __str__(self):
        return f'{self.__octet}'

    def check_for_errors(self):
        if self.__octet > 255:
            raise ValueError('Octet should be a decimal number 0-255!')
        if self.__octet < 0:
            raise ValueError('Octet can\' be lower than 0!')

    def __add__(self, other):
        return Octet(self.__octet+other.__octet)

    def __sub__(self, other):
        return Octet(self.__octet-other.__octet)

    def __invert__(self):
        return Octet(~self.__octet & ((1 << 8) - 1))

    def __and__(self, other):
        return Octet(self.__octet & other.__octet)

    def __len__(self):
        return 8

    def __eq__(self, other):
        return self.__octet == other.__octet

    def count(self, x: int):
        temp = self.__octet
        count = 0

        while temp:
            count += temp & 1
            temp >>= 1
        return count if x else 8 - count


class IPv4:
    def __init__(self, *args, ip: Optional[Union[list[int], list[Octet], tuple[int], tuple[Octet]]] = None):
        if len(args) != 4:
            raise IndexError('IPv4 is 4 bytes')
        self.__ipv4 = [Octet(i) for i in (args if ip is None else ip)]

        self.check_for_errors()

    @classmethod
    def from_cidr(cls, cidr: int):
        if cidr <= 32:
            temp = 0
            for _ in range(cidr):
                temp <<= 1
                temp |= 1
            temp <<= 32 - cidr
            return cls.from_int(temp)
        raise ValueError("Cidr can't be higher than 32")

    @classmethod
    def from_int(cls, ip: int):
        temp = [0] * 4

        for i in range(3, -1, -1):
            temp[i] = ip & 255
            ip >>= 8
        return cls(*temp)

    @classmethod
    def from_string(cls, ip: str):
        return cls(*list(map(int, ip.split('.'))))

    def __repr__(self):
        return '.'.join(map(str, self.__ipv4))

    def check_for_errors(self):
        [octet.check_for_errors() for octet in self.__ipv4]

        if len(self.__ipv4) != 4:
            raise ValueError('IPv4 contains 4 octets. Octet value should be 0-255')

    def __add__(self, other):
        new = []
        for octet in range(len(self.__ipv4)):
            new.append(self.__ipv4[octet] + other.__ipv4[octet])
        return IPv4(*new)

    def __sub__(self, other):
        new = []
        for octet in range(len(self.__ipv4)):
            new.append(self.__ipv4[octet] - other.__ipv4[octet])
        return IPv4(*new)

    def __invert__(self):
        new = []

        for octet in range(len(self.__ipv4)):
            new.append(~self.__ipv4[octet])
        return IPv4(*new)

    def __and__(self, other):
        new = []
        for octet in range(len(self.__ipv4)):
            new.append(self.__ipv4[octet] & other.__ipv4[octet])
        return IPv4(*new)

    def __eq__(self, other):
        for i in range(len(self.__ipv4)):
            if self.__ipv4[i] != other.__ipv4[i]:
                return False
        return True

    def count(self, x: int):
        count_ = 0
        for octet in range(len(self.__ipv4)):
            count_ += self.__ipv4[octet].count(x)
        return count_


class Network:
    def __init__(self, ip: str, mask: str = None):
        if mask is None:
            self.__mask = IPv4.from_cidr(int(ip.split('/')[-1]))
            self.__ip = IPv4.from_string(ip.split('/')[0])
        else:
            self.__ip = IPv4.from_string(ip)
            self.__mask = IPv4.from_string(mask)

    def __repr__(self):
        return f'IP: {self.__ip}\nMask: {self.__mask}'

    @property
    def network_address(self):
        return self.__ip & self.__mask

    @property
    def broadcast_address(self):
        return self.network_address + ~self.__mask

    @property
    def host0(self):
        return self.network_address + IPv4.from_int(1)

    @property
    def host_1(self):
        return self.broadcast_address - IPv4.from_int(1)

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

        except ValueError as ex:
            print(ex)
            print('Wprowadź dane ponownie...')

        except KeyboardInterrupt:
            print('Koniec')
            break
