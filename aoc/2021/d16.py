from dataclasses import dataclass
from math import prod

_ops = {
    '000': sum,
    '001': prod,
    '010': min,
    '011': max,
    '101': lambda l: int(l[0] > l[1]),
    '110': lambda l: int(l[0] < l[1]),
    '111': lambda l: int(l[0] == l[1])
}


@dataclass
class Packet:
    ver: str
    data: str = '0'
    type: str = '100'
    kids: list = tuple()

    def version(self):
        return int(self.ver, 2)

    def value(self):
        return int(self.data, 2)

    def calc(self):
        if self.type == '100':
            return self.value()
        else:
            fun = _ops[self.type]
            return fun([k.calc() for k in self.kids])

    def flatten(self):
        if type == '100':
            return [self]
        else:
            return [self, *(s for kid in self.kids for s in kid.flatten())]


def parse_packet(packet):
    ver, type = packet[:3], packet[3:6]
    packet = packet[6:]
    if type == '100':
        out = ''
        while True:
            f, nyb = packet[0], packet[1:5]
            out += nyb
            packet = packet[5:]
            if f == '0':
                break
        return Packet(ver, out), packet
    else:  # other type
        if packet[0] == '0':  # length
            L = int(packet[1:16], 2)
            rest = packet[16 + L:]
            packet = packet[16:16 + L]
            kids = []
            while packet:
                sub, packet = parse_packet(packet)
                kids.append(sub)
            return Packet(ver, type=type, kids=kids), rest

        else:  # count
            N = int(packet[1:12], 2)
            rest = packet[12:]
            kids = []
            for i in range(N):
                sub, rest = parse_packet(rest)
                kids.append(sub)
            return Packet(ver, type=type, kids=kids), rest


def part1(data):
    packet = bin(int(data, 16))[2:]
    L = len(packet)
    packet = packet.zfill(L + ((-L) % 4))

    p, _ = parse_packet(packet)

    return sum(p.version() for p in parse_packet(packet)[0].flatten())


def part2(data):
    packet = bin(int(data, 16))[2:]
    L = len(packet)
    packet = packet.zfill(L + ((-L) % 4))

    p, _ = parse_packet(packet)

    return p.calc()


def main(data):
    print(f'part 1: {part1(data)}')

    print(f'part 2: {part2(data)}')


if __name__ == '__main__':
    from aocd import data

    # test_data = """38006F45291200"""
    test_data = """EE00D40C823060"""
    assert part1("""8A004A801A8002F478""") == 16
    assert part1("""620080001611562C8802118E34""") == 12
    assert part1("""A0016C880162017C3686B18A3D4780""") == 31

    # main(test_data)
    main(data)
