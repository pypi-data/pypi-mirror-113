from setuptools import setup, find_packages
from pathlib import Path


def get_version() -> str:
    local_dict = {}
    with open(str(Path(__file__).parent / 'src' / 'plt_pack' / '__version.py'), 'r') as f:
        exec(f.read(), {}, local_dict)

    return local_dict['__version__']


__version__ = get_version()

install_requires = [
    'numpy',
    'msgpack>=1.0.0',
    'msgpack-numpy>=0.4.7.1',
    'matplotlib',
    'packaging',
]

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

setup(
    name='plt_pack',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version=__version__,
    author='Vladimir Starostin',
    author_email='vladimir.starostin@uni-tuebingen.de',
    url='https://github.com/StarostinV/plt-pack',
    description='A packaging tool for storing and exchanging data & code bound'
                ' in a single file. Main focus on supporting matplotlib package'
                ' for exchanging scientific figures. Integrated with Jupyter Notebook.',
    license='MIT',
    python_requires='>=3.7.2',
    install_requires=install_requires,
    classifiers=classifiers,
)
