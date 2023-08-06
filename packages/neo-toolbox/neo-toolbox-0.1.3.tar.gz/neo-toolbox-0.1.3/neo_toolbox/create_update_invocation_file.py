import json
from base64 import b64encode


def create_update_invocation_file(
        contract_name,
        nef_file_path,
        manifest_file_path,
        operation='update'
) -> str:
    """  """
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
