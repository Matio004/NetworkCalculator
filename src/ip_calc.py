from argparse import ArgumentParser
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
    arg_parser = ArgumentParser(
        'ip_calc', description='CLI for network calculator. By default it gives all information in verbose form',
        epilog='Program developed for IT in high school'
    )
    arg_parser.add_argument('-a', '--address', type=str,
                            help='ip address and mask in CIDR form. If you wish to give mask explicitly use -m.')
    arg_parser.add_argument('-m', '--mask', type=str,
                            help='mask defined as ip address')
    arg_parser.add_argument('-n', '--network', action='store_true', help='show network address')
    arg_parser.add_argument('-b', '--broadcast', action='store_true', help='show broadcast address')
    arg_parser.add_argument('-f', '--first', action='store_true', help='show first host address')
    arg_parser.add_argument('-l', '--last', action='store_true', help='show last host address')
    arg_parser.add_argument('-c', '--count', action='store_true', help='show count of available ip addresses')

    args = arg_parser.parse_args()

    if not args.address:
        raise ValueError('No ip address was provided')
    else:
        if args.mask:
            try:
                net = Network(args.address, args.mask)
            except ValueError:
                raise ValueError('Address must be a valid ip. If you have used -m then there should be no cidr given.')
        else:
            try:
                net = Network(args.address)
            except ValueError:
                raise ValueError('It is not a valid ip address. Remember you must specify cidr')

        if any((args.network, args.broadcast, args.first, args.last, args.count)):
            if args.network:
                print(f'Network Address: {net.network_address}')
            if args.broadcast:
                print(f'Broadcast Address: {net.broadcast_address}')
            if args.first:
                print(f'First Host Address: {net.host0}')
            if args.last:
                print(f'Last Host Address: {net.host_1}')
            if args.count:
                print(f'Number of addressable hosts: {net.max_hosts}')

        else:
            print(f'\nNetwork Address: {net.network_address}\n'
                  f'Broadcast Address: {net.broadcast_address}\n'
                  f'First Host Address: {net.host0}\n'
                  f'Last Host Address: {net.host_1}\n'
                  f'Number of addressable hosts: {net.max_hosts}\n')
