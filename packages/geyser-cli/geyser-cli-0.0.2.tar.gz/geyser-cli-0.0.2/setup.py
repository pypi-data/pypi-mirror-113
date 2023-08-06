# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geyser']

package_data = \
{'': ['*'], 'geyser': ['assets/*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'tabulate>=0.8.9,<0.9.0', 'web3>=5.21.0,<6.0.0']

entry_points = \
{'console_scripts': ['geyser = geyser:main']}

setup_kwargs = {
    'name': 'geyser-cli',
    'version': '0.0.2',
    'description': 'A command line utility for the Ampleforth Geyser',
    'long_description': "<h1 align=center><code>Geyser-cli</code></h1>\n\n`geyser-cli` is an unofficial command line utility for checking the LP positions\nas well as the current value, denominated in USD, of a set of addresses\nparticipating in Ampleforth's Geyser.\n\n## Installation\n\n`pip install geyser-cli`\n\n## Setup\n\n### Ethereum node\n\n`geyser-cli` needs to talk to an Ethereum node. You can either use a local one\nor a hosted service.\nAnyway, set the node's URL as environment variable `$PROVIDER`.\n\nExample: `$ export PROVIDER=https://mainnet.infura.io/v3/<INFURA-PROJECT-ID>`\n\n## Commands\n\nChecking the available commands with `$ geyser --help` outputs:\n```\nUsage: geyser [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  status\n```\n\nAs shown in the output, there is currently only one command supported: `status`.\n\nWith the `status` command you can check the current status for a set of\naddresses.\n\nExample:\n```\n$ geyser status                            \\\ngov.merkleplant.eth                        \\\n0x6ad0586e4350bf0f4199d8a425fc646c485c3943 \\\n0xaE6dCd07fac9D7CccC98509120c1071048cDD8a1 \\\n0x31d6E97282e76450f04E91c13bfc47F1Fb27B0B6\n```\n\nOutput:\n```\n== gov.merkleplant.eth ==========\n\nOld Faithful\nToken    Balance      Value in $\n-------  ---------  ------------\nAMPL     211.54216       199.542\nUSDC     295.20488       295.205\n$$$                      494.75\n\n== 0x6Ad0586E4350Bf0F4199d8A425fc646C485C3943 ==========\n\nTrinity\nToken    Balance      Value in $\n-------  ---------  ------------\nAMPL     193.64992       182.664\nWETH     0.09840         178.163\nWBTC     0.00582         178.294\n$$$                      539.12\n\n== 0xaE6dCd07fac9D7CccC98509120c1071048cDD8a1 ==========\n\nBeehive\nToken    Balance       Value in $\n-------  ----------  ------------\nAMPL     2005.61831       1891.84\nWETH     1.01921          1845.33\n$$$                       3737.17\n\n== 0x31d6E97282e76450f04E91c13bfc47F1Fb27B0B6 ==========\n\nPescadero\nToken    Balance        Value in $\n-------  -----------  ------------\nAMPL     15826.63873       14928.8\nWETH     8.04035           14557.4\n$$$                        29486.2\n```\n\nAs shown in the example, `geyser-cli` will print the current LP-positions for\neach active Geyser in which the address is participating as well as the current\nUSD denominated value.\nThe current value is fetched from Chainlink's on-chain price feeds.\n\nAddresses which do not participate in a current Geyser will not be printed.\n\nAlso note that ENS resolution is supported.\n\n## TODOs\n\n- [ ] Calculate the interest earned per Geyser\n- [ ] Implement a `history` command to see the information about finished\n      Geysers\n\nAny kind of contribution is highly welcome!\n\n## Support\n\nIf there are any question, don't hesitate to ask!\n\nYou can reach me at pascal [at] merkleplant.xyz or in the official Ampleforth\nDiscord forum.\n\n## Acknowledgment\n\nThis project is heavily inspired by [uniswap-python](https://github.com/uniswap-python/uniswap-python).\n",
    'author': 'pascal-merkleplant',
    'author_email': 'pascal@merkleplant.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
