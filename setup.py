import setuptools
from importlib.machinery import SourceFileLoader
import os

dirname = os.path.dirname(__file__)
path_version = os.path.join(dirname, "transport_service/_version.py")
version = SourceFileLoader('version', path_version).load_module()

setuptools.setup(
    name='transport_service',
    version=version.__version__,
    description='Wrapper for transport services',
    author='Pantelis Mitropoulos',
    author_email='pmitropoulos@getmap.gr',
    license='Apache',
    packages=setuptools.find_packages(exclude=('tests*',)),
    package_data={'transport_service': [
        'logging.conf'
    ]},
    python_requires='>=3.7',
    zip_safe=False,
)
