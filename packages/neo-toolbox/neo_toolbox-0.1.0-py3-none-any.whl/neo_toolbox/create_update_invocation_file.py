import json
from base64 import b64encode


def create_update_invocation_file(contract, nef_file_path, manifest_file_path, operation='update'):
    invocation_dict = {
        'contract': contract,
        'operation': operation,
    }

    args = []

    with open(nef_file_path, 'rb') as file:
        raw_bytes = file.read()
        args.append({
            'type': 'ByteString',
            'value': b64encode(raw_bytes).decode('ascii'),
        })

    with open(manifest_file_path, 'rb') as file:
        raw_bytes = file.read()
        args.append({
            'type': 'ByteString',
            'value': b64encode(raw_bytes).decode('ascii'),
        })

    invocation_dict['args'] = args

    return json.dumps([invocation_dict])
