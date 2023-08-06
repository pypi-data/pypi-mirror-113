from setuptools import setup, find_packages

setup(
    name="PyDeepAI",
    version='0.2.0',
    author="Mikhail Serebryakov a.k.a Zanga",
    author_email="<rayman.channel@yandex.ru>",
    description='Unofficial DeepAI python module',
    long_description_content_type="text/markdown",
    long_description='''# pydeepai
Unofficial DeepAI python module
## Examples

### Create a API object

Without proixes:

```
>>> from PyDeepAI import API
>>> DEEPAI_API = API(key='quickstart-QUdJIGlzIGNvbWluZy4uLi4K')
>>> print(str(DEEPAI_API))
<API quickstart-QUdJIGlzIGNvbWluZy4uLi4K>
```

With proixes:

```
>>> from PyDeepAI import API
>>> DEEPAI_API = API(key='quickstart-QUdJIGlzIGNvbWluZy4uLi4K', proxies={
        "http": "http://localhost:1000",
        "https": "http://localhost:1000"
>>> })
>>> print(str(DEEPAI_API))
<API quickstart-QUdJIGlzIGNvbWluZy4uLi4K>
```

### Make a Request

```
>>> IMAGE_URL = 'https://otnoshenija.ru/wp-content/uploads/2019/11/sinonimy-otnosheniya-druzheskie.jpg'
>>> print(DEEPAI_API.request('facial-recognition', IMAGE_URL))
{'id': 'b727c61b-c55e-4b4b-af61-f075afd08e38', 'output': {'faces': [{'confidence': '0.99', 'bounding_box': [8, 617, 202, 242], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [285, 347, 129, 161], 'name': 'face'}, {'confidence': '0.97', 'bounding_box': [566, 114, 158, 191], 'name': 'face'}, {'confidence': '0.9', 'bounding_box': [450, 294, 152, 191], 'name': 'face'}, {'confidence': '0.87', 'bounding_box': [675, 399, 135, 188], 'name': 'face'}, {'confidence': '0.65', 'bounding_box': [799, 377, 154, 176], 'name': 'face'}, {'confidence': '0.91', 'bounding_box': [559, 649, 158, 184], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [1005, 319, 182, 219], 'name': 'face'}, {'confidence': '0.81', 'bounding_box': [879, 611, 231, 242], 'name': 'face'}]}}
```

```
>>> import requests
>>> IMAGE = requests.get(IMAGE_URL).content
>>> print(DEEPAI_API.request('facial-recognition', IMAGE, 'image'))
{'id': 'b727c61b-c55e-4b4b-af61-f075afd08e38', 'output': {'faces': [{'confidence': '0.99', 'bounding_box': [8, 617, 202, 242], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [285, 347, 129, 161], 'name': 'face'}, {'confidence': '0.97', 'bounding_box': [566, 114, 158, 191], 'name': 'face'}, {'confidence': '0.9', 'bounding_box': [450, 294, 152, 191], 'name': 'face'}, {'confidence': '0.87', 'bounding_box': [675, 399, 135, 188], 'name': 'face'}, {'confidence': '0.65', 'bounding_box': [799, 377, 154, 176], 'name': 'face'}, {'confidence': '0.91', 'bounding_box': [559, 649, 158, 184], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [1005, 319, 182, 219], 'name': 'face'}, {'confidence': '0.81', 'bounding_box': [879, 611, 231, 242], 'name': 'face'}]}}
```

```
>>> import requests
>>> IMAGE = requests.get(IMAGE_URL).content
>>> open("file.jpg", "wb").write(IMAGE)
>>> print(DEEPAI_API.request('facial-recognition', open('file.jpg', 'rb'), 'image'))
{'id': 'b727c61b-c55e-4b4b-af61-f075afd08e38', 'output': {'faces': [{'confidence': '0.99', 'bounding_box': [8, 617, 202, 242], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [285, 347, 129, 161], 'name': 'face'}, {'confidence': '0.97', 'bounding_box': [566, 114, 158, 191], 'name': 'face'}, {'confidence': '0.9', 'bounding_box': [450, 294, 152, 191], 'name': 'face'}, {'confidence': '0.87', 'bounding_box': [675, 399, 135, 188], 'name': 'face'}, {'confidence': '0.65', 'bounding_box': [799, 377, 154, 176], 'name': 'face'}, {'confidence': '0.91', 'bounding_box': [559, 649, 158, 184], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [1005, 319, 182, 219], 'name': 'face'}, {'confidence': '0.81', 'bounding_box': [879, 611, 231, 242], 'name': 'face'}]}}
```

```
>>> import requests, io
>>> IMAGE = io.BytesIO(requests.get(IMAGE_URL).content)
>>> print(DEEPAI_API.request('facial-recognition', IMAGE, 'image'))
{'id': 'b727c61b-c55e-4b4b-af61-f075afd08e38', 'output': {'faces': [{'confidence': '0.99', 'bounding_box': [8, 617, 202, 242], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [285, 347, 129, 161], 'name': 'face'}, {'confidence': '0.97', 'bounding_box': [566, 114, 158, 191], 'name': 'face'}, {'confidence': '0.9', 'bounding_box': [450, 294, 152, 191], 'name': 'face'}, {'confidence': '0.87', 'bounding_box': [675, 399, 135, 188], 'name': 'face'}, {'confidence': '0.65', 'bounding_box': [799, 377, 154, 176], 'name': 'face'}, {'confidence': '0.91', 'bounding_box': [559, 649, 158, 184], 'name': 'face'}, {'confidence': '0.93', 'bounding_box': [1005, 319, 182, 219], 'name': 'face'}, {'confidence': '0.81', 'bounding_box': [879, 611, 231, 242], 'name': 'face'}]}}
```
''',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'api', 'image api', 'video api', 'requests', 'http'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
