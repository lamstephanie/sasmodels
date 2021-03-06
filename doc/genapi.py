from __future__ import with_statement
import os.path

MODULE_TEMPLATE=""".. Autogenerated by genmods.py

******************************************************************************
%(name)s
******************************************************************************

:mod:`%(package)s.%(module)s`
==============================================================================

.. automodule:: %(package)s.%(module)s
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

"""

INDEX_TEMPLATE=""".. Autogenerated by genmods.py

.. _api-index:

##############################################################################
   %(package_name)s
##############################################################################

.. only:: html

   :Release: |version|
   :Date: |today|

.. toctree::
   :titlesonly:
   :numbered: 1
   :maxdepth: 2

   %(rsts)s
"""


def genfiles(package, package_name, modules, dir='api'):

    if not os.path.exists(dir):
        os.makedirs(dir)

    for module,name in modules:
        with open(os.path.join(dir,module+'.rst'), 'w') as f:
            f.write(MODULE_TEMPLATE%locals())

    rsts = "\n   ".join(module+'.rst' for module,name in modules)
    with open(os.path.join(dir,'index.rst'),'w') as f:
        f.write(INDEX_TEMPLATE%locals())


modules=[
    #('__init__', 'Top level namespace'),
    #('alignment', 'GPU data alignment [unused]'),
    ('bumps_model', 'Bumps interface'),
    ('convert', 'Sasview to sasmodel converter'),
    ('core', 'Model access'),
    ('direct_model', 'Simple interface'),
    ('exception', 'Annotate exceptions'),
    ('generate', 'Model parser'),
    ('kernelcl', 'OpenCL model evaluator'),
    ('kerneldll', 'Ctypes model evaluator'),
    ('kernelpy', 'Python model evaluator'),
    ('model_test', 'Unit test support'),
    ('resolution', '1-D resolution functions'),
    ('resolution2d', '2-D resolution functions'),
    ('sasview_model', 'Sasview interface'),
    ('sesans', 'SESANS model evaluator'),
    ('weights', 'Distribution functions'),
    #('transition', 'Model stepper for automatic model selection'),
]
package='sasmodels'
package_name='Reference'
genfiles(package, package_name, modules)
