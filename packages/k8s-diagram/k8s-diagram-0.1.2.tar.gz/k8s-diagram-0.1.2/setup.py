# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['k8s_diagram']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'argparse>=1.4.0,<2.0.0',
 'diagrams>=0.20.0,<0.21.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['k8s-diagram = k8s_diagram.app:app']}

setup_kwargs = {
    'name': 'k8s-diagram',
    'version': '0.1.2',
    'description': 'Creates a preview diagram of Kubernetes Resources without the need to apply them.',
    'long_description': '# K8s Diagram Previewer\n\nThis project exists to help developers take some of the guesswork\nout of deploying Kubernetes definitions by providing a preview of\nwhat will actually be deployed with a set of YAML definitions.\n\n## Installation\n\nClone the repo and run `pip install k8s-diagram`\n\n  You may also need to install [graphviz](https://graphviz.org/download/).\n\n## Running\n\nThis script takes one argument, a path to a folder containing K8s \nYAML definitions and outputs a PNG diagram at kubernetes.png \nrepresenting those definitions, as well as a python file at \ncreate_diagram.py if you would like to extend the diagram with \nother infrastructure surrounding your project. To automatically\nopen the image upon completion, add the `--show` flag.\n\n`k8s-diagram <path_to_folder>`\n\nTo try out the example, run `k8s-diagram ./example_yaml`\n\nFor Helm Charts, simply run with the --helm flag and your chart will be\ntemplated and placed into `/tmp/helm_preview_yaml/chart.yaml` before the script runs.\n\nYou can also pass in a context from kubeconfig with the `--cluster-context` flag to pull in all supported resources from\nthe target context prior to diagram generation.\n\nRun `k8s-diagram --help` to see other available options.\n\n## Support\n\nThis tool currently supports the following Kubernetes resource types:\n\n* Deployment\n* Service\n* Ingress\n* Pod\n* CronJob\n* Job\n* DaemonSet\n* StatefulSet\n* ConfigMap\n* Secret\n* PersistentVolumeClaim\n\nThere is partial support for all node types listed at https://diagrams.mingrammer.com/docs/nodes/k8s but links will not be formed.',
    'author': 'Jimmy Mills',
    'author_email': 'jimmyemills+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
