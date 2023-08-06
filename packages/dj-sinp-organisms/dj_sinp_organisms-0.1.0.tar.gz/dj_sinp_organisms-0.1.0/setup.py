# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sinp_organisms', 'sinp_organisms.migrations']

package_data = \
{'': ['*'], 'sinp_organisms': ['fixtures/*']}

install_requires = \
['Django>=3.2.5,<4.0.0',
 'dj-sinp-nomenclatures>=0.1.1,<0.2.0',
 'django-rest-framework>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'dj-sinp-organisms',
    'version': '0.1.0',
    'description': 'Django app to manage french SINP organisms standard',
    'long_description': '=========================\nSINP Organisms for Django\n=========================\n\n`DjangoSinpOrganisms <https://github.com/dbchiro/DjangoSinpOrganisms>`_ is a simple `Django <https://www.djangoproject.com/>`_ reusable app to manage `French SINP Organisms <http://standards-sinp.mnhn.fr/referentiel-des-organismes/>`_, respecting standard.\n\n\nDetailed documentation is in the "docs" directory.\n\nQuick start\n-----------\n\n1. Install app\n\n.. code-block:: bash\n\n    $ pip install -U dj-sinp-organisms\n\n\n\n2. Configure ``INSTALLED_APPS``:\n\n.. code-block:: python\n\n    INSTALLED_APPS = (\n        \'django.contrib.admin\',\n        \'django.contrib.auth\',\n        (...),\n        \'rest_framework\',\n        \'sinp_nomenclatures\',\n        \'sinp_organisms\',\n        (...),\n    )\n\n\n3. Configure ``urls.py``:\n\n.. code-block:: python\n\n    urlpatterns = [\n        path(\'admin/\', admin.site.urls),\n        path(\'api-auth/\', include(\'rest_framework.urls\')),\n        (...),\n        path(\'api/v1/\', include(\'sinp_nomenclatures.urls\')),\n        path(\'api/v1/\', include(\'sinp_organisms.urls\')),\n        (...),\n    ]\n\n4. Run ``python manage.py migrate`` to create the polls models.\n\n5. Start the development server and visit http://127.0.0.1:8000/admin/\n   to create an organism (you\'ll need the Admin app enabled).\n\n6. Visit http://127.0.0.1:8000/api/v1/organisms to view organisms API.\n',
    'author': 'dbChiro project',
    'author_email': 'project@dbchiro.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbchiro/DjangoSinpNomenclature',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
