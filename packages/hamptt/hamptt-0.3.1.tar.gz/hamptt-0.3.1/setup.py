# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hamptt', 'hamptt.boards']

package_data = \
{'': ['*']}

install_requires = \
['func_timeout>=4.3.5']

extras_require = \
{'bt': ['PyBluez>=0.23']}

setup_kwargs = {
    'name': 'hamptt',
    'version': '0.3.1',
    'description': 'Implementation of Push-To-Talk board for ham radio transmitters like Baofeng UV-5R',
    'long_description': 'Ham PTT\n=======\n\nBluetooth PTT switch for ham radio transmitters like Baofeng UV-5R.  \nBoard helps to control transmitter from PC.\n\nProblematic\n-----------\n\nTesting of UART interface showed unstable connection. During transmit via UART an usb-ttl \nchip periodically crashes and stops working. Cause is some radio strong interference \non USB cable. So Bluetooth serial protocol stack chosen instead.\n\nSchematic\n---------\n\nHost -> (Bluetooth) -> Esp-32 Arduino -> Relay -> Transmitter PTT button\n\n* Hardware\n\n    - Host PC with Bluetooth (tested Ubuntu 20.04)\n    - Esp32 DevKit v1 (or similar esp32)\n    - Relay shield\n    - Baofeng UV-5R\n\nExamples\n--------\n\n- Find BT devices `hcitool scan`\n- Python\n\n```python3\nfrom hamptt import open_ptt\n\nwith open_ptt(bt_addr="A0:B1:C2:D3:E4:F5") as ptt:\n    ptt.begin()\n    # I.e. play message to transmitter or something else\n    ptt.end()\n```\n\nInstall\n-------\n\n* Host PC machine\n\n    - Python 3.8\n    - Bluetooth\'s libs (required for pybluez)\n\n      ```shell\n      sudo apt-get install bluez libbluetooth-dev\n      ```\n\n    - Pip\n      ```shell\n      python3 -m pip install "hamptt[bt]"\n      ```\n\n\n* Esp32\n\n    - Upload sketch to your esp-32 via PlatformIO  \n      NOTE! Check your board config in `platformio.ini` (see: https://platformio.org/)\n      ```\n      pio run -t upload\n      ``` \n\n    - Connect pins Esp-32 to relay\n\n        - VVC -> Relay +\n        - GND -> Relay -\n        - GPIO D25 -> Relay IN\n\n    - Connect relay and audio, for Baofeng UV-5R it looks like:\n\n      ![Baofeng UV-5R Pins](https://www.dxzone.com/dx33739/baofeng-mic-pin-out-and-programming-cable-schematics.jpg "Baofeng UV-5R Pins")  \n      NOTE: You can rebuild your hands-free cable or buy another one\n\nDevelopment\n===========\n\n* Build and install\n  ```shell\n  pip3 uninstall hamptt\n  rm -rf dist && poetry build && pip3 install ./dist/*.whl\n  ```\n  \n* Publish\n  - Prepare  \n     ```shell\n    poetry config repositories.testpypi https://test.pypi.org/legacy/\n    poetry config pypi-token.testpypi <TOKEN>\n    \n    poetry config repositories.pypi https://upload.pypi.org/legacy/\n    poetry config pypi-token.pypi <TOKEN>\n    ```  \n  \n  - Publish\n    ```shell\n    poetry publish --build -r testpypi\n    \n    poetry publish --build -r pypi\n    ````',
    'author': 'mrkeuz',
    'author_email': 'mr.keuz@ya.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrkeuz/hamptt/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
