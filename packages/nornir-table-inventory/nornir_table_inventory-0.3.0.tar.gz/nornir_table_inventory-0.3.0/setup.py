# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_table_inventory', 'nornir_table_inventory.plugins.inventory']

package_data = \
{'': ['*']}

install_requires = \
['nornir>=3.0.0,<4.0.0', 'pandas>=1.2.0,<2.0.0']

entry_points = \
{'nornir.plugins.inventory': ['CSVInventory = '
                              'nornir_table_inventory.plugins.inventory.table:CSVInventory',
                              'ExcelInventory = '
                              'nornir_table_inventory.plugins.inventory.table:ExcelInventory',
                              'FlatDataInventory = '
                              'nornir_table_inventory.plugins.inventory.table:FlatDataInventory']}

setup_kwargs = {
    'name': 'nornir-table-inventory',
    'version': '0.3.0',
    'description': 'nornir inventory plugin,support managing inventory by csv or excel file',
    'long_description': '[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)\n[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n\n\n# nornir_table_inventory\n\nThe nornir_table_inventory is [Nornir](https://github.com/nornir-automation/nornir) plugin for inventory.It can manage inventory by table file(CSV or Excel).\nNetmiko connections support only.\n\nIt doesn\'t support groups or defaults,because it focuses on flat data,and the data lies in table file of two-dimensional.\n\n\n\nnornir_table_inventory supports 2  inventory classes .\n- `CSVInventory` manages inventory by csv file\n- `ExcelInventory` manages inventory by excel(xlsx) file\n\n## Installing\n\n\n```bash\npip install nornir-table-inventory\n```\n\n## Example usage\n\n### Using the Nornir configuration file\n\n```yaml\n---\ninventory:\n      plugin: CSVInventory\n      options:\n          csv_file: "inventory.csv"\n\nrunner:\n    plugin: threaded\n    options:\n        num_workers: 100\n```\n```python\nfrom nornir import InitNornir\n\n\nnr = InitNornir(config_file=r\'config.yml\')\n\nfor n, h in nr.inventory.hosts.items():\n  print(\'host name:\', n)\n  print(\'host hostname:\', h.hostname)\n  print(\'host username:\', h.username)\n  print(\'host password:\', h.password)\n  print(\'host platform:\', h.platform)\n  print(\'host port:\', h.port)\n  print(\'host data:\', h.data)\n  print(\'host netmiko details:\', h.connection_options.get(\'netmiko\').dict())\n  print(\'=\'*150)\n```\n\n\n### Using the InitNornir function by dict data\n\n```python\nfrom nornir import InitNornir\n\nrunner = {\n    "plugin": "threaded",\n    "options": {\n        "num_workers": 100,\n    },\n}\ninventory = {\n    "plugin": "ExcelInventory",\n    "options": {\n        "excel_file": "inventory.xlsx",\n    },\n}\n\nnr = InitNornir(runner=runner, inventory=inventory)\n\nfor n, h in nr.inventory.hosts.items():\n  print(\'host name:\', n)\n  print(\'host hostname:\', h.hostname)\n  print(\'host username:\', h.username)\n  print(\'host password:\', h.password)\n  print(\'host platform:\', h.platform)\n  print(\'host port:\', h.port)\n  print(\'host data:\', h.data)\n  print(\'host netmiko details:\', h.connection_options.get(\'netmiko\').dict())\n  print(\'=\'*150)\n\n```\n\n\n\n### CSVInventory arguments\n\n```\nArguments:\n    csv_file: csv file path，optional，default:inventory.csv\n```\n\n### ExcelInventory arguments\n\n```\nArguments:\n    excel_file: excel file path，optional，default:inventory.xlsx（Microsoft Office EXCEL 2007/2010/2013/2016/2019）\n```\n\n# Table Instructions\n\n|name|hostname|platform|port|username|password|city|model|netmiko_timeout|netmiko_secret|\n| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |\n|netdevops01|192.168.137.201|cisco_ios|22|netdevops|admin123!|bj|catalyst3750|60|admin1234!|\n|netdevops02|192.168.137.202|cisco_ios|22|netdevops|admin123!|shanghai|catalyst3750|60|admin1234!|\n\n- name：name of host\n\n- hostname： IP or fqdn of host\n\n- platform：netmiko\'s device_type\n\n- port：port of host,netmiko\'s port\n\n- username，password： username adn password of host\n\n- `netmiko_`prefix variables，will load into ConnectHandler（Netmiko）function to build netmiko ssh connection object.\n\n- `timeout conn_timeout auth_timeout banner_timeout blocking_timeout session_timeout` will be converted into int.If you define it in table\'s headers，you must assignment it，otherwise it will raise exception ，because it will call `int(None)`.\n\n- netmiko\'s `fast_cli` will be converted into boolean.values of  `false 0 None`(Case insensitive)will be converted into False，others will be converted into True。\n\n- others data such as city or model (any field name you can define) in the table will be host\'s data.\n\n\n  Above table will be used as following codes and result\n\n  ```python\n  from nornir import InitNornir\n  \n  nr = InitNornir(config_file=r\'config.yml\')\n  for n, h in nr.inventory.hosts.items():\n    print(\'host name:\', n)\n    print(\'host hostname:\', h.hostname)\n    print(\'host username:\', h.username)\n    print(\'host password:\', h.password)\n    print(\'host platform:\', h.platform)\n    print(\'host port:\', h.port)\n    print(\'host data:\', h.data)\n    print(\'host netmiko details:\', h.connection_options.get(\'netmiko\').dict())\n    print(\'=\'*150)\n  \n  ```\n\n  Results：\n\n  ```shell\n  host name: netdevops01\n  host hostname: 192.168.137.201\n  host username: netdevops\n  host password: admin123!\n  host platform: cisco_ios\n  host port: 22\n  host data: {\'city\': \'bj\', \'model\': \'catalyst3750\'}\n  host netmiko details: {\'extras\': {\'timeout\': 60, \'secret\': \'admin1234!\'}, \'hostname\': None, \'port\': None, \'username\': None, \'password\': None, \'platform\': None}\n  ======================================================================================================================================================\n  host name: netdevops02\n  host hostname: 192.168.137.202\n  host username: netdevops\n  host password: admin123!\n  host platform: cisco_ios\n  host port: 22\n  host data: {\'city\': \'shanghai\', \'model\': \'catalyst3750\'}\n  host netmiko details: {\'extras\': {\'timeout\': 60, \'secret\': \'admin1234!\'}, \'hostname\': None, \'port\': None, \'username\': None, \'password\': None, \'platform\':\n  ```\n\n  ',
    'author': 'feifeiflight',
    'author_email': 'feifeiflight@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jiujing/nornir_table_inventory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
