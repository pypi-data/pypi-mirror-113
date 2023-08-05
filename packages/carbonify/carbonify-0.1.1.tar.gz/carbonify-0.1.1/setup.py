# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carbonify']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'nltk>=3.6.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'plotly>=5.1.0,<6.0.0',
 'streamlit>=0.84.1,<0.85.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'carbonify',
    'version': '0.1.1',
    'description': 'Open source library for carbon accounting and Lifecycle analysis',
    'long_description': '# Carbonify\n## Open source library for carbon accounting and Lifecycle analysis\n![](docs/assets/banner_carbonify.png)\n\nManipulating carbon data is complex and requires both climate expertise and the knowledge of the right data source to make valid hypothesis.\n\nThe **Carbonify** python library and tools are aimed to democratize data manipulation of carbon data to facilitate accounting and lifecycle analysis.  \n\n\n!!! warning "Experimental"\n    This library is extremely experimental, under active development and alpha-release\n    Don\'t expect the documentation to be up-to-date or all features to be tested\n    Please contact [us](mailto:theo.alvesdacosta@ekimetrics.com) if you have any question\n\n\n## Features\n### Current features\n- Easy access to Base Carbone by ADEME with data indexing\n- Data visualization and search functionalities to easily find carbon ratios\n\n\n## Installation\n### Install from PyPi\nThe library is available on [PyPi](https://pypi.org/project/carbonify/) via \n```\npip install carbonify\n```\n\n### For developers\n- You can clone the github repo / fork and develop locally\n- Poetry is used for environment management, dependencies and publishing, after clone you can run \n\n```\n# To setup the environment\npoetry install\n\n# To run Jupyter notebook or a python console\npoetry run jupyter notebook\npoetry run python\n```\n\n## Contributors\n- [Ekimetrics](https://ekimetrics.com/)\n\n\n\n## Project Structure\n```\n- carbonify/ # Your python library\n- data/\n    - raw/\n    - processed/\n- docs/\n- tests/                            # Where goes each unitary test in your folder\n- scripts/                          # Where each automation script will go\n- requirements.txt                  # Where you should put the libraries version used in your library\n```\n\n\n## References\n\n### Base Carbone\n- [Base Carbone](https://data.ademe.fr/datasets/base-carbone(r)) by ADEME - [Documentation](https://www.bilans-ges.ademe.fr/fr/accueil/contenu/index/page/presentation/siGras/0)\n- [Agribalyse](https://data.ademe.fr/datasets/agribalyse-synthese) by ADEME - [Documentation](https://doc.agribalyse.fr/documentation/conditions-dusage-des-donnees)\n- https://www.hellocarbo.com/blog/calculer/base-carbone/\n\n### LCA \n- [CarbonFact.co](https://carbonfact.co/)\n- https://www.carbonify.app/products/apple-iphone-12-us-64gb\n\n### EDA components\n- https://blog.streamlit.io/the-streamlit-agraph-component/\n- https://github.com/ChrisChross/streamlit-agraph\n',
    'author': 'Theo Alves Da Costa',
    'author_email': 'theo.alvesdacosta@ekimetrics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
