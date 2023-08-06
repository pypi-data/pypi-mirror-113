# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_typescript_generator', 'drf_typescript_generator.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.4,<4.0.0', 'djangorestframework>=3.12.4,<4.0.0']

setup_kwargs = {
    'name': 'drf-typescript-generator',
    'version': '0.1.1',
    'description': 'Package for generating TypeScript types from DRF serializers',
    'long_description': '# DRF Typescript generator\n\nThis package allows you to generate typescript types / interfaces for Django REST framework\nserializers, which can be then simply used in frontend applications.\n\n## Setup\n\nInstall the package with your preferred dependency management tool:\n\n```console\n$ poetry add drf-typescript-generator\n```\n\nAdd `drf_typescript_generator` to `INSTALLED_APPS` in your django settings&#46;py file:\n\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'drf_typescript_generator\',\n    ...\n]\n```\n\n## Usage\n\nTo generate types run django management command `generate_types` with the names of django apps\nyou want the script to look for serializers in:\n\n```console\n$ python manage.py generate_types my_app\n```\n\nExample serializer found in *my_app*:\n\n```python\nclass MySerializer(serializers.Serializer):\n    some_string = serializers.CharField(max_length=100)\n    some_number = serializers.IntegerField()\n    some_boolean = serializers.BooleanField()\n    choice = serializers.ChoiceField(\n        choices=[1, 2, 3],\n        allow_null=True\n    )\n    multichoice = serializers.MultipleChoiceField(\n        choices=[2, 3, 5]\n    )\n```\n\nGenerated typescript type:\n\n```typescript\nexport type MySerializer = {\n  choice: 1 | 2 | 3 | null\n  multichoice: (2 | 3 | 5)[]\n  someBoolean: boolean\n  someNumber: number\n  someString: string\n}\n```\n\nThe script looks for DRF routers in project urls&#46;py file as well as urls&#46;py files in given\napps and extracts serializers based on viewsets defined in those routers.\n\n### Arguments\n\nThe `generate_types` command supports following arguments:\n\n| Argument | Value type | Description | Default value |\n| --- | --- | --- | --- |\n| `--format` | "type" \\| "interface" | Whether to output typescript types or interfaces | "type"\n| `--semicolons` | boolean | If the argument is present semicolons will be added in output | False\n| `--spaces` | int | Output indentation will use given number of spaces (mutually exclusive with `--tabs`). Spaces are used if neither `--spaces` nor `--tabs` argument is present. | 2\n| `--tabs` | int | Output indentation will use given number of tabs (mutually exclusive with `--spaces`) | None\n\n## Features\n\nThe package currently supports following features that are correctly transformed to typescript syntax:\n\n- [X] Basic serializers\n- [X] Model serializers\n- [X] Nested serializers\n- [X] Method fields (typed with correct type if python type hints are used)\n- [X] Required / optional fields\n- [X] List fields \n- [X] Choice and multiple choice fields (results in composite typescript type)\n- [X] allow_blank, allow_null (results in composite typescript type)\n\nMore features are planned to add later on:\n\n- [ ] One to many and many to many fields correct typing\n- [ ] Differentiate between read / write only fields while generating type / interface\n- [ ] Integration with tools like [drf_yasg](https://github.com/axnsan12/drf-yasg) to allow downloading the\ngenerated type from the documentation of the API\n- [ ] Accept custom mappings\n',
    'author': 'napmn',
    'author_email': 'lukass135@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/remastr/drf-typescript-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
