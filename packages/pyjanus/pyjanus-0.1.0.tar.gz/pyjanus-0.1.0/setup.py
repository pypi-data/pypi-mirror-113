# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyjanus', 'pyjanus.plugins']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'pyee>=8.1.0,<9.0.0', 'websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'pyjanus',
    'version': '0.1.0',
    'description': 'janus-gateway python client',
    'long_description': '# pyjanus\njanus-gateway python client\n\n## Usage\n```\nfrom pyjanus import Client\nfrom pyjanus.plugins.videoroom import ListparticipantsRequest\n\nclient = Client(\'wss://janus.conf.meetecho.com/ws\')\nawait client.connect()\n\nsession = await client.create_session(keepalive_timeout=9)\nhandle = await session.attach("janus.plugin.videoroom")\n\n# send request\ntr = await handle.send({"request": "list"})\nresponse = await tr.response\n\n# send request use plugin model\ntr = await handle.send(ListparticipantsRequest(room=1234).dict(exclude_none=True))\nresponse = await tr.response\n```',
    'author': 'Jiang Yue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skymaze/pyjanus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
