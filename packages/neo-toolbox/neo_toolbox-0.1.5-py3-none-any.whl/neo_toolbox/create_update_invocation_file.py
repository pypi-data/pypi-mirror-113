import json
from base64 import b64encode


def create_update_invocation_file(
        contract_name: str,
        nef_file_path: str,
        manifest_file_path: str,
        operation='update'
) -> str:
    """
    Create a Neo Express invocation file that can be used to update a smart contract.

    :param contract_name: The name of the smart contract to update.
    :param nef_file_path: The path to the smart contract NEF file.
    :param manifest_file_path: The path to the smart contract manifest file.
    :param operation: The name of the operation/method on the smart contract.
    :return: Returns the invocation script as JSON.
    :rtype: str
    """
    invocation_dict = {
        'contract': contract_name,
        'operation': operation,
    }

    args = []

    with open(nef_file_path, 'rb') as file:
        raw_bytes = file.read()
        args.append({
            'type': 'ByteArray',
            'value': raw_bytes.hex(),
        })

    with open(manifest_file_path, 'rb') as file:
        raw_bytes = file.read()
        args.append({
            'type': 'ByteArray',
            'value': raw_bytes.hex(),
        })

    invocation_dict['args'] = args

    return json.dumps([invocation_dict])
