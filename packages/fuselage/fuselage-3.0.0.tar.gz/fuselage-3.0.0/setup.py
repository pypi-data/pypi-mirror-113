# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuselage',
 'fuselage.changes',
 'fuselage.contrib',
 'fuselage.providers',
 'fuselage.resources']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fuselage = fuselage.main:main']}

setup_kwargs = {
    'name': 'fuselage',
    'version': '3.0.0',
    'description': 'Orchestration and configuration management in Python',
    'long_description': '# Fuselage\n\nfuselage is a simple and fast idempotent configuration bundle builder and runtime.\n\nTo use fuselage:\n\n* Use your code to build a configuration bundle via our API. The output is an executable payload. \n* Transfer that payload to your server.\n* Run it.\n\nShould you use fuselage? Probably not. But if you are wondering why:\n\n* It\'s **fast**. Unlike some configuration management tools the entire process runs on the target. It doesn\'t rely on a round trip between every step.\n* It\'s **small**. It\'s only dependency is a python3 interpreter on the target system plus some common posix binaries.\n* It\'s **secure**. It doesn\'t bring it\'s onw control plane that you need to understand in detail to properly secure.\n* It\'s **simple**. It provides the absolute minimum, and tries to get out the way for the stuff where it doesn\'t need to have an opinion. Bring your own template engine, or don\'t use one at all.  Bring your own control plane. Run it from a deamonset, run it via fabric or even just use scp and run it by hand.\n\n\n## Using with fabric\n\nYou will need to install fabric explicitly. Fuselage does not depend on fabric.\n\nYou can write simple deployment scripts with Fabric by adding this to your fabfile:\n\n```python\nfrom fuselage.fabric import blueprint\nfrom fuselage.resources import *\n\n@blueprint\ndef minecraft(bundle):\n    yield Directory(\n        name=\'/var/local/minecraft\',\n    )\n    yield Execute(\n        command=\'wget https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar\',\n        cwd="/var/local/minecraft",\n        creates="/var/local/minecraft/minecraft_server.1.8.jar",\n    )\n    yield File(\n        name=\'/var/local/minecraft/server.properties\',\n        contents=open(\'var_local_minecraft_server.properties\').read(),\n    )\n    yield File(\n        name="/etc/systemd/system/minecraft.service",\n        contents=open("etc_systemd_system_minecraft.service"),\n    )\n    yield Execute(\n        command="systemctl daemon-reload",\n        watches=[\'/etc/systemd/system/minecraft.service\'],\n    )\n    yield Execute(\n        command="systemctl restart minecraft.service",\n        watches=[\n            "/var/local/minecraft/server.properties",\n            "/etc/systemd/system/minecraft.service",\n        ]\n    )\n```\n\nAnd then run it against multiple servers::\n\n```bash\nfab -H server1,server2,server3 minecraft\n```\n',
    'author': 'Isotoma Limited',
    'author_email': 'support@isotoma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yaybu/fuselage',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
