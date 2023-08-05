# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pacsanini',
 'pacsanini.cli',
 'pacsanini.io',
 'pacsanini.net',
 'pacsanini.pipeline']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4',
 'click>=7.1.2,<8.0.0',
 'loguru>=0.5.3,<0.6.0',
 'luigi>=3.0.3,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pydantic>=1.7.4',
 'pydicom>=2.1.2,<3.0.0',
 'pynetdicom>=1.5.7,<2.0.0']

entry_points = \
{'console_scripts': ['pacsanini = pacsanini.cli:entry_point']}

setup_kwargs = {
    'name': 'pacsanini',
    'version': '0.1.1',
    'description': 'A package for DICOM utilities.',
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/pacsanini/badge/?version=latest)](https://pacsanini.readthedocs.io/en/latest/?badge=latest)\n![GitHub](https://img.shields.io/github/license/Therapixel/pacsanini) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Therapixel/pacsanini)\n\n# pacsanini\n\n`pacsanini` 🎻 is a package designed to help with the collection of DICOM files and the extraction\nof DICOM tags (metadata) for structuring purposes.\n\n`pacsanini`'s functionalities come out of a desire to facilitate research in\nmedical imagery by easing the process of data collection and structuring.\nThe two main pain points for this are:\n\n* acquiring data from a PACS\n* extracting metadata from DICOM files in research-ready formats (eg: csv)\n\nThe project seeks to target medical/research professionals that are not necessarily\nfamiliar with coding but wish to obtain data sets and software engineers that wish to\nbuild applications with a certain level of abstraction.\n\n## Documentation\n\nCheck out the complete documentation on [readthedocs](https://pacsanini.readthedocs.io/en/latest/).\nYou will be able to find examples on how to use the `pacsanini` API from within you Python application\nand as a command line tool.\n\n## Contributing and Code of Conduct\n\nAll contributions to improve `pacsanini` are welcome and valued. For more information on how you can contribute,\nplease read the [Contributing](CONTRIBUTING.md) document and make sure that you are familiar with our\n[Code of Conduct](CODE_OF_CONDUCT.md).\n\n## Installation\n\nTo obtain the cutting edge version of `pacsanini`, you can use `pip` or `poetry` in the following way:\n\n```bash\npip install git+https://github.com/Therapixel/pacsanini.git\n# or\npoetry add git+https://github.com/Therapixel/pacsanini.git\n```\n### For development\n\n`poetry` is the only supported build tool for installing `pacsanini` in a development context.\nSee the previous section on how to install `poetry`.\n\n```bash\ngit clone https://github.com/Therapixel/pacsanini.git\ncd pacsanini\npoetry install --no-root --no-dev\n# or, to install the project and its development dependencies:\npoetry install --no-root\n```\n\n### Usage with docker\n\nA docker image can be built locally to run `pacsanini` within an isolated environment.\n\n```bash\ndocker image build -t latest .\ndocker run pacsanini --help\n```\n\n## Roadmap\n\nThe following topics are the main areas where `pacsanini` can improve as a library and a tool.\nOf course, these topics are up for discussion and such discussions are encouraged in the\n[GitHub issues](https://github.com/Therapixel/pacsanini/issues) section.\n\n### Documentation\n\n* 🚧 Provide more in-depth examples of how `pacsanini` can be used and be useful inside\n  python applications\n\n### Data Collection\n\n* 🚧 Make the single-command pipeline more mature.\n  * Add a feature to send notifications when a step is done\n\n* 🚧 Use sql storage as an alternative to CSV storage.\n\n* 🚧 Improve error handling for C-MOVE operations.\n\n* 🚧 Implement the ability for event handling when DICOM files are received by the storescp server.\n\n### Testing\n\n* 🚧 Find a good way to test DICOM network messaging applications. Possibly with the\n  `dcmtk` suite, the apps from `pynetdicom` or even a Docker container with a PACS?\n",
    'author': 'Aurélien Chick',
    'author_email': 'achick@therapixel.com',
    'maintainer': 'Aurélien Chick',
    'maintainer_email': 'achick@therapixel.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
