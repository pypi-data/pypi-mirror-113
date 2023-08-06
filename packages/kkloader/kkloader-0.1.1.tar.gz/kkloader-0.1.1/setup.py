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
    'version': '0.1.1',
    'description': 'a simple deserializer / serializer for Koikatu / EmotionCreators data.',
    'long_description': '# KoikatuCharaLoader\na simple deserializer / serializer for Koikatu / EmotionCreators character data.\n\n# update: "dump as json" is now available.\n```\nfrom KoikatuCharaData import KoikatuCharaData\n\ndef main():\n    k = KoikatuCharaData.load("sa.png")\n    k.save_json("sa.json")\n\nif __name__==\'__main__\':\n    main()  \n```\n\n- `sa.json`\n```sa.json\n{\n  "product_no": 100,\n  "header": "\\u3010KoiKatuChara\\u3011",\n  "version": "0.0.0",\n  "custom": {\n    "face": {\n      "version": "0.0.2",\n      "shapeValueFace": [\n        0.5403226017951965,\n        1.0,\n        0.2016129046678543,\n        0.0,\n        0.22580644488334656,\n        0.0,\n        0.0,\n        0.1794193685054779,\n        0.0,\n...\n```\n\n# install\nrequires python 3.x and `msgpack`\n```\n$ git clone https://github.com/106-/KoikatuCharaLoader.git\n$ cd KoikatuCharaLoader\n$ pip install -r requirements.txt\n```\n\n# examples\n\n## renaming character\n```python\nfrom KoikatuCharaData import KoikatuCharaData\n\ndef main():\n    k = KoikatuCharaData.load("sa.png")\n    k.parameter["lastname"] = "春野"\n    k.parameter["firstname"] = "千佳"\n    k.parameter["nickname"] = "ちかりん"\n    k.save("si.png")\n\nif __name__==\'__main__\':\n    main()   \n```\n\n## set the height of character to 50\n```python\nfrom KoikatuCharaData import KoikatuCharaData\n\ndef main():\n    k = KoikatuCharaData.load("sa.png")\n    k.custom["body"]["shapeValueBody"][0] = 0.5\n    k.save("si.png")\n\nif __name__==\'__main__\':\n    main()    \n```\n\n## remove swim cap\n```python\nfrom KoikatuCharaData import KoikatuCharaData\n\ndef main():\n    k = KoikatuCharaData.load("sa.png")\n    for i,c in enumerate(k.coordinate):\n        for n,p in enumerate(c["accessory"]["parts"]):\n            if p["id"] == 5:\n                k.coordinates[i]["accessory"]["parts"][n]["type"] = 120\n    k.save("si.png")\n\nif __name__==\'__main__\':\n    main()    \n```\n\n## remove under hair\n```python\nfrom KoikatuCharaData import KoikatuCharaData\nk = KoikatuCharaData.load("sa.png")\nkc.Custom.body["underhairId"] = 0\nk.save("si.png")\n```\n\n# member variables\n\n| KoikatuCharaData.* |                  |\n|-------------------:|-----------------:|\n|            png_data|     raw png image|\n|       face_png_data|    raw face image|\n|    face, body, hair|      shape values|\n|   coordinates(List)| contains seven coordinates corresponding to situation.|\n| parameter | personal data (i.e. name, birthday, personality, ..etc)|\n\n# refer\npngデータの長さの取得にあたり, [martinwu42/pykoikatu](https://github.com/martinwu42/pykoikatu)を参考にしました.',
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
