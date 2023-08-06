from neo_toolbox.data_transformation import decode_address


def create_owner_bytes(address):
    """
    Creates a small template that can be used in Boa3 smart contracts to identify owner of a contract.

    :param address: The address of the owner of the contract. E.g. NNpbB25aNMY2pD5JkWeAEbsNfp7C3GoZF1
    :return: Returns a template that can be copied to the smart contract.
    :rtype: str
    """

    hash_hex = decode_address(address)
    hash_bytes = bytearray.fromhex(hash_hex)
    hash_bytes.reverse()

    as_string = str(bytes(hash_bytes))

    return f"OWNER = UInt160({as_string})"
