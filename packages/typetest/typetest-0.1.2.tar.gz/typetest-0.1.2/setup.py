# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typetest']

package_data = \
{'': ['*'], 'typetest': ['results/placeholder']}

install_requires = \
['blessed>=1.18.1,<2.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'pandas>=1.3.0,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['typetest = typetest.__main__:run',
                     'typetest-analyse = typetest.analyse:run']}

setup_kwargs = {
    'name': 'typetest',
    'version': '0.1.2',
    'description': 'Test your typing speed without leaving the terminal.',
    'long_description': '<p align="center">\n  <img src="./img/logo.png" width="300"/>\n</p>\n<p align="center">Test your typing speed without leaving the terminal.</p>\n\n<p align="center">\n  <a href="https://github.com/mastermedo/typetest">\n    <img src="https://img.shields.io/github/languages/code-size/mastermedo/typetest" alt="build" title="build"/>\n  </a>\n  <a href="https://github.com/mastermedo/typetest/LICENSE">\n    <img src="https://img.shields.io/github/license/mastermedo/typetest" alt="license" title="license"/>\n  </a>\n  <a href="https://github.com/mastermedo/typetest/stargazers">\n    <img src="https://img.shields.io/badge/maintainer-mastermedo-yellow" alt="maintainer" title="maintainer"/>\n  </a>\n</p>\n\n<p align="center">\n  <a href="https://github.com/mastermedo/typetest">\n    <img src="./img/typetest-demo.gif" alt="demo" title="demo"/>\n  </a>\n</p>\n\n## :clipboard: description\n`typetest` is a self-contained minimal typing test program written with [blessed](https://github.com/jquast/blessed/).\nAs is, it is a near clone of [10fastfingers](https://10fastfingers.com/typing-test/english) with an added bonus of being able to see typing speed as you\'re typing.\n\n## :zap: features\n1. adjustable settings\n2. storing test results\n3. analysing mistakes\n4. easy to track improvement\n\n## :chart_with_upwards_trend: analyse test results\n![wpm](./img/wpm.png)\n![char_speeds](./img/char_speeds.png)\n![word_speeds](./img/word_speeds.png)\n![mistypes](./img/mistypes.png)\n![dist](./img/dist.png)\n\n## :shipit: installation\n\n1. install python 3\n2. install [blessed](https://pypi.org/project/blessed/)\n3. clone this repository\n4. run `python typetest -s -d 60 < common_300`\n5. (optional) add `typetest` to path or make an alias like `tt`\n6. (optional) store your results in some file and analyse\n\n## :bulb: ideas for tests\nAlong with `typetest` this repository features sample tests.\nTry them like so: `typetest -s -d 60 -i common_200` or scrape something off the internet, like a [featured article](https://en.wikipedia.org/wiki/Wikipedia:Featured_articles) on wikipedia.\n\n```python\n#!/usr/bin/env python3\nimport re\nimport requests\nfrom bs4 import BeautifulSoup\n\nword_pattern = re.compile(r"[\'A-Za-z\\d\\-]+[,\\.\\?\\!]?")  # symbols to keep\nurl = \'https://en.wikipedia.org/wiki/Special:RandomInCategory/Featured_articles\'\n\nr = requests.get(url)\nsoup = BeautifulSoup(r.text, \'html.parser\')\nfor sup in soup.select(\'sup\'):\n    sup.extract()  # remove citations\n\ntext = \' \'.join(p.text for p in soup.select(\'p\'))\ntext = re.sub(r\'\\[.*?\\]|\\(.*?\\)\', \'\', text)  # remove parenthesis\nprint(\' \'.join(re.findall(word_pattern, text)))\n```\nIf you create a file called `wiki_random` you can start the test with `wiki_random | typetest`.\nWrite your own scraper, you may find some suggestions [here](https://en.wikipedia.org/wiki/Lists_of_English_words).\n\n## :question: usage\n\n```\nusage: typetest [-h] [-d DURATION] [-i INPUT] [-o OUTPUT] [-s] [-r ROWS]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -d DURATION, --duration DURATION\n                        duration in seconds (default: inf)\n  -i INPUT, --input INPUT\n                        file to read words from (default: sys.stdin)\n  -o OUTPUT, --output OUTPUT\n                        file to store results in\n                        (default: /home/medo/repos/typetest/results)\n  -s, --shuffle         shuffle words (default: False)\n  -r ROWS, --rows ROWS  number of test rows to show (default: 2)\n\nexample:\n  typetest -i test.txt -s -d 60\n  echo \'The typing seems really strong today.\' | typetest -d 3.5\n  typetest < test.txt\n\nshortcuts:\n  ^c / ctrl+c           end the test and get results now\n  ^h / ctrl+h           backspace\n  ^r / ctrl+r           restart the same test\n  ^w / ctrl+w           delete a word\n  ^u / ctrl+u           delete a word\n```\n\n<p align="center">\n  <a href="#">\n    <img src="https://img.shields.io/badge/⬆️back_to_top_⬆️-white" alt="Back to top" title="Back to top"/>\n  </a>\n</p>\n',
    'author': 'MasterMedo',
    'author_email': 'mislav.vuletic@gmail.com',
    'maintainer': 'MasterMedo',
    'maintainer_email': 'mislav.vuletic@gmail.com',
    'url': 'https://github.com/MasterMedo/typetest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
