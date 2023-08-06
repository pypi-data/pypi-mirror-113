# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neo_toolbox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'neo-toolbox',
    'version': '0.1.5',
    'description': 'Tools for working with the Neo N3 blockchain.',
    'long_description': '# Neo Toolbox\n\nSmall toolkit for interacting with the Neo N3 blockchain.\n\n### Available tools\n\n1. [Data Transformation](#data_transformation)\n2. [Create Owner Bytes](#create_owner_bytes)\n3. [Create Update Invocation File](#create_update_invocation_file)\n\n\n\n#### <a name="data_transformation"></a>Data Transformation\n\nLets you convert between wallet hashes and addresses.\n\n##### Example\n\n```python\nfrom neo_toolbox.data_transformation import encode_hash, decode_address\n\n# Encode a wallet hash\noriginal_hash_hex = \'a7271ccc82bb311db369719d1868e6ac19ece31f\'\naddress = encode_hash(original_hash_hex)\nprint(address)\n# Outputs: \'NNpbB25aNMY2pD5JkWeAEbsNfp7C3GoZF1\'\n\n# Decode a wallet address\noriginal_address = \'NNpbB25aNMY2pD5JkWeAEbsNfp7C3GoZF1\'\nhash_hex = decode_address(original_address)\nprint(hash_hex)\n# Outputs: \'a7271ccc82bb311db369719d1868e6ac19ece31f\'\n```\n\n\n#### <a name="create_owner_bytes"></a>Create Owner Bytes\n\nThis helper function lets you convert a N3 wallet address to an python variable that can be used\nin your smart contract to verify the owner of the contract. This is very useful to add admin\nfunctionality to your smart contract.\n\n##### Example\n\n```python\nfrom neo_toolbox.create_owner_bytes import create_owner_bytes\n\noriginal_address = \'NNpbB25aNMY2pD5JkWeAEbsNfp7C3GoZF1\'\ncode_snippet = create_owner_bytes(original_address)\nprint(code_snippet)\n# Outputs: \'OWNER = UInt160(b"\\x1f\\xe3\\xec\\x19\\xac\\xe6h\\x18\\x9dqi\\xb3\\x1d1\\xbb\\x82\\xcc\\x1c\'\\xa7")\'\n```\n\n#### <a name="create_update_invocation_file"></a>Create Update Invocation File\n\nThis helper function lets you create a [Neo Express](https://github.com/neo-project/neo-express)\ninvocation file that can be used to update a smart contract.\n\n##### Example\n\n```python\nfrom neo_toolbox.create_update_invocation_file import create_update_invocation_file\n\nnef_file = \'path/to/sample_contract.nef\'\nmanifest_file = \'path/to/sample_contract.manifest.json\'\ntemplate = create_update_invocation_file(\'your_contract_name\', nef_file, manifest_file, operation=\'my_custom_update\')\nprint(template)\n# Outputs a JSON string: \'[{"contract": ...\'\n```\n\n\n*Created and maintained by Adapted AS (Norway).*',
    'author': 'Adrian Fjellberg',
    'author_email': 'adrian@adapted.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
