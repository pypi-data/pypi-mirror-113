# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spartan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spartan-py',
    'version': '0.2.0',
    'description': 'Library for spartan protocol',
    'long_description': '# spartan-py\n\nBasic spartan protocol implementation as a python library.\n\n```python\nimport spartan\n\nres = spartan.get("spartan://mozz.us/echo", "hi")\nwhile True:\n\tbuf = res.read()\n\tif not buf:\n\t\tbreak\n\tsys.stdout.buffer.write(buf)\nres.close()\n```\n\nTry it in the REPL:\n```python\n>>> import spartan\n>>> req = spartan.Request("spartan.mozz.us")\n>>> req\n>>> <Request spartan.mozz.us:300 / 0>\n>>> res = req.send()\n>>> res\n>>> 2 text/gemini\n>>> res.read()\n>>> [...]\n>>> res.close()\n```\n',
    'author': 'Hedy Li',
    'author_email': 'hedy@tilde.cafe',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~hedy/spartan-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
