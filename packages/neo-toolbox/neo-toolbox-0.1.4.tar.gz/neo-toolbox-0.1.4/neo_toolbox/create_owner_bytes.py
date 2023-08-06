from neo_toolbox.data_transformation import decode_address


def create_owner_bytes(address):
    hash_hex = decode_address(address)
    hash_bytes = bytearray.fromhex(hash_hex)
    hash_bytes.reverse()

    as_string = str(bytes(hash_bytes))

    return f"OWNER = UInt160({as_string})"
