from hashlib import sha256
from typing import List

ADDRESS_VERSION_BYTE_N3 = '35'


def base_58_encode(num):
    """Converts a number into Base-58."""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    encoded: List[str] = []
    alpha_cnt: int = len(alphabet)

    if num < 0:
        return ''

    while num >= alpha_cnt:
        mod = num % alpha_cnt
        num //= alpha_cnt
        encoded.append(alphabet[mod])

    if num > 0:
        encoded.append(alphabet[num])

    return ''.join(encoded[::-1])


def base_58_decode(ins: str) -> int:
    """Converts a Base-58 encoded integer, as string, back to a number."""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    multi: int = 1
    decoded: int = 0
    alpha_cnt: int = len(alphabet)

    for char in ins[::-1]:
        decoded += multi * alphabet.index(char)
        multi *= alpha_cnt

    return decoded


def pad_address(hex_string):
    raw_byes = bytearray.fromhex(ADDRESS_VERSION_BYTE_N3 + hex_string)
    hashed_address = sha256(raw_byes)
    double_hashed_address = sha256(hashed_address.digest())
    double_hashed_address_hex = double_hashed_address.digest().hex()
    return ADDRESS_VERSION_BYTE_N3 + hex_string + double_hashed_address_hex[0:8]


def reverse_hex(hex_string):
    raw_bytes = bytearray.fromhex(hex_string)
    raw_bytes.reverse()
    return raw_bytes.hex()


def encode_hash(hash_hex: str):
    reversed_hex = reverse_hex(hash_hex)
    padded_address = pad_address(reversed_hex)
    return base_58_encode(int(padded_address, 16))


def decode_address(address: str):
    raw_hash = base_58_decode(address)
    hash_hex = hex(raw_hash)[4:-8]
    hash_bytes = bytearray.fromhex(hash_hex)
    hash_bytes.reverse()
    return hash_bytes.hex()
