# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pidng']

package_data = \
{'': ['*'], 'pidng': ['liblj92/*']}

install_requires = \
['exifread>=2.3.2,<3.0.0', 'numpy>=1.14,<2.0']

setup_kwargs = {
    'name': 'pidng',
    'version': '3.4.7',
    'description': 'Python utility for converting Raspberry Pi Camera RAW images into Adobe DNG Format.',
    'long_description': 'PYDNG\n=========\n![](https://img.shields.io/badge/Version-3.4.7-green.svg)\n\nCreate Adobe DNG RAW files using Python.\n\n![](https://raw.githubusercontent.com/schoolpost/PiDNG/master/docs/demo.jpg)\n\n**Features**\n------------\n\n- 8,10,12,14,16-bit precision\n- Lossless compression\n- DNG Tags ( extensible )\n\n### Works with any **Bayer RAW** Data including native support for **Raspberry Pi cameras**.\n- OV5467 ( Raspberry Pi Camera Module V1 )\n- IMX219 ( Raspberry Pi Camera Module V2 )\n- IMX477( Raspberry Pi High Quality Camera )\n\n*Raspberry Pi High Quality Camera examples below ( DNG top, JPEG bottom )*\n\n![](https://raw.githubusercontent.com/schoolpost/PiDNG/master/docs/collage.jpg)\n\n***\n\nInstructions\n------------\n\nRequires: \n- Python3 \n- Numpy  \n- ExifRead\n\n\n### Install\n\nFrom PyPI:\n```\npython3 -mpip install PiDNG \n```\n\nLatest version from GitHub:\n\n```\npython3 -mpip install  git+https://github.com/schoolpost/PiDNG.git\n```\n\nInstall via Poetry:\n\nPer command line in your poetry environment:\n```\npoetry add PiDNG \n```\nOr add in to your pyproject.toml file:\n\n```\n[tool.poetry.dependencies]\n...\nPiDNG = "^3.4.5"\n```\n\n\n### How to use:\n\n```\n\n# examples\nfrom pidng.core import RPICAM2DNG\n\n# use file string input to the jpeg+raw file. \nd = RPICAM2DNG()\nd.convert(\'imx477.jpg\')\n\n\n# the included command line utility can be used as shown below\nUtility.py:\n  python3 examples/utility.py <options> <inputFilename> \n  python3 examples/utility.py imx477.jpg  \n\n```\n\n***\n\nTODO\n------------\n\n- SUB IFDS/THUMBNAILS\n\n***\n\nCredits\n------------\nSource referenced from:\n\nCanPi ( Jack ) | [color-matrices](https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=278828)\n\nWaveform80 | [picamera](https://github.com/waveform80/picamera)\n\nKrontech | [chronos-utils](https://github.com/krontech/chronos-utils)\n\nAndrew Baldwin | [MLVRawViewer](https://bitbucket.org/baldand/mlrawviewer)\n\n\n',
    'author': 'Csaba Nagy',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/schoolpost/PiDNG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
