# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basis_modules',
 'basis_modules.helpers',
 'basis_modules.helpers.importers',
 'basis_modules.modules',
 'basis_modules.modules.alphavantage',
 'basis_modules.modules.alphavantage.importers',
 'basis_modules.modules.alphavantage.tests',
 'basis_modules.modules.bigcommerce',
 'basis_modules.modules.bigcommerce.importers',
 'basis_modules.modules.bigcommerce.tests',
 'basis_modules.modules.business_intelligence',
 'basis_modules.modules.business_intelligence.functions',
 'basis_modules.modules.business_intelligence.functions.transaction_ltv_model',
 'basis_modules.modules.business_intelligence.functions.transaction_ltv_model.tests',
 'basis_modules.modules.business_intelligence.tests',
 'basis_modules.modules.crunchbase',
 'basis_modules.modules.crunchbase.importers',
 'basis_modules.modules.crunchbase.tests',
 'basis_modules.modules.fred',
 'basis_modules.modules.fred.importers',
 'basis_modules.modules.fred.tests',
 'basis_modules.modules.mailchimp',
 'basis_modules.modules.mailchimp.exporters',
 'basis_modules.modules.mailchimp.tests',
 'basis_modules.modules.marketstack',
 'basis_modules.modules.marketstack.importers',
 'basis_modules.modules.marketstack.tests',
 'basis_modules.modules.marketstack.transformers',
 'basis_modules.modules.plotly',
 'basis_modules.modules.shopify',
 'basis_modules.modules.shopify.importers',
 'basis_modules.modules.shopify.tests',
 'basis_modules.modules.square',
 'basis_modules.modules.square.importers',
 'basis_modules.modules.square.tests',
 'basis_modules.modules.stocks',
 'basis_modules.modules.stripe',
 'basis_modules.modules.stripe.exporters',
 'basis_modules.modules.stripe.importers',
 'basis_modules.modules.stripe.tests',
 'basis_modules.modules.stripe.transformers']

package_data = \
{'': ['*'],
 'basis_modules.modules.alphavantage': ['schemas/*'],
 'basis_modules.modules.bigcommerce': ['schemas/*'],
 'basis_modules.modules.business_intelligence': ['schemas/*'],
 'basis_modules.modules.crunchbase': ['schemas/*'],
 'basis_modules.modules.fred': ['schemas/*'],
 'basis_modules.modules.mailchimp': ['schemas/*'],
 'basis_modules.modules.marketstack': ['schemas/*'],
 'basis_modules.modules.plotly': ['schemas/*'],
 'basis_modules.modules.shopify': ['schemas/*'],
 'basis_modules.modules.square': ['schemas/*'],
 'basis_modules.modules.stocks': ['schemas/*'],
 'basis_modules.modules.stripe': ['schemas/*']}

install_requires = \
['basis-core>=0,<1']

setup_kwargs = {
    'name': 'basis-modules',
    'version': '0.1.1',
    'description': 'Basis modules repository',
    'long_description': None,
    'author': 'Ken Van Haren',
    'author_email': 'kenvanharen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
