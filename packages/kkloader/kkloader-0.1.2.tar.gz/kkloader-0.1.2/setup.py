# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kkloader']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'kkloader',
    'version': '0.1.2',
    'description': 'a simple deserializer / serializer for Koikatu / EmotionCreators data.',
    'long_description': '# KoikatuCharaLoader\nA simple deserializer / serializer for Koikatu / EmotionCreators character data.\n\n# Installation\nYou can install this module from [PyPI](https://pypi.org/project/kkloader/).\n```\n$ pip install kkloader\n```\nIf this does not work, try the following command (for Windows users, maybe).\n```\n$ python -m pip install kkloader\n```\n\n# Basic Usage\n```python\n$ python\n>>> from kkloader import KoikatuCharaData # Load a module.\n>>> kc = KoikatuCharaData.load("./data/kk_chara.png") # Load a character data.\n>>> kc.parameter["nickname"] # Print character\'s nickname.\n\'かずのん\'\n>>> kc.parameter["nickname"] = "chikarin" # Renaming nickname.\n>>> kc.save("./kk_chara_modified.png") # Save to `kk_chara_modified.png`.\n```\nthat\'s it :)\n\n# Export to JSON file\n```\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("sa.png")\nk.save_json("sa.json") \n```\n\n`sa.json`\n```sa.json\n{\n  "product_no": 100,\n  "header": "\\u3010KoiKatuChara\\u3011",\n  "version": "0.0.0",\n  "custom": {\n    "face": {\n      "version": "0.0.2",\n      "shapeValueFace": [\n        0.5403226017951965,\n        1.0,\n        0.2016129046678543,\n        0.0,\n        0.22580644488334656,\n        0.0,\n        0.0,\n        0.1794193685054779,\n        0.0,\n...\n```\n\n# Recipes\n\n### Rename Character\'s Name\n```python\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("sa.png")\nk.parameter["lastname"] = "春野"\nk.parameter["firstname"] = "千佳"\nk.parameter["nickname"] = "ちかりん"\nk.save("si.png")\n```\n\n### Set the Height of Character to 50\n```python\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("sa.png")\nk.custom["body"]["shapeValueBody"][0] = 0.5\nk.save("si.png")  \n```\n\n### Remove Swim Cap\n```python\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("sa.png")\nfor i,c in enumerate(k.coordinate):\n    for n,p in enumerate(c["accessory"]["parts"]):\n        if p["id"] == 5:\n            k.coordinates[i]["accessory"]["parts"][n]["type"] = 120\nk.save("si.png")  \n```\n\n### Remove Under Hair\n```python\nfrom kkloader import KoikatuCharaData\nk = KoikatuCharaData.load("sa.png")\nkc.Custom.body["underhairId"] = 0\nk.save("si.png")\n```\n\n# Member Variables\n\n| KoikatuCharaData.* |                  |\n|-------------------:|-----------------:|\n|            png_data|     raw png image|\n|       face_png_data|    raw face image|\n|    face, body, hair|      shape values|\n|   coordinates(List)| contains seven coordinates corresponding to situation.|\n| parameter | personal data (i.e. name, birthday, personality, ..etc)|\n\n# Acknowledgements\n- [martinwu42/pykoikatu](https://github.com/martinwu42/pykoikatu)',
    'author': 'great-majority',
    'author_email': 'yosaku.ideal+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/great-majority/KoikatuCharaLoader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
