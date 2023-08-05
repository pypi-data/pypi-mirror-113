# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tjax',
 'tjax._src',
 'tjax._src.dataclasses',
 'tjax._src.fixed_point',
 'tjax._src.gradient']

package_data = \
{'': ['*']}

install_requires = \
['colorful>=0.5.4,<0.6.0',
 'jax>=0.2.13,<0.3.0',
 'jaxlib>=0.1',
 'matplotlib>=3.3,<4.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.21',
 'optax>=0,<1',
 'yapf>=0.31']

setup_kwargs = {
    'name': 'tjax',
    'version': '0.12.6',
    'description': 'Tools for JAX.',
    'long_description': "=============\nTools for JAX\n=============\n\n.. role:: bash(code)\n    :language: bash\n\n.. role:: python(code)\n   :language: python\n\nThis repository implements a variety of tools for the differential programming library\n`JAX <https://github.com/google/jax>`_.\n\n----------------\nMajor components\n----------------\n\nTjax's major components are:\n\n- A dataclass decorator :python:`dataclasss` that facilitates defining JAX trees, and has a MyPy plugin.\n  (See `dataclass <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/dataclasses>`_ and `mypy_plugin <https://github.com/NeilGirdhar/tjax/blob/master/tjax/mypy_plugin.py>`_.)\n\n- A fixed point finding library heavily based on `fax <https://github.com/gehring/fax>`_.  Our\n  library (`fixed_point <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/fixed_point>`_):\n\n  - supports stochastic iterated functions,\n  - uses dataclasses instead of closures to avoid leaking JAX tracers, and\n  - supports higher-order differentiation.\n\n----------------\nMinor components\n----------------\n\nTjax also includes:\n\n- An object-oriented wrapper on top of `optax <https://github.com/deepmind/optax>`_.  (See\n  `gradient <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/gradient>`_.)\n\n- A pretty printer :python:`print_generic` for aggregate and vector types, including dataclasses.  (See\n  `display <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/display.py>`_.)\n\n- Versions of :python:`custom_vjp` and :python:`custom_jvp` that support being used on methods.\n  (See `shims <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/shims.py>`_.)\n\n- Tools for working with cotangents.  (See\n  `cotangent_tools <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/cotangent_tools.py>`_.)\n\n- A random number generator class :python:`Generator`.  (See `generator <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/generator.py>`_.)\n\n- JAX tree registration for `NetworkX <https://networkx.github.io/>`_ graph types.  (See\n  `graph <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/graph.py>`_.)\n\n- Leaky integration :python:`leaky_integrate` and Ornstein-Uhlenbeck process iteration\n  :python:`diffused_leaky_integrate`.  (See `leaky_integral <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/leaky_integral.py>`_.)\n\n- An improved version of :python:`jax.tree_util.Partial`.  (See `partial <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/partial.py>`_.)\n\n- A Matplotlib trajectory plotter :python:`PlottableTrajectory`.  (See `plottable_trajectory <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/plottable_trajectory.py>`_.)\n\n- A testing function :python:`assert_jax_allclose` that automatically produces testing code.  And, a related\n  function :python:`jax_allclose`.  (See `testing <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/testing.py>`_.)\n\n- Basic tools like :python:`divide_where`.  (See `tools <https://github.com/NeilGirdhar/tjax/blob/master/tjax/_src/tools.py>`_.)\n\nAlso, see the `documentation <https://neilgirdhar.github.io/tjax/tjax/index.html>`_.\n\n-----------------------\nContribution guidelines\n-----------------------\n\n- Conventions: PEP8.\n\n- How to run tests: :bash:`pytest .`\n\n- How to clean the source:\n\n  - :bash:`isort tjax`\n  - :bash:`pylint tjax`\n  - :bash:`mypy tjax`\n  - :bash:`flake8 tjax`\n",
    'author': 'Neil Girdhar',
    'author_email': 'mistersheik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NeilGirdhar/tjax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
