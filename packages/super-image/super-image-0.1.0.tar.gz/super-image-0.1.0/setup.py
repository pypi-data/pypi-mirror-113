# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['super_image',
 'super_image.data',
 'super_image.models',
 'super_image.models.edsr',
 'super_image.models.msrn',
 'super_image.utils']

package_data = \
{'': ['*']}

install_requires = \
['h5py==3.1.0',
 'huggingface-hub>=0.0.13,<0.0.14',
 'opencv-python==4.5.2.54',
 'torch==1.9.0',
 'torchvision==0.10.0',
 'tqdm==4.61.2']

entry_points = \
{'console_scripts': ['super-image = super_image.cli:main']}

setup_kwargs = {
    'name': 'super-image',
    'version': '0.1.0',
    'description': 'State-of-the-art image super resolution models for PyTorch.',
    'long_description': '<h1 align="center">super-image</h1>\n\n<p align="center">\n    <a href="https://eugenesiow.github.io/super-image/">\n        <img alt="documentation" src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat">\n    </a>\n    <a href="https://pypi.org/project/super-image/">\n        <img alt="pypi version" src="https://img.shields.io/pypi/v/super-image.svg">\n    </a>\n</p>\n\n<h3 align="center">\n    <p>State-of-the-art image super resolution models for PyTorch.</p>\n</h3>\n\n\n## Requirements\n\nsuper-image requires Python 3.6 or above.\n\n## Installation\n\nWith `pip`:\n```bash\npip install super-image\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 super-image\n```\n\n## Quick Start\n\n```python\nfrom super_image import EdsrModel, ImageLoader\nfrom PIL import Image\nimport requests\n\nurl = \'https://paperswithcode.com/media/datasets/Set5-0000002728-07a9793f_zA3bDjj.jpg\'\nimage = Image.open(requests.get(url, stream=True).raw)\n\nmodel = EdsrModel.from_pretrained(\'eugenesiow/edsr-base\', scale=2)\ninputs = ImageLoader.load_image(image)\npreds = model(inputs)\n\nImageLoader.save_image(preds, \'./scaled_2x.png\')\nImageLoader.save_compare(inputs, preds, \'./scaled_2x_compare.png\')\n```',
    'author': 'Eugene Siow',
    'author_email': 'kyo116@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eugenesiow/super-image',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
