# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arrakisclient',
 'arrakisclient.tests',
 'arrakisclient.types',
 'arrakisclient.types.tests',
 'authzed',
 'authzed.api.v0',
 'authzed.api.v1alpha1',
 'grpcutil',
 'validate']

package_data = \
{'': ['*']}

install_requires = \
['async_generator>=1.10,<2.0',
 'grpcio==1.34.0',
 'mock>=4.0.3,<5.0.0',
 'protobuf>=3.14.0,<4.0.0',
 'protoc-gen-validate>=0.4.1,<0.5.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6']}

setup_kwargs = {
    'name': 'authzed',
    'version': '0.3.0',
    'description': 'Client library for the Authzed service.',
    'long_description': '# Authzed Python Client\n\nThis repository houses the Python client library for Authzed.\n\nThe library maintains various versions the Authzed gRPC APIs.\nYou can find more info on each API on the [Authzed API reference documentation].\nAdditionally, Protobuf API documentation can be found on the [Buf Registry Authzed API repository].\n\n[Authzed API Reference documentation]: https://docs.authzed.com/reference/api\n[Buf Registry Authzed API repository]: https://buf.build/authzed/api/docs/main\n\nSupported API versions:\n- v1alpha1\n- v0\n- arrakisclient (v0 Legacy ORM)\n\n## Installation\n\n```\npip install authzed\n```\n\n## Example\n\nEverything API specific is in its respective `authzed.api.VERSION` module.\n`grpcutil` contains functionality for making interacting with gRPC simple.\n\n```python\nfrom authzed.api.v1alpha1 import Client, ReadSchemaRequest\nfrom grpcutil import bearer_token_credentials\n\n\nclient = Client("grpc.authzed.com:443", bearer_token_credentials("mytoken"))\nresp = client.ReadSchema(ReadSchemaRequest(object_definitions_names=["example/user"]))\nprint(resp.object_definitions)\n```\n\nIf an event loop is running when the client is initialized, all functions calls are async:\n\n```python\nimport asyncio\n\nfrom authzed.api.v1alpha1 import Client, ReadSchemaRequest\nfrom grpcutil import bearer_token_credentials\n\n\nasync def async_new_client():\n    # Within an async context, the client\'s methods are all async:\n    client = Client("grpc.authzed.com:443", bearer_token_credentials("mytoken"))\n    resp = await client.ReadSchema(ReadSchemaRequest(object_definitions_names=["example/user"]))\n    print(resp)\n\nloop = asyncio.get_event_loop()\ntry:\n    loop.run_until_complete(async_new_client())\nfinally:\n    loop.close()\n```\n\n## Full Examples\n\nFull examples for each version of the API can be found in the [examples directory](examples).\n',
    'author': 'Authzed',
    'author_email': 'support@authzed.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
