"""
sasmodels
=========

**sasmodels** is a package containing models for small angle neutron and xray
scattering.  Models supported are the one dimensional circular average and
two dimensional oriented patterns.  As well as the form factor calculations
for the individual shapes **sasmodels** also provides automatic shape
polydispersity, angular dispersion and resolution convolution.  SESANS
patterns can be computed for any model.

Models can be written in python or in C.  C models can run on the GPU if
OpenCL drivers are available.  See :mod:`generate` for details on
defining new models.
"""
__version__ = "0.9"

def data_files():
    """
    Return the data files to be installed with the package.

    The format is a list of (directory, [files...]) pairs which can be
    used directly in setup(...,data_files=...) for setup.py.
    """
    from os.path import join as joinpath
    import glob

    from .generate import EXTERNAL_DIR, DATA_PATH

    def expand_patterns(path, patterns):
        target_path = joinpath(EXTERNAL_DIR, *path)
        source_path = joinpath(DATA_PATH, *path)
        files = []
        for p in patterns:
            files.extend(glob.glob(joinpath(source_path, p)))
        return target_path, files

    return_list = [
        expand_patterns([], ['*.c', '*.cl', 'convert.json']),
        expand_patterns(['models'], ['*.c']),
        expand_patterns(['models', 'lib'], ['*.c']),
        ]
    return return_list


