# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lof']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'fastapi>=0.66.0,<0.67.0',
 'python-dotenv>=0.18.0,<0.19.0',
 'typer>=0.3.2,<0.4.0',
 'uvicorn>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['lof = lof.cli:cli']}

setup_kwargs = {
    'name': 'lof',
    'version': '0.2.2',
    'description': 'AWS Lambdas on FastAPI it is a Cli utilit that up & run your Python lambdas in local env based on AWS CloudFormation Template',
    'long_description': "\nAWS Lambdas on FastAPI - LoF\n----------------------------\n\nAWS Lambdas on FastAPI (LoF) is a command line tool that helps you fast & easy up & run your Python AWS Lambdas for tests and local development. \n\nPay attention, that this is only for **Python lambdas**.\n\nIt does not support any other programming languages.\n\nHow does it work?\n-----------------\n\nInstall\n^^^^^^^\n\n.. code-block:: bash\n\n\n       pip install lof\n\nNow run lof & provide to it path to your template yaml file.\nOr you can run it from source dir with template.yaml without any args\n\nHow to use\n^^^^^^^^^^\n\n.. code-block:: bash\n\n\n       lof\n\n       # or if path custom\n\n       lof --template example/template.yaml\n\nYou can choose that lambdas exclude from run by passing their names:\n\n.. code-block:: bash\n\n\n       lof --template example/template.yaml --exclude=PostLambda2Function\n\nTo pass environment variables to Lambdas, use flag --env, you can pass variables in 2 formats - json format and '.env' format. Both files as examples presented in example/ folder\n\n.. code-block:: bash\n\n\n       lof --env=.env\n\n       # or \n\n       lof --env=vars.json\n\nThis mean, that lof will up & run all lambdas exclude this 2: PostTrafficHook & Roles\n\nDemo\n----\n\nwill be added soon\n\nTODO\n----\n\n\n#. Add feature to call Authorizer & CORS lambdas handlers in local run.\n#. Support JSON AWS Cloud Formation Template\n\nExample\n-------\n\nTo try how LoF works you can use AWS CloudFormation template.yaml & Lambdas from example/ folder.\n\nIssues & features request\n-------------------------\n\nFill free to open Issues & report bugs. I will solve them as soon as possible.\n\nProblem Context\n---------------\n\nOn my current project I works a lot with AWS Lambdas & tries to up & run them with SAM local. \nAnd there is some issues especially when you work on the project with a big count of lambdas.\n\nSome of them:\n\n1) First of all it does not allow skip some lambdas form config\n2) It build lambdas inside each docker container so it takes significant time to build/rebuild & up all containers (and you need up all containers if you want to have fast integration tests)\n\nBoth points in the mix make impossible to use SAM in weak developers envs like VDI, for example.\n\nChangelog\n---------\n\n**v0.2.2**\n\n\n#. README.md is updated\n#. Fixed Issue with lambdas in template, that does not have Events with Path (like S3 triggered lambdas)\n#. Fixed issue with status code 204 - now it returns correct answer with no failes.\n#. Added some tests\n\n**v0.2.1**\n\n\n#. Now LoF do not try/except lambdas errors\n\n**v0.2.0**\n\n\n#. Fixed status_code resend from lambda & JSON body response\n\n**v0.1.0**\n\n\n#. First version of Lambdas on FastApi. \n   Based on AWS CloudFormation template it's serve lambdas as FastAPI endpoints for local testing.\n",
    'author': 'Iuliia Volkova',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xnuinside/lof',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
